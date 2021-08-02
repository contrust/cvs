from pathlib import Path


def init():
    repository_path = Path('.')
    cvs_directory_path = repository_path / '.cvs'
    if cvs_directory_path.exists():
        return
    cvs_directory_path.mkdir()
    objects_path = cvs_directory_path / 'objects'
    blobs_path = objects_path / 'blobs'
    trees_path = objects_path / 'trees'
    commits_path = objects_path / 'commits'
    objects_path.mkdir()
    blobs_path.mkdir()
    trees_path.mkdir()
    commits_path.mkdir()
    index_path = cvs_directory_path / 'index'
    refs_path = cvs_directory_path / 'refs'
    refs_path.mkdir()
    tags_path = refs_path / 'tags'
    tags_path.mkdir()
    heads_path = refs_path / 'heads'
    heads_path.mkdir()
    index_path.write_bytes(b'')
