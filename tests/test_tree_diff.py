from cvs.hash_object import Tree, Blob
from cvs.tree_diff import get_trees_diff, get_tree_children_names


def test_get_trees_diff_returns_two_trees():
    tree1 = Tree()
    tree2 = Tree()
    left, right = get_trees_diff(tree1, tree2)
    assert isinstance(left, Tree)
    assert isinstance(right, Tree)


def test_left_and_right_dont_contain_blobs_with_the_same_name_and_content():
    tree1 = Tree()
    tree2 = Tree()
    blob1 = Blob(data=b"first")
    tree1.children = {'blob1': blob1}
    tree2.children = {'blob1': blob1}
    left, right = get_trees_diff(tree1, tree2)
    assert 'blob1' not in left.children
    assert 'blob1' not in right.children


def test_left_and_right_contain_blobs_with_same_name_and_different_content():
    tree1 = Tree()
    tree2 = Tree()
    blob1 = Blob(data=b"first")
    blob2 = Blob(data=b"second")
    tree1.children = {'blob1': blob1}
    tree2.children = {'blob1': blob2}
    left, right = get_trees_diff(tree1, tree2)
    assert 'blob1' in left.children and left.children['blob1'] == blob1
    assert 'blob1' in right.children and right.children['blob1'] == blob2


def test_left_and_right_contain_blobs_with_different_name_and_same_content():
    tree1 = Tree()
    tree2 = Tree()
    blob1 = Blob(data=b"first")
    tree1.children = {'blob1': blob1}
    tree2.children = {'blob2': blob1}
    left, right = get_trees_diff(tree1, tree2)
    assert 'blob1' in left.children and left.children['blob1'] == blob1
    assert 'blob2' in right.children and right.children['blob2'] == blob1


def test_left_and_right_contain_blobs_with_differ_name_and_differ_content():
    tree1 = Tree()
    tree2 = Tree()
    blob1 = Blob(data=b"first")
    blob2 = Blob(data=b"second")
    tree1.children = {'blob1': blob1}
    tree2.children = {'blob2': blob2}
    left, right = get_trees_diff(tree1, tree2)
    assert 'blob1' in left.children and left.children['blob1'] == blob1
    assert 'blob2' in right.children and right.children['blob2'] == blob2


def test_left_and_right_contain_blob_and_tree_if_they_have_same_name():
    tree1 = Tree()
    tree2 = Tree()
    blob1 = Blob(data=b"first")
    blob2 = Tree()
    tree1.children = {'blob1': blob1}
    tree2.children = {'blob1': blob2}
    left, right = get_trees_diff(tree1, tree2)
    assert 'blob1' in left.children and left.children['blob1'] == blob1
    assert 'blob1' in right.children and right.children['blob1'] == blob2


def test_left_and_right_contain_diff_of_trees_if_they_have_same_name():
    tree1 = Tree()
    tree2 = Tree()
    sub_tree1 = Tree()
    sub_tree2 = Tree()
    blob1 = Blob(data=b"first")
    blob2 = Blob(data=b"second")
    blob3 = Blob(data=b"third")
    sub_tree1.children = {"sb1": blob1, "sb2": blob2}
    sub_tree2.children = {"sb1": blob1, "sb2": blob3}
    tree1.children = {'b1': sub_tree1}
    tree2.children = {'b1': sub_tree2}
    left, right = get_trees_diff(tree1, tree2)
    assert 'b1' in left.children and isinstance(left.children['b1'], Tree)
    assert 'b1' in right.children and isinstance(right.children['b1'], Tree)
    assert 'sb1' not in left.children['b1'].children
    assert 'sb2' in left.children['b1'].children
    assert 'sb1' not in right.children['b1'].children
    assert 'sb2' in right.children['b1'].children


def test_get_tree_children_names_gives_names_joined_by_slash():
    tree = Tree()
    sub_tree = Tree()
    blob = Blob(data=b'')
    sub_tree.children = {"1": blob, "2": blob}
    tree.children = {"1": blob, "2": blob, "3": blob,
                     "4": sub_tree, "5": sub_tree}
    tree_children_names = set(map(lambda x: x[0],
                                  get_tree_children_names(tree)))
    assert tree_children_names == {"1", "2", "3", "4/1", "4/2", "5/1", "5/2"}
