import os
from cvs.config import *
from cvs.branch import *
from cvs.modify import add
from cvs.commit import commit
from cvs.checkout import checkout


def test_can_not_create_branch_if_there_are_not_any_commits(capsys):
    create_branch('test')
    assert (capsys.readouterr().out ==
            'Head file does not point to any commit or branch.\n')


def test_branch_name_in_branch_folder_after_creation(make_test1_commit):
    assert 'test' not in os.listdir(str(heads_refs_path))
    create_branch('test')
    assert 'test' in os.listdir(str(heads_refs_path))


def test_branch_file_contains_commit_hash(create_two_files):
    add('test1.txt')
    commit_hash = commit('')
    create_branch('test')
    branch_file_content = (heads_refs_path / 'test').read_text()
    assert branch_file_content == commit_hash


def test_branch_updates_commit_hash_if_checkout(make_test1_commit):
    create_branch('test')
    checkout('test')
    (repository_path / 'test2.txt').write_text('')
    add('test2.txt')
    commit_hash = commit('')
    branch_file_content = (heads_refs_path / 'test').read_text()
    assert branch_file_content == commit_hash


def test_can_not_create_branch_with_already_existed_name(capsys,
                                                         make_test1_commit):
    create_branch('test')
    capsys.readouterr()
    create_branch('test')
    assert capsys.readouterr().out == "The branch test already exists.\n"


def test_print_successfully_created_after_branch_creation(capsys,
                                                          make_test1_commit):
    capsys.readouterr()
    create_branch('test')
    assert (capsys.readouterr().out ==
            'The branch test was successfully created.\n')
