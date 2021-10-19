from cvs.unload_tree import unload_tree
from cvs.hash_object import Tree, Blob
from pathlib import Path


def test_files_are_created_after_unloading():
    tree = Tree()
    sub_tree = Tree()
    blob1 = Blob(data=b'blob one content')
    blob2 = Blob(data=b'blob two content')
    sub_tree.children['blob2'] = blob2
    tree.children = {'blob1': blob1, 'sub_tree': sub_tree}
    test_path = Path('./test')
    unload_tree(tree, test_path)
    assert (test_path / 'blob1').exists()
    assert (test_path / 'sub_tree').exists()
    assert (test_path / 'sub_tree' / 'blob2').exists()


def test_files_have_the_same_content_as_tree_blobs_after_unloading():
    tree = Tree()
    blob1 = Blob(data=b'blob one content')
    tree.children['blob1'] = blob1
    test_path = Path('./test')
    unload_tree(tree, test_path)
    blob1_content = (test_path / 'blob1').read_text()
    assert blob1_content == 'blob one content'
