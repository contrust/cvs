import os
import re

from cvs.commit import is_commit_exist
from cvs.config import refs_path, tags_refs_path, tags_path, head_path, \
    heads_refs_path
from cvs.hash_object import Tag

TAG_REGEX = re.compile(r'^Commit: (?P<commit_hash>\w{40})\n'
                       r'Date: (?P<date>[^\n]*)\n\n'
                       r'(?P<message>.*)$', re.DOTALL | re.MULTILINE)


def tag(name: str, message: str) -> None:
    if is_tag_exist(name):
        print(f'The tag {name} already exists.')
        return
    try:
        head_content = head_path.read_text()
    except FileNotFoundError:
        print('Head file does not exist.')
        return
    if not is_commit_exist(head_content):
        try:
            branch_content = (heads_refs_path / head_content).read_text()
        except FileNotFoundError:
            print(f'Branch {head_content} does not exist.')
            return
        if not (branch_content and is_commit_exist(branch_content)):
            print(f'Branch {head_content} does not '
                  f'attached to any existing commit.')
            return
    try:
        tag_hash = Tag(message).update_hash()
    except FileNotFoundError:
        print('Cannot create tag because some files in cvs were modified.')
        return
    try:
        (refs_path / "tags" / name).write_text(tag_hash)
    except FileNotFoundError:
        print('Tags folder does not exist.')
        return
    print(f'The tag {name} was successfully created.')


def tag_list():
    try:
        tags_names = os.listdir(str(tags_refs_path))
    except FileNotFoundError:
        print('Tags folder does not exist.')
        return
    if tags_names:
        for tag_name in tags_names:
            print(tag_name)
    else:
        print("There are no tags at the moment.")


def is_tag_exist(tag_name: str) -> bool:
    return (tags_refs_path / tag_name).exists()


def get_tag_commit_hash(tag_name: str) -> str:
    tag_hash = (tags_refs_path / tag_name).read_text()
    tag_text = (tags_path / tag_hash).read_text()
    tag_match = TAG_REGEX.match(tag_text)
    return tag_match.group('commit_hash')
