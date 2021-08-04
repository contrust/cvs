from cvs.config import heads_refs_path
from cvs.head import read_head
import os.path


def create_branch(name: str):
    if is_branch_exist(name):
        print('The branch with such name already exists.')
        return
    with open(str(heads_refs_path / name), mode='w') as branch_file:
        branch_file.write(read_head())
        print(f'The branch "{name}" was successfully created.')


def is_branch_exist(branch_name: str) -> bool:
    return os.path.exists(str(heads_refs_path / branch_name))


def get_branch_commit_hash(branch_name: str) -> str:
    with open(str(heads_refs_path / branch_name)) as commit_file:
        commit_hash = commit_file.read()
        return commit_hash
