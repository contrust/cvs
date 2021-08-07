from cvs.hash_object import Tree, Blob
from cvs.config import trees_path, blobs_path


def read_tree(tree_hash: str) -> Tree:
    with open(str(trees_path / tree_hash)) as tree_file:
        tree = Tree()
        for line in tree_file:
            child_type, child_hash, child_name = line.strip().split()
            if child_type == 'Blob':
                child_blob = Blob((blobs_path / child_hash).read_bytes())
                tree.children[child_name] = child_blob
            elif child_type == 'Tree':
                child_tree = read_tree(child_hash)
                tree.children[child_name] = child_tree
        return tree
