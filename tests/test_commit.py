from cvs.commit import *
from cvs.modify import add


def test_commit_file_is_created_after_committing(create_two_files):
    add('test1.txt')
    commit_hash = commit('')
    assert is_commit_exist(commit_hash)


def test_commit_file_content_matches_regex(create_two_files,
                                           create_dir_with_two_files):
    add('.')
    commit_hash = commit('')
    commit_file_content = (commits_path / commit_hash).read_text()
    assert COMMIT_REGEX.match(commit_file_content) is not None


def test_commit_refers_to_index_tree_hash(create_two_files):
    add('test1.txt')
    commit_hash = commit('')
    commit_tree_hash = get_commit_tree_hash(commit_hash)
    index_content = index_path.read_text()
    assert commit_tree_hash == index_content


def test_print_successful_commit_when_added_some_changes(capsys,
                                                         create_two_files):
    add('test1.txt')
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


def test_commit_file_contain_given_message(create_two_files):
    add('test1.txt')
    commit_hash = commit('test message')
    message = get_commit_message(commit_hash)
    assert message == 'test message'


def test_commit_changes_main_branch_content(create_two_files):
    add('test1.txt')
    main_content1 = (heads_refs_path / 'main').read_text()
    commit_hash = commit('')
    main_content2 = (heads_refs_path / 'main').read_text()
    assert main_content1 != main_content2
    assert main_content2 == commit_hash
