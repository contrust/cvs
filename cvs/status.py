from cvs.branch import is_branch_exist
from cvs.commit import is_commit_exist
from cvs.config import head_path


def status():
    try:
        head_content = head_path.read_text()
    except FileNotFoundError:
        print('Head file does not exist.')
        return
    if is_branch_exist(head_content):
        print(f'On {head_content} branch')
    elif is_commit_exist(head_content):
        print(f'On {head_content} commit')
    else:
        print('The head file stores not appropriate data.')
