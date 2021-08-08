from cvs.branch import is_branch_exist, get_branch_content
from cvs.clean_directory import clean_directory
from cvs.commit import get_commit_tree_hash, is_commit_exist
from cvs.config import head_path, index_path
from cvs.read_tree import read_tree
from cvs.tag import is_tag_exist, get_tag_commit_hash
from cvs.unload_tree import unload_tree


def checkout(ref_name: str) -> None:
    try:
        head_content = head_path.read_text()
    except FileNotFoundError:
        print('Head file does not exist.')
        return
    if head_content == ref_name:
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
    try:
        tree_hash = get_commit_tree_hash(commit_hash)
    except AttributeError:
        print(f'{commit_hash} file does not match the format.')
        return
    try:
        tree = read_tree(tree_hash)
    except (FileNotFoundError, AttributeError):
        print(f'Error occurred while reading tree {tree_hash}')
        return
    clean_directory('.')
    unload_tree(tree, '.')
    try:
        index_path.write_text(tree_hash)
    except FileNotFoundError:
        print('Index file does not exist.')
        return
    print(f'Successful checkout to {ref_name}')
