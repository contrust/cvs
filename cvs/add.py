import os
from pathlib import Path

from cvs.create_tree import create_tree
from cvs.hash_object import Blob, Tree, HashObject
from cvs.read_tree import read_tree
from cvs.config import index_path


def add(object_path: str) -> None:
    object_path = os.path.normpath(object_path)
    add_object = None
    if os.path.isfile(object_path):
        with open(object_path, mode='rb') as blob_file:
            add_object = Blob(blob_file.read(), os.path.basename(object_path))
    if os.path.isdir(object_path):
        add_object = create_tree(object_path, os.path.basename(object_path))
    with open(str(index_path)) as head_file:
        index_tree_hash = head_file.read()
    index_tree = read_tree(index_tree_hash) if index_tree_hash else Tree()
    index_tree = insert_hash_object(index_tree, add_object, Path(object_path).parts)
    with open(str(index_path), mode='w') as head_file:
        head_file.write(index_tree.hash())


def insert_hash_object(tree: Tree, hash_object: HashObject, path_parts) -> Tree:
    if len(path_parts) == 0:
        tree = hash_object
    else:
        child_with_same_name = None
        for child in tree.children[:]:
            if child.name == path_parts[0]:
                child_with_same_name = child
        if len(path_parts) == 1:
            if child_with_same_name:
                tree.children.remove(child_with_same_name)
            if hash_object:
                tree.children.append(hash_object)
        else:
            child_tree = None
            if child_with_same_name and child_with_same_name.__class__.__name__ == 'Tree':
                child_tree = child_with_same_name
            elif hash_object:
                child_tree = Tree(path_parts[0])
                tree.children.append(child_tree)
            if child_tree:
                insert_hash_object(child_tree, hash_object, path_parts[1:])
    tree.hash()
    return tree
