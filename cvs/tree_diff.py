import difflib
import os
from pathlib import Path

from cvs.hash_object import Tree, Blob
from cvs.config import cvs_directory_path, repository_path
from cvs.read_tree import read_tree
from cvs.unload_tree import unload_tree


def get_trees_diff(tree1: Tree, tree2: Tree) -> list:
    left_only = Tree()
    right_only = Tree()
    for name in set(tree1.children.keys()).union(set(tree2.children.keys())):
        if name not in tree1.children:
            right_only.children[name] = tree2.children[name]
        elif name not in tree2.children:
            left_only.children[name] = tree1.children[name]
        else:
            if (tree1.children[name].update_hash() !=
                    tree2.children[name].update_hash()):
                if (isinstance(tree1.children[name], Tree) and
                        isinstance(tree1.children[name], Blob) or
                        isinstance(tree1.children[name], Blob)):
                    left_only.children[name] = tree1.children[name]
                    right_only.children[name] = tree2.children[name]
                else:
                    sub_left_only, sub_right_only = get_trees_diff(
                        tree1.children[name], tree2.children[name])
                    left_only.children[name] = sub_left_only
                    right_only.children[name] = sub_right_only
    return [left_only, right_only]


def get_tree_children_names(tree: Tree):
    for child_name, child in tree.children.items():
        if isinstance(child, Blob):
            yield [child_name, child]
        else:
            for sub_child_name, blob in get_tree_children_names(child):
                yield [f'{child_name}/{sub_child_name}', blob]
