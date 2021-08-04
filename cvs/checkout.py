import os.path

from cvs.branch import is_branch_exist, get_branch_commit_hash
from cvs.clean_directory import clean_directory
from cvs.commit import get_commit_tree_hash, is_commit_exist
from cvs.head import write_head
from cvs.tag import is_tag_exist, get_tag_commit_hash
from cvs.unload_tree import unload_tree
from cvs.read_tree import read_tree


def checkout(ref_name):
    if is_commit_exist(ref_name):
        commit_hash = ref_name
        write_head(commit_hash)
    elif is_tag_exist(ref_name):
        commit_hash = get_tag_commit_hash(ref_name)
        write_head(commit_hash)
    elif is_branch_exist(ref_name):
        commit_hash = get_branch_commit_hash(ref_name)
        write_head(ref_name)
    else:
        print('There is no commit, tag or branch with such name.')
        return
    clean_directory('.')
    tree_hash = get_commit_tree_hash(commit_hash)
    unload_tree(read_tree(tree_hash), '.')
    print(f'Successful checkout to {ref_name}')
