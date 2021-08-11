from pathlib import Path

from cvs.branch import is_branch_exist
from cvs.clean_directory import clean_directory
from cvs.commit import get_commit_tree_hash, is_commit_exist
from cvs.config import head_path, index_path, heads_refs_path
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
        try:
            head_path.write_text(commit_hash)
        except FileNotFoundError:
            print('Head file does not exist.')
            return
    elif is_tag_exist(ref_name):
        try:
            commit_hash = get_tag_commit_hash(ref_name)
        except (FileNotFoundError, AttributeError):
            print("Can not read commit hash of tag.")
            return
        try:
            head_path.write_text(commit_hash)
        except FileNotFoundError:
            print('Head file does not exist.')
            return
    elif is_branch_exist(ref_name):
        try:
            commit_hash = (heads_refs_path / ref_name).read_text()
        except FileNotFoundError:
            print(f'Branch {ref_name} does not exist.')
            return
        try:
            head_path.write_text(ref_name)
        except FileNotFoundError:
            print('Head file does not exist.')
            return
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
    try:
        clean_directory('.')
    except FileNotFoundError:
        print('Working directory was modified while cleaning.')
        return
    try:
        unload_tree(tree, Path('.'))
    except FileNotFoundError:
        print('Working directory was modified while unloading tree.')
        return
    try:
        index_path.write_text(tree_hash)
    except FileNotFoundError:
        print('Index file does not exist.')
        return
    print(f'Successful checkout to {ref_name}')
