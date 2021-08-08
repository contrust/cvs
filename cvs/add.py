import os
from pathlib import Path

from cvs.config import index_path
from cvs.create_tree import create_tree
from cvs.hash_object import Blob, Tree, HashObject
from cvs.read_tree import read_tree


def add(object_path: str) -> None:
    object_path = os.path.relpath(object_path)
    if object_path.startswith('..'):
        print('You are trying to add object outside of the working directory.')
        return
    add_object = None
    if os.path.isfile(object_path):
        with open(object_path, mode='rb') as blob_file:
            add_object = Blob(blob_file.read())
    elif os.path.isdir(object_path):
        try:
            add_object = create_tree(object_path)
        except FileNotFoundError:
            print('Blobs folder does not exist.')
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
        index_tree = insert_hash_object(index_tree, add_object,
                                        Path(object_path).parts)
    except FileNotFoundError:
        print('Trees folder does not exist.')
        return
    try:
        index_path.write_text(index_tree.content_hash)
    except FileNotFoundError:
        print('Index file does not exist.')
        return
    print(f'Successfully updated {object_path}')


def insert_hash_object(tree: Tree, hash_object: HashObject, path_parts: iter) \
        -> Tree:
    if not path_parts:
        tree = hash_object
    else:
        child_with_same_name = tree.children.get(path_parts[0], None)
        if len(path_parts) == 1:
            if child_with_same_name:
                del tree.children[path_parts[0]]
            if hash_object:
                tree.children[path_parts[0]] = hash_object
        else:
            child_tree = None
            if (child_with_same_name and
                    child_with_same_name.__class__.__name__ == 'Tree'):
                child_tree = child_with_same_name
            elif hash_object:
                child_tree = Tree()
                tree.children[path_parts[0]] = child_tree
            if child_tree:
                insert_hash_object(child_tree, hash_object, path_parts[1:])
    tree.update_hash()
    return tree
