from cvs.modify import add, rm
from cvs.config import *
from cvs.read_tree import read_tree


def test_only_given_path_is_removed(create_two_files):
    add('.')
    rm('test1.txt')
    index_content = index_path.read_text()
    index_tree = read_tree(index_content)
    assert 'test2.txt' in index_tree.children
    assert len(index_tree.children) == 1


def test_can_not_remove_object_outside_working_directory(capsys):
    rm('../test_rm.py')
    assert (capsys.readouterr().out ==
            'Can not modify object '
            'outside of the working directory.\n')


def test_all_files_is_removed_if_remove_current_working_directory(
        create_two_files):
    add('.')
    rm('.')
    index_content = index_path.read_text()
    tree = read_tree(index_content)
    assert len(tree.children) == 0


def test_can_not_remove_not_existing_object(capsys):
    rm('not_existing.txt')
    assert (capsys.readouterr().out ==
            "Can not remove not_existing.txt "
            "because there is no such path in index.\n")


def test_print_successfully_removed_if_remove_existed_object(capsys,
                                                             create_two_files):
    add('.')
    capsys.readouterr()
    rm('test1.txt')
    assert capsys.readouterr().out == f'Successfully removed test1.txt\n'
