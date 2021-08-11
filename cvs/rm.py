import os
from pathlib import Path

from cvs.config import index_path
from cvs.hash_object import Tree
from cvs.read_tree import read_tree


def remove_tree_object(tree, path_parts) -> None:
    if not path_parts:
        tree.children = {}
    elif len(path_parts) == 1:
        del tree.children[path_parts[0]]
    else:
        remove_tree_object(tree.children[path_parts[0]], path_parts[1:])
    tree.update_hash()


def rm(object_path: str) -> None:
    object_path = os.path.relpath(object_path)
    if object_path.startswith('..'):
        print('You are trying to remove object '
              'outside of the working directory.')
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
        remove_tree_object(index_tree, Path(object_path).parts)
    except (KeyError, AttributeError):
        print(f'There is no directory or file in '
              f'index with {object_path} path')
        return
    except FileNotFoundError:
        print('Trees folder does not exist.')
        return
    try:
        index_path.write_text(index_tree.content_hash)
    except FileNotFoundError:
        print('Index file does not exist.')
        return
    print(f'Successfully removed {object_path}')
