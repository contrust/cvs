import pytest

from cvs.config import *
from cvs.hash_object import Tree, Blob
from cvs.add import add
from cvs.read_tree import read_tree


def test_index_contains_tree_hash(create_two_files):
    add('test1.txt')
    index_content = index_path.read_text()
    tree = Tree()
    tree.children['test1.txt'] = Blob(data=b'')
    tree_hash = tree.update_hash()
    assert index_content == tree_hash


def test_only_given_path_is_added_to_index(create_two_files):
    add('test1.txt')
    index_content = index_path.read_text()
    tree = read_tree(index_content)
    assert 'test1.txt' in tree.children
    assert len(tree.children) == 1


def test_all_files_is_added_if_add_current_working_directory(create_two_files):
    add('.')
    index_content = index_path.read_text()
    tree = read_tree(index_content)
    assert 'test1.txt' in tree.children
    assert 'test2.txt' in tree.children
    assert len(tree.children) == 2


def test_can_not_add_file_outside_of_working_directory(capsys):
    add('../test_add.py')
    assert (capsys.readouterr().out ==
            'Can not add object outside of the working directory.\n')


def test_can_not_add_not_existing_object(capsys):
    add('not_existing.txt')
    assert (capsys.readouterr().out ==
            f'There is no directory or file with not_existing.txt path\n')


def test_print_successfully_updated_if_add_existing_object(capsys,
                                                           create_two_files):
    add('test1.txt')
    assert capsys.readouterr().out == f'Successfully updated test1.txt\n'