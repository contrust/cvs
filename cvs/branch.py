import os.path
from cvs.config import heads_refs_path, head_path, commits_path


def is_branch_exist(branch_name: str) -> bool:
    return (heads_refs_path / branch_name).exists()


def create_branch(name: str):
    if is_branch_exist(name):
        print(f'The branch {name} already exists.')
        return
    try:
        head_content = head_path.read_text()
    except FileNotFoundError:
        print('Head file does not exist.')
        return
    commit_hash = head_content
    if is_branch_exist(head_content) and head_content:
        try:
            commit_hash = (heads_refs_path / head_content).read_text()
        except FileNotFoundError:
            print('Branch folder does not exist.')
            return
    if (commits_path / commit_hash).exists() and commit_hash:
        try:
            (heads_refs_path / name).write_text(commit_hash)
        except FileNotFoundError:
            print('Branch folder does not exist.')
            return
    else:
        print('Head file does not point to any commit or branch.')
        return
    print(f'The branch {name} was successfully created.')


def branch_list():
    try:
        branch_names = os.listdir(str(heads_refs_path))
    except FileNotFoundError:
        print('Branch folder does not exist.')
        return
    if branch_names:
        for branch_name in branch_names:
            print(branch_name)
    else:
        print("There are no branches at the moment.")
