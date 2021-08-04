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
    if not index_path.read_text():
        print('Can not commit empty repository.')
        return
    commit_hash = Commit(message).hash()
    if (is_branch_exist(branch_name := head_path.read_text()) or
            branch_name == 'main' and not os.listdir(str(heads_refs_path))):
        (heads_refs_path / branch_name).write_text(commit_hash)
    else:
        head_path.write_text(commit_hash)
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
    commit_text = (commits_path / commit_hash).read_text()
    commit_match = COMMIT_REGEX.match(commit_text)
    return commit_match.group('tree_hash')


def get_commit_parent_hash(commit_hash: str) -> str:
    commit_text = (commits_path / commit_hash).read_text()
    commit_match = COMMIT_REGEX.match(commit_text)
    return commit_match.group('parent_hash')
