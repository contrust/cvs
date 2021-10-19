import os
from pathlib import Path

from cvs.config import index_path
from cvs.create_tree import create_tree
from cvs.hash_object import Blob, Tree, HashObject
from cvs.read_tree import read_tree


def add(object_path: str) -> None:
    object_path = os.path.relpath(object_path)
    if object_path.startswith('..'):
        print('Can not add object outside of the working directory.')
        return
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
        index_tree_hash = index_path.read_text()
    except FileNotFoundError:
        print('Index file does not exist.')
        return
    try:
        index_tree = read_tree(index_tree_hash) if index_tree_hash else Tree()
    except (FileNotFoundError, AttributeError):
        print(f'Error occurred while reading tree {index_tree_hash}')
        return
    try:
        insert_hash_object(index_tree, add_object, Path(object_path).parts)
    except FileNotFoundError:
        print('Trees folder does not exist.')
        return
    try:
        index_path.write_text(index_tree.content_hash)
    except FileNotFoundError:
        print('Index file does not exist.')
        return
    print(f'Successfully updated {object_path}')


def insert_hash_object(tree: Tree, hash_object: HashObject,
                       path_parts: tuple) -> None:
    if not path_parts:
        tree.children = hash_object.children
    elif len(path_parts) == 1:
        tree.children[path_parts[0]] = hash_object
    else:
        if not isinstance(tree.children.get(path_parts[0]), Tree):
            tree.children[path_parts[0]] = Tree()
        insert_hash_object(tree.children[path_parts[0]],
                           hash_object, path_parts[1:])
    tree.update_hash()
