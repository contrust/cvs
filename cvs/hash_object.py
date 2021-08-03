from abc import ABC, abstractmethod
from hashlib import sha1
from dataclasses import dataclass
from datetime import datetime, timezone
from cvs.config import objects_path, index_path, head_path


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
        with open(str(objects_path / self.folder_name / content_hash), mode='wb') as output_file:
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
        with open(str(index_path)) as index_file:
            with open(str(head_path)) as head_file:
                parent_hash = head_file.read()
                tree_hash = index_file.read()
                return f'tree {tree_hash}\n' \
                       f'parent {parent_hash}\n' \
                       f'datetime {self.time}\n\n' \
                       f'{self.message}'.encode('utf-8')
