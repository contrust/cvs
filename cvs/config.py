from pathlib import Path

repository_path = Path('.').absolute()
cvs_directory_path = repository_path / '.cvs'
objects_path = cvs_directory_path / 'objects'
blobs_path = objects_path / 'blobs'
trees_path = objects_path / 'trees'
commits_path = objects_path / 'commits'
index_path = cvs_directory_path / 'index'
head_path = cvs_directory_path / 'HEAD'
refs_path = cvs_directory_path / 'refs'
tags_path = refs_path / 'tags'
heads_path = refs_path / 'heads'
