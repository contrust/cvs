from cvs.branch import is_branch_exist, get_branch_content
from cvs.clean_directory import clean_directory
from cvs.commit import get_commit_tree_hash, is_commit_exist
from cvs.config import head_path, index_path
from cvs.read_tree import read_tree
from cvs.tag import is_tag_exist, get_tag_commit_hash
from cvs.unload_tree import unload_tree


def checkout(ref_name):
    if head_path.read_text() == ref_name:
        print(f'You are already on {ref_name}.')
        return
    if is_commit_exist(ref_name):
        commit_hash = ref_name
        head_path.write_text(commit_hash)
    elif is_tag_exist(ref_name):
        commit_hash = get_tag_commit_hash(ref_name)
        head_path.write_text(commit_hash)
    elif is_branch_exist(ref_name):
        commit_hash = get_branch_content(ref_name)
        head_path.write_text(ref_name)
    else:
        print('There is no commit, tag or branch with such name.')
        return
    clean_directory('.')
    tree_hash = get_commit_tree_hash(commit_hash)
    unload_tree(read_tree(tree_hash), '.')
    index_path.write_text(tree_hash)
    print(f'Successful checkout to {ref_name}')
