from cvs.config import *
from cvs.add import add
from cvs.commit import commit, get_commit_tree_hash


def test_commit_refers_to_index_tree_hash(create_two_files):
    add('test1.txt')
    commit_hash = commit('')
    commit_tree_hash = get_commit_tree_hash(commit_hash)
    index_content = index_path.read_text()
    assert commit_tree_hash == index_content


def test_print_successful_commit_when_added_some_changes(capsys,
                                                         create_two_files):
    (repository_path / 'test.txt').write_text('')
    add('test.txt')
    capsys.readouterr()
    commit_hash = commit('')
    assert capsys.readouterr().out == f'Successful commit {commit_hash}\n'


def test_print_can_not_create_empty_repository(capsys):
    commit('')
    assert capsys.readouterr().out == 'Can not commit empty repository.\n'


def test_can_not_commit_when_no_changes(capsys, create_two_files):
    add('test1.txt')
    commit('')
    capsys.readouterr()
    commit_hash = commit('no changes commit.')
    assert (capsys.readouterr().out ==
            'There has not been done any changes after current commit.\n')
    assert commit_hash is None
