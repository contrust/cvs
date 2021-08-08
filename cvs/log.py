from cvs.branch import get_branch_content, is_branch_exist
from cvs.commit import get_commit_parent_hash
from cvs.config import commits_path, head_path
from cvs.commit import COMMIT_REGEX


def log():
    try:
        head_content = head_path.read_text()
    except FileNotFoundError:
        print('Head file does not exist.')
        return
    try:
        commit_hash = (get_branch_content(head_content)
                       if is_branch_exist(head_content) else head_content)
    except FileNotFoundError:
        print(f'Branch {head_content} does not exist.')
        return
    while commit_hash:
        try:
            commit_text = (commits_path / commit_hash).read_text()
        except FileNotFoundError:
            print(f'Commit {commit_hash} does not exist.')
            return
        commit_match = COMMIT_REGEX.match(commit_text)
        try:
            print('\033[91m' + f'commit {commit_hash}' + '\033[0m\n' +
                  f'Date: {commit_match.group("date")}\n\n'
                  f'{commit_match.group("message")}\n')
            commit_hash = get_commit_parent_hash(commit_hash)
        except AttributeError:
            print(f'{commit_hash} file does not match the commit format.')
            return
