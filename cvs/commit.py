import os.path
import re

from cvs.branch import is_branch_exist
from cvs.config import commits_path, heads_refs_path, index_path, head_path
from cvs.hash_object import Commit

COMMIT_REGEX = re.compile(r'^Tree: (?P<tree_hash>\w{40})\n'
                          r'Parent: (?P<parent_hash>(\w{40})?)\n'
                          r'Date: (?P<date>[^\n]*)\n\n'
                          r'(?P<message>.*)$', re.DOTALL | re.MULTILINE)


def commit(message: str) -> str:
    head_content = head_path.read_text()
    if not is_commit_exist(head_content):
        if is_branch_exist(head_content):
            head_content = (heads_refs_path / head_content).read_text()
        else:
            print('Head points to not existing branch or commit.')
            return
    try:
        index_content = index_path.read_text()
    except FileNotFoundError:
        print('Index file does not exist.')
        return
    if not index_content:
        print('Can not commit empty repository.')
        return
    if head_content:
        head_tree_hash = get_commit_tree_hash(head_content)
        if head_tree_hash == index_content:
            print('There has not been done any changes after current commit.')
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
    return commit_hash


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


def get_commit_regex_match(commit_hash: str):
    commit_text = (commits_path / commit_hash).read_text()
    commit_match = COMMIT_REGEX.match(commit_text)
    return commit_match


def get_commit_message(commit_hash: str) -> str:
    commit_match = get_commit_regex_match(commit_hash)
    return commit_match.group('message')


def get_commit_tree_hash(commit_hash: str) -> str:
    commit_match = get_commit_regex_match(commit_hash)
    return commit_match.group('tree_hash')


def get_commit_parent_hash(commit_hash: str) -> str:
    commit_match = get_commit_regex_match(commit_hash)
    return commit_match.group('parent_hash')
