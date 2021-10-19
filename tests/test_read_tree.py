from cvs.hash_object import Tree, Blob
from cvs.read_tree import read_tree


def test_read_tree_restores_all_names_and_content():
    tree = Tree()
    blob1 = Blob(data=b'blob one content')
    blob2 = Blob(data=b'blob two content')
    sub_tree = Tree()
    sub_tree.children = {'blob2': blob2}
    tree.children = {'blob1': blob1, 'sub_tree': sub_tree}
    tree_hash = tree.update_hash()
    restored_tree = read_tree(tree_hash)
    assert tree.children == restored_tree.children
    assert isinstance(restored_tree.children['blob1'], Blob)
    assert restored_tree.children['blob1'].data == b'blob one content'
    assert isinstance(restored_tree.children['sub_tree'], Tree)
    assert restored_tree.children['sub_tree'].children == sub_tree.children
    assert isinstance(restored_tree.children['sub_tree'].children['blob2'],
                      Blob)
    assert (restored_tree.children['sub_tree'].children['blob2'].data ==
            b'blob two content')
