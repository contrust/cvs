import os
from pathlib import Path

from cvs.config import index_path
from cvs.create_tree import create_tree
from cvs.hash_object import Blob, Tree, HashObject
from cvs.index import get_index_tree


class AlreadyDeletedException(Exception):
    pass


class NotModifiedException(Exception):
    pass


def modify_index(object_path: str, is_adding: bool) -> None:
    object_path = os.path.relpath(object_path)
    add_object = None
    if object_path.startswith('..'):
        print('Can not modify object outside of the working directory.')
        return
    if is_adding:
        if os.path.isfile(object_path):
            try:
                with open(object_path, mode='rb') as blob_file:
                    add_object = Blob(blob_file.read())
            except FileNotFoundError:
                print(f'Can not open {object_path}')
        elif os.path.isdir(object_path):
            try:
                add_object = create_tree(object_path)
            except FileNotFoundError:
                print(f'Can not create tree for {object_path}')
                return
        else:
            print(f'There is no directory or file with {object_path} path')
            return
    try:
        index_tree = get_index_tree()
    except FileNotFoundError:
        print(f'Can not create index tree because index file does not exist.')
        return
    except AttributeError:
        print(f'Index tree file does not match tree format.')
        return
    try:
        insert_hash_object(index_tree, add_object, Path(object_path).parts)
    except FileNotFoundError:
        print('Trees or blobs in cvs folder does not exist.')
        return
    except AlreadyDeletedException:
        print(f'Can not remove {object_path} '
              f'because there is no such path in index.')
        return
    except NotModifiedException:
        print(f'Can not add {object_path} '
              f'because it was not modified since last adding.')
        return
    try:
        index_path.write_text(index_tree.content_hash)
    except FileNotFoundError:
        print('Index file does not exist.')
        return
    print(f'Successfully {"added" if is_adding else "removed"} {object_path}')


def insert_hash_object(tree: Tree, hash_object: HashObject,
                       path_parts: tuple) -> None:
    if not path_parts:
        tree.children = hash_object.children if hash_object else {}
    elif len(path_parts) == 1:
        if hash_object:
            if (path_parts[0] in tree.children and
                    tree.children[path_parts[0]].update_hash() ==
                    hash_object.update_hash()):
                raise NotModifiedException
            tree.children[path_parts[0]] = hash_object
        else:
            if path_parts[0] in tree.children:
                del tree.children[path_parts[0]]
            else:
                raise AlreadyDeletedException
    else:
        if (hash_object and
                not isinstance(tree.children.get(path_parts[0]), Tree)):
            tree.children[path_parts[0]] = Tree()
        insert_hash_object(tree.children[path_parts[0]],
                           hash_object, path_parts[1:])
    tree.update_hash()


def add(object_path: str):
    modify_index(object_path, True)


def rm(object_path: str):
    modify_index(object_path, False)
