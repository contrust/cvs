from cvs.config import *
from cvs.hash_object import Blob, Tree


def test_tree_file_contains_blob_hash(create_two_files):
    tree = Tree()
    blob = Blob(data=b'blab')
    blob_hash = blob.update_hash()
    tree.children['test1.txt'] = blob
    tree_hash = tree.update_hash()
    tree_file_content = (trees_path / tree_hash).read_text()
    assert blob_hash in tree_file_content
