import os

from cvs.hash_object import Blob, Tree


def create_tree(tree_path: str, tree_name: str = None) -> str:
    tree = Tree(tree_name)
    for children_name in sorted(os.listdir(tree_path)):
        if children_name[0] != '.':
            children_path = os.path.join(tree_path, children_name)
            if os.path.isfile(children_path):
                with open(children_path, mode='rb') as blob_file:
                    children_blob = Blob(blob_file.read(), children_name)
                    tree.children.append(children_blob)
            elif os.path.isdir(children_path):
                children_tree = create_tree(children_path, children_name)
                tree.children.append(children_tree)
    tree.hash()
    return tree
