from cvs.hash_object import Tree, Blob
from cvs.config import trees_path, blobs_path


def read_tree(tree_hash: str, tree_name: str = None) -> Tree:
    tree = Tree(tree_name)
    with open(str(trees_path / tree_hash)) as tree_file:
        for line in tree_file:
            child_type, child_hash, child_name = line.strip().split()
            if child_type == 'Blob':
                with open(str(blobs_path / child_hash), mode='rb') as blob_file:
                    tree.children.append(Blob(blob_file.read(), child_name))
            elif child_type == 'Tree':
                tree.children.append(read_tree(child_hash, child_name))
    return tree


if __name__ == '__main__':
    pass
