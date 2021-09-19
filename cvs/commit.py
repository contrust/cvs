import os.path
import re

from cvs.branch import is_branch_exist
from cvs.config import commits_path, heads_refs_path, index_path, head_path
from cvs.hash_object import Commit

COMMIT_REGEX = re.compile(r'^Tree: (?P<tree_hash>\w{40})\n'
                          r'Parent: (?P<parent_hash>(\w{40})?)\n'
                          r'Date: (?P<date>[^\n]*)\n\n'
                          r'(?P<message>.*)$', re.DOTALL | re.MULTILINE)


def commit(message: str) -> None:
    try:
        index_content = index_path.read_text()
    except FileNotFoundError:
        print('Index file does not exist.')
        return
    if not index_content:
        print('Can not commit empty repository.')
        return
    try:
        commit_hash = Commit(message).update_hash()
    except FileNotFoundError:
        print('Commit folder does not exist.')
        return
    try:
        branch_name = head_path.read_text()
    except FileNotFoundError:
        print('Head file does not exist.')
        return
    if is_branch_exist(branch_name) and branch_name:
        try:
            (heads_refs_path / branch_name).write_text(commit_hash)
        except FileNotFoundError:
            print('Branch folder does not exist.')
            return
    else:
        try:
            head_path.write_text(commit_hash)
        except FileNotFoundError:
            print('Head file does not exist.')
            return
    print(f'Successful commit {commit_hash}')


def commit_list():
    try:
        commits_names = os.listdir(str(commits_path))
    except FileNotFoundError:
        print('Commit folder does not exist.')
        return
    if commits_names:
        for commit_name in commits_names:
            print(commit_name)
    else:
        print("There are no commits at the moment.")


def is_commit_exist(commit_hash: str) -> bool:
    return (commits_path / commit_hash).exists()


def get_commit_tree_hash(commit_hash: str) -> str:
    commit_text = (commits_path / commit_hash).read_text()
    commit_match = COMMIT_REGEX.match(commit_text)
    tree_hash = commit_match.group('tree_hash')
    return tree_hash


def get_commit_parent_hash(commit_hash: str) -> str:
    commit_text = (commits_path / commit_hash).read_text()
    commit_match = COMMIT_REGEX.match(commit_text)
    parent_hash = commit_match.group('parent_hash')
    return parent_hash
