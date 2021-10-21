from cvs.config import index_path
from cvs.hash_object import Tree
from cvs.read_tree import read_tree


def get_index_tree():
    index_tree_hash = index_path.read_text()
    index_tree = read_tree(index_tree_hash) if index_tree_hash else Tree()
    return index_tree
