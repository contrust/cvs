import os

import pytest

from cvs.config import *
from cvs.branch import *
from cvs.add import add
from cvs.commit import commit
from cvs.checkout import checkout


def test_head_file_content_changes_to_branch_name_if_checkout_to_branch(
        make_test1_commit):
    create_branch('test')
    checkout('test')
    head_content = head_path.read_text()
    assert head_content == 'test'


def test_head_file_content_changes_to_branch_name_if_checkout_to_commit(
        create_two_files):
    add('test1.txt')
    commit_hash = commit('')
    add('test2.txt')
    commit('')
    checkout(commit_hash)
    head_content = head_path.read_text()
    assert head_content == commit_hash


def test_print_you_are_already_on_if_checkout_to_head_content(
        capsys, make_test1_commit):
    head_content = head_path.read_text()
    capsys.readouterr()
    checkout(head_content)
    assert capsys.readouterr().out == f'You are already on {head_content}.\n'


def test_can_not_checkout_to_not_existing_ref(capsys):
    checkout('not_existing_reference')
    assert (capsys.readouterr().out ==
            'There is no commit, tag or branch '
            'with not_existing_reference name.\n')


def test_repository_files_changes_after_checkout(create_two_files):
    add('test1.txt')
    commit_hash = commit('')
    add('test2.txt')
    commit('')
    checkout(commit_hash)
    listdir = os.listdir('.')
    assert 'test1.txt' in listdir
    assert '.cvs' in listdir
    assert len(listdir) == 2
