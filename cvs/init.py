from cvs.config import *


def init():
    if cvs_directory_path.exists():
        print('CVS is already inited.')
        return
    cvs_directory_path.mkdir()
    objects_path.mkdir()
    blobs_path.mkdir()
    trees_path.mkdir()
    commits_path.mkdir()
    refs_path.mkdir()
    tags_path.mkdir()
    tags_refs_path.mkdir()
    heads_refs_path.mkdir()
    index_path.write_bytes(b'')
    head_path.write_bytes(b'main')
    (heads_refs_path / 'main').write_bytes(b'')
    print('CVS inited successfully.')
