import os
import re

from cvs.branch import get_branch_content
from cvs.config import refs_path, tags_refs_path, tags_path, head_path
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
    try:
        branch_content = get_branch_content('main')
    except FileNotFoundError:
        print('Branch folder does not exist.')
        return
    if head_content == 'main' and not branch_content:
        print('There is no commit to attach.')
        return
    tag_hash = Tag(message).update_hash()
    try:
        (refs_path / "tags" / name).write_text(tag_hash)
    except FileNotFoundError:
        print('Tags folder does not exist.')
        return
    print(f'The tag {name} was successfully created.')


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
    tag_hash = (tags_refs_path / tag_name).read_text()
    tag_text = (tags_path / tag_hash).read_text()
    tag_match = TAG_REGEX.match(tag_text)
    return tag_match.group('commit_hash')
