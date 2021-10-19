import sys
from cvs.hash_object import Tree
from cvs.read_tree import read_tree
from cvs.branch import is_branch_exist
from cvs.commit import is_commit_exist
from cvs.config import head_path, heads_refs_path, index_path
from cvs.diff import get_trees_diff, get_tree_children_names
from cvs.commit import get_commit_tree_hash


def status():
    try:
        head_content = head_path.read_text()
    except FileNotFoundError:
        print('Head file does not exist.')
        return
    if is_branch_exist(head_content):
        print('\033[34m' + f'On {head_content} branch' + '\033[0m')
        head_content = (heads_refs_path / head_content).read_text()
    elif is_commit_exist(head_content):
        print('\033[34m' + f'On {head_content} commit' + '\033[0m')
    else:
        print('The head file stores not appropriate data.')
        sys.exit(1)
    print('\033[35m' + '\nChanged files:\n' + '\033[0m')
    index_tree_hash = index_path.read_text()
    if not index_tree_hash:
        return
    tree1 = read_tree(index_tree_hash)
    if head_content:
        commit_tree_hash = get_commit_tree_hash(head_content)
        tree2 = read_tree(commit_tree_hash)
    else:
        tree2 = Tree()
    only_index_tree, only_commit_tree = get_trees_diff(tree1, tree2)
    left_dict = {x: y for x, y in get_tree_children_names(only_index_tree)}
    right_dict = {x: y for x, y in get_tree_children_names(only_commit_tree)}
    for name in sorted(list(
            set(left_dict.keys()).union(set(right_dict.keys())))):
        print(name)
