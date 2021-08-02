from abc import ABC, abstractmethod
from hashlib import sha1
from dataclasses import dataclass


def get_hash(data: bytes) -> str:
    return sha1(bytes(data)).hexdigest()


@dataclass
class HashObject(ABC):
    def __init__(self, name=None, folder_name=None):
        self.name = name
        self.folder_name = folder_name

    @abstractmethod
    def __bytes__(self) -> bytes:
        """Get byte representation of object"""

    def hash(self) -> str:
        """Save byte content of object in cvs objects directory and
         return it's hash"""
        content = bytes(self)
        content_hash = get_hash(content)
        with open(f'.cvs/objects/{self.folder_name}/{content_hash}', mode='wb') as output_file:
            output_file.write(content)
        return content_hash


class Tree(HashObject):
    def __init__(self, name=None):
        super().__init__(name, "trees")
        self.children = []

    def __bytes__(self) -> bytes:
        return b'\n'.join([f'{child.__class__.__name__} '
                           f'{child.hash()} '
                           f'{child.name}'.encode('utf-8')
                           for child in sorted(self.children,
                                               key=lambda x: x.name)])


class Blob(HashObject):
    def __init__(self, data: bytes, name=None):
        super().__init__(name, "blobs")
        self.data = data

    def __bytes__(self) -> bytes:
        return bytes(self.data)

