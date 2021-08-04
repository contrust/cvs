from cvs.branch import get_branch_content, is_branch_exist
from cvs.commit import get_commit_parent_hash
from cvs.config import commits_path
from cvs.head import read_head


def log():
    head_content = read_head()
    commit_hash = (get_branch_content(head_content)
                   if is_branch_exist(head_content) else head_content)
    while commit_hash:
        with open(str(commits_path / commit_hash)) as commit_file:
            commit_file.readline()
            commit_file.readline()
            print('\033[91m' + f'commit {commit_hash}' + '\033[0m')
            print(commit_file.read())
            print()
        commit_hash = get_commit_parent_hash(commit_hash)