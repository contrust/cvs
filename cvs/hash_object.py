from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha1

from cvs.branch import is_branch_exist, get_branch_content
from cvs.config import objects_path, head_path, index_path


def get_hash(data: bytes) -> str:
    return sha1(bytes(data)).hexdigest()


@dataclass
class HashObject(ABC):
    def __init__(self, folder_name=None):
        self.folder_name = folder_name

    @abstractmethod
    def __bytes__(self) -> bytes:
        """Get byte representation of object"""

    def hash(self) -> str:
        """Save byte content of object in cvs objects directory and
         return it's hash"""
        content = bytes(self)
        content_hash = get_hash(content)
        with open(str(objects_path / self.folder_name / content_hash),
                  mode='wb') as output_file:
            output_file.write(content)
        return content_hash


class Tree(HashObject):
    def __init__(self, name=None):
        super().__init__("trees")
        self.name = name
        self.children = []

    def __bytes__(self) -> bytes:
        return b'\n'.join([f'{child.__class__.__name__} '
                           f'{child.hash()} '
                           f'{child.name}'.encode('utf-8')
                           for child in sorted(self.children,
                                               key=lambda x: x.name)])


class Blob(HashObject):
    def __init__(self, data: bytes, name=None):
        super().__init__("blobs")
        self.name = name
        self.data = data

    def __bytes__(self) -> bytes:
        return bytes(self.data)


class Commit(HashObject):
    def __init__(self, message: str):
        super().__init__("commits")
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
        super().__init__("tags")
        self.message = message
        self.time = datetime.now(timezone.utc).strftime("%d/%b/%Y:%H:%M:%S %z")

    def __bytes__(self):
        head_content = head_path.read_text()
        commit_hash = (get_branch_content(head_content)
                       if is_branch_exist(head_content) else head_content)
        return f'Commit: {commit_hash}\n' \
               f'Date: {self.time}\n\n' \
               f'{self.message}'.encode('utf-8')
