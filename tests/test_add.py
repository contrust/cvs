import pytest

from cvs.config import *
from cvs.hash_object import Tree, Blob
from cvs.add import add


def test_only_given_path_is_added_to_index(create_two_files):
    add('test1.txt')
    index_content = index_path.read_text()
    tree = Tree()
    tree.children['test1.txt'] = Blob(data=b'')
    tree_hash = tree.update_hash()
    assert index_content == tree_hash


def test_all_files_is_added_if_add_current_working_directory(create_two_files):
    add('.')
    index_content = index_path.read_text()
    tree = Tree()
    tree.children['test1.txt'] = Blob(data=b'')
    tree.children['test2.txt'] = Blob(data=b'')
    tree_hash = tree.update_hash()
    assert index_content == tree_hash


def test_can_not_add_file_outside_of_working_directory(capsys):
    add('../test_add.py')
    assert (capsys.readouterr().out ==
            'Can not add object outside of the working directory.\n')


def test_index_contains_tree_hash(create_two_files):
    add('test1.txt')
    index_content = index_path.read_text()
    tree = Tree()
    tree.children['test1.txt'] = Blob(data=b'')
    tree_hash = tree.update_hash()
    assert index_content == tree_hash
