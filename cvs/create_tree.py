import os

from cvs.hash_object import Blob, Tree


def create_tree(tree_path: str) -> Tree:
    tree = Tree()
    for child_name in sorted(os.listdir(tree_path)):
        if child_name[0] != '.':
            children_path = os.path.join(tree_path, child_name)
            if os.path.isfile(children_path):
                with open(children_path, mode='rb') as blob_file:
                    child_blob = Blob(blob_file.read())
                    child_blob.update_hash()
                    tree.children[child_name] = child_blob
            elif os.path.isdir(children_path):
                child_tree = create_tree(children_path)
                tree.children[child_name] = child_tree
    tree.update_hash()
    return tree
