import difflib
import os
from pathlib import Path

from cvs.hash_object import Tree, Blob
from cvs.commit import get_commit_tree_hash
from cvs.config import cvs_directory_path, repository_path
from cvs.read_tree import read_tree
from cvs.unload_tree import unload_tree
from cvs.tree_diff import get_trees_diff, get_tree_children_names


def is_binary_string(string: bytes) -> bool:
    chars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
    return bool(string.translate(None, chars))


def diff(commit_hash1, commit_hash2):
    tree_hash1 = get_commit_tree_hash(commit_hash1)
    tree_hash2 = get_commit_tree_hash(commit_hash2)
    tree1 = read_tree(tree_hash1)
    tree2 = read_tree(tree_hash2)
    left_only, right_only = get_trees_diff(tree1, tree2)
    left_dict = {x: y for x, y in get_tree_children_names(left_only)}
    right_dict = {x: y for x, y in get_tree_children_names(right_only)}
    for name in sorted(list(set(left_dict.keys()).union(set(right_dict.keys())))):
        data1 = left_dict.get(name, Blob(data=b'')).data
        data2 = right_dict.get(name, Blob(data=b'')).data
        if not is_binary_string(data1) and not is_binary_string(data2) and (data1 or data2):
            data1 = data1.decode('utf-8').splitlines()
            data2 = data2.decode('utf-8').splitlines()
            diff_lines = list(difflib.unified_diff(data1, data2, name, name))
            print('\033[35m' + name + '\033[0m')
            for i in diff_lines[2:]:
                print(('\033[32m' if i.startswith('+') else ('\033[31m' if i.startswith('-') else '')) + i + '\033[0m')
            print()
    print(end="")
