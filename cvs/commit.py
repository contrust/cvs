import os.path

from cvs.branch import is_branch_exist
from cvs.config import commits_path, heads_refs_path
from cvs.hash_object import Commit
from cvs.head import write_head, read_head
import re

from cvs.index import read_index

COMMIT_REGEX = re.compile(r'^Tree: (?P<tree_hash>\w{40})\n'
                          r'Parent: (?P<parent_hash>(\w{40})?)\n'
                          r'Date: (?P<date>[^\n]*)\n\n'
                          r'(?P<message>.*)$', re.DOTALL | re.MULTILINE)


def commit(message: str) -> None:
    if not read_index():
        print('Can not commit empty repository.')
        return
    commit_hash = Commit(message).hash()
    if (is_branch_exist(branch_name := read_head()) or
            branch_name == 'main' and not os.listdir(str(heads_refs_path))):
        with open(str(heads_refs_path / branch_name), mode='w') as branch_file:
            branch_file.write(commit_hash)
    else:
        write_head(commit_hash)
    print(f'Successful commit {commit_hash}')


def commit_list():
    commits_names = os.listdir(str(commits_path))
    if commits_names:
        for commit_name in commits_names:
            print(commit_name)
    else:
        print("There are no commits at the moment.")


def is_commit_exist(commit_hash: str) -> bool:
    return os.path.exists(str(commits_path / commit_hash))


def get_commit_tree_hash(commit_hash: str) -> str:
    with open(str(commits_path / commit_hash)) as commit_file:
        commit_match = COMMIT_REGEX.match(commit_file.read())
        return commit_match.group('tree_hash')


def get_commit_parent_hash(commit_hash: str) -> str:
    with open(str(commits_path / commit_hash)) as commit_file:
        commit_match = COMMIT_REGEX.match(commit_file.read())
        return commit_match.group('parent_hash')
