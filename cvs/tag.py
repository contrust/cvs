import os

from cvs.branch import get_branch_content
from cvs.config import refs_path, tags_refs_path, tags_path
from cvs.hash_object import Tag
import re

from cvs.head import read_head

TAG_REGEX = re.compile(r'^Commit: (?P<commit_hash>\w{40})\n'
                       r'Date: (?P<date>[^\n]*)\n\n'
                       r'(?P<message>.*)$', re.DOTALL | re.MULTILINE)


def tag(name: str, message: str) -> None:
    if is_tag_exist(name):
        print('The tag with such name already exists.')
        return
    elif read_head() == 'main' and not get_branch_content('main'):
        print('There is no commit to attach.')
        return
    tag_hash = Tag(message).hash()
    with open(str(refs_path / "tags" / name), mode='w') as head_file:
        head_file.write(tag_hash)


def tag_list():
    tags_names = os.listdir(str(tags_refs_path))
    if tags_names:
        for tag_name in tags_names:
            print(tag_name)
    else:
        print("There are no tags at the moment.")


def is_tag_exist(tag_name: str) -> bool:
    return os.path.exists(str(tags_refs_path / tag_name))


def get_tag_commit_hash(tag_name: str) -> str:
    with open(str(tags_refs_path / tag_name)) as tag_hash_file:
        tag_hash = tag_hash_file.read()
        with open(str(tags_path / tag_hash)) as tag_file:
            tag_match = TAG_REGEX.match(tag_file.read())
            return tag_match.group('commit_hash')
