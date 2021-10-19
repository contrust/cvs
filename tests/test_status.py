from cvs.config import repository_path

from cvs.rm import rm
from cvs.status import status
from cvs.checkout import checkout
from cvs.branch import create_branch
from cvs.add import add
from cvs.commit import commit


def test_status_shows_head_content(capsys, create_two_files):
    add('test1.txt')
    commit_hash = commit('')
    create_branch('lol')
    checkout('lol')
    capsys.readouterr()
    status()
    assert 'On lol branch' in capsys.readouterr().out
    checkout(commit_hash)
    capsys.readouterr()
    status()
    assert f'On {commit_hash} commit' in capsys.readouterr().out


def test_status_shows_added_files(capsys, create_two_files):
    status()
    assert 'test1.txt' not in capsys.readouterr().out
    add('test1.txt')
    assert 'test1.txt' in capsys.readouterr().out


def test_status_has_no_changed_files_after_commit(capsys, create_two_files):
    status()
    add('.')
    commit('')
    capsys.readouterr()
    status()
    assert 'test1.txt' not in capsys.readouterr().out
    assert 'test2.txt' not in capsys.readouterr().out


def test_status_shows_removed_files(capsys, create_two_files):
    add('.')
    commit('')
    rm('test2.txt')
    capsys.readouterr()
    status()
    assert 'test2.txt' in capsys.readouterr().out


def test_status_shows_changed_files(capsys, create_two_files):
    status()
    add('.')
    commit('')
    (repository_path / 'test1.txt').write_text('sample_text')
    add('test1.txt')
    capsys.readouterr()
    status()
    assert 'test1.txt' in capsys.readouterr().out
