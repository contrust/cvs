from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha1
from pathlib import Path

from cvs.branch import is_branch_exist, get_branch_content
from cvs.config import head_path, index_path, trees_path, \
    blobs_path, commits_path, tags_path


def get_hash(data: bytes) -> str:
    return sha1(bytes(data)).hexdigest()


@dataclass
class HashObject(ABC):
    def __init__(self, folder: Path = None, content_hash: str = None):
        self.folder = folder
        self.content_hash = content_hash

    @abstractmethod
    def __bytes__(self) -> bytes:
        """Get byte representation of object"""

    def update_hash(self) -> str:
        """Save byte content of object in cvs objects directory and
         return it's hash"""
        content = bytes(self)
        self.content_hash = get_hash(content)
        (self.folder / self.content_hash).write_bytes(content)
        return self.content_hash


class Tree(HashObject):
    def __init__(self):
        super().__init__(trees_path)
        self.children = {}

    def __bytes__(self) -> bytes:
        return b'\n'.join([f'{child.__class__.__name__} '
                           f'{child.update_hash()} '
                           f'{child_name}'.encode('utf-8')
                           for child_name, child in sorted(self.children.items())])


class Blob(HashObject):
    def __init__(self, data: bytes):
        super().__init__(blobs_path)
        self.data = data

    def __bytes__(self) -> bytes:
        return bytes(self.data)


class Commit(HashObject):
    def __init__(self, message: str):
        super().__init__(commits_path)
        self.message = message
        self.time = datetime.now(timezone.utc).strftime("%d/%b/%Y:%H:%M:%S %z")

    def __bytes__(self) -> bytes:
        head_content = head_path.read_text()
        parent_hash = (get_branch_content(head_content)
                       if is_branch_exist(head_content) else head_content)
        tree_hash = index_path.read_text()
        return f'Tree: {tree_hash}\n' \
               f'Parent: {parent_hash}\n' \
               f'Date: {self.time}\n\n' \
               f'{self.message}'.encode('utf-8')


class Tag(HashObject):
    def __init__(self, message: str):
        super().__init__(tags_path)
        self.message = message
        self.time = datetime.now(timezone.utc).strftime("%d/%b/%Y:%H:%M:%S %z")

    def __bytes__(self):
        head_content = head_path.read_text()
        commit_hash = (get_branch_content(head_content)
                       if is_branch_exist(head_content) else head_content)
        return f'Commit: {commit_hash}\n' \
               f'Date: {self.time}\n\n' \
               f'{self.message}'.encode('utf-8')
