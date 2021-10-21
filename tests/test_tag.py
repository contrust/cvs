from cvs.tag import *
from cvs.config import tags_path, tags_refs_path
from cvs.modify import add
from cvs.commit import commit


def test_can_not_tag_if_there_are_no_any_commits(capsys):
    tag('elo', 'bro')
    assert (capsys.readouterr().out ==
            'Branch main does not attached to any existing commit.\n')


def test_print_successfully_created_tag_if_head_points_to_existed_commit(
        capsys, make_test1_commit
):
    capsys.readouterr()
    tag('elo', 'bro')
    assert (capsys.readouterr().out ==
            'The tag elo was successfully created.\n')


def test_can_not_create_tag_with_already_existing_name(capsys,
                                                       make_test1_commit):
    tag('elo', 'bro')
    capsys.readouterr()
    tag('elo', 'nebro')
    assert capsys.readouterr().out == 'The tag elo already exists.\n'


def test_tag_hash_file_is_created_after_tagging(make_test1_commit):
    tag_hash = tag('elo', 'bro')
    assert (tags_path / tag_hash).exists()


def test_tag_name_file_is_created_after_tagging(make_test1_commit):
    tag('elo', 'bro')
    assert (tags_refs_path / 'elo').exists()


def test_tag_name_file_contains_tree_hash(make_test1_commit):
    tag_hash = tag('elo', 'bro')
    tag_name_file_content = (tags_refs_path / 'elo').read_text()
    assert tag_hash == tag_name_file_content


def test_tag_file_content_matches_regex(make_test1_commit):
    tag_hash = tag('elo', 'bro')
    tag_file_content = (tags_path / tag_hash).read_text()
    assert TAG_REGEX.match(tag_file_content) is not None


def test_tag_file_contains_message(make_test1_commit):
    tag_hash = tag('elo', 'my bro is your bro')
    tag_file_content = (tags_path / tag_hash).read_text()
    assert 'my bro is your bro' in tag_file_content


def test_tag_file_contains_commit_hash(create_two_files):
    add('test1.txt')
    commit_hash = commit('')
    tag_hash = tag('elo', 'bro')
    tag_content = (tags_path / tag_hash).read_text()
    assert commit_hash in tag_content
