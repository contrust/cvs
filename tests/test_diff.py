from unittest.mock import patch

from cvs.commit import commit
from cvs.diff import *
from cvs.modify import add
from cvs.config import repository_path


def true_false_generator(a):
    i = 0
    while True:
        i += 1
        yield bool(i % 2)


def make_two_commits_with_files_with_different_content():
    (repository_path / 'test1.txt').write_text('12345')
    add('test1.txt')
    commit1_hash = commit('')
    (repository_path / 'test1.txt').write_text('1234567890')
    add('test1.txt')
    commit2_hash = commit('')
    return [commit1_hash, commit2_hash]


def test_show_content_difference_if_compare_two_not_binary_files(
        capsys, create_two_files):
    commit1_hash, commit2_hash =\
        make_two_commits_with_files_with_different_content()
    capsys.readouterr()
    diff(commit1_hash, commit2_hash)
    output = capsys.readouterr().out
    assert 'test1.txt' in output
    assert '@@ -1 +1 @@' in output
    assert '-12345' in output
    assert '+1234567890' in output


@patch('cvs.diff.is_binary_string', lambda x: True)
def test_show_size_difference_if_compare_two_binary_files(capsys,
                                                          create_two_files):
    commit1_hash, commit2_hash =\
        make_two_commits_with_files_with_different_content()
    capsys.readouterr()
    diff(commit1_hash, commit2_hash)
    assert (f'{colorize("test1.txt", PINK)} '
            f'binary file size was changed from 5 to 10 bytes\n\n' ==
            capsys.readouterr().out)


@patch('cvs.diff.is_binary_string', true_false_generator)
def test_show_size_difference_if_compare_binary_and_not_binary_files(
        capsys, create_two_files):
    commit1_hash, commit2_hash =\
        make_two_commits_with_files_with_different_content()
    capsys.readouterr()
    diff(commit1_hash, commit2_hash)
    assert (f'{colorize("test1.txt", PINK)} '
            f'binary file size was changed from 5 to 10 bytes\n\n' ==
            capsys.readouterr().out)
