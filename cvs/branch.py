from cvs.config import heads_refs_path
from cvs.head import read_head
import os.path


def create_branch(name: str):
    if is_branch_exist(name):
        print('The branch with such name already exists.')
        return
    with open(str(heads_refs_path / name), mode='w') as branch_file:
        branch_file.write(read_head())
        print(f'The branch {name} was successfully created.')


def branch_list():
    branch_names = os.listdir(str(heads_refs_path))
    if branch_names:
        for branch_name in branch_names:
            print(branch_name)
    else:
        print("There are no branches at the moment.")


def is_branch_exist(branch_name: str) -> bool:
    return os.path.exists(str(heads_refs_path / branch_name))


def get_branch_content(branch_name: str) -> str:
    with open(str(heads_refs_path / branch_name)) as branch_file:
        branch_content = branch_file.read()
        return branch_content
