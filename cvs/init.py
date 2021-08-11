from cvs.config import cvs_directory_path, objects_path, blobs_path,\
    trees_path, commits_path, refs_path, tags_path, tags_refs_path,\
    heads_refs_path, index_path, head_path


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
    index_path.write_text('')
    head_path.write_text('main')
    (heads_refs_path / 'main').write_text('')
    print('CVS inited successfully.')
