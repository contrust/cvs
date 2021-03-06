from cvs.config import *
from cvs.init import init


def test_files_were_created_after_init():
    assert repository_path.exists()
    assert cvs_directory_path.exists()
    assert objects_path.exists()
    assert blobs_path.exists()
    assert trees_path.exists()
    assert tags_path.exists()
    assert commits_path.exists()
    assert index_path.exists()
    assert head_path.exists()
    assert refs_path.exists()
    assert tags_refs_path.exists()
    assert heads_refs_path.exists()


def test_can_not_init_if_cvs_is_already_inited(capsys):
    init()
    assert capsys.readouterr().out == 'CVS is already inited.\n'
