from cvs.hash_object import Commit
from cvs.config import head_path


def commit(message: str) -> None:
    commit_hash = Commit(message).hash()
    with open(str(head_path), mode='w') as head_file:
        head_file.write(commit_hash)