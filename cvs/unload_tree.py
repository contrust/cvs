import os
from pathlib import Path

from cvs.hash_object import Tree


def unload_tree(tree: Tree, tree_path: str):
    path = Path(tree_path)
    if not path.exists():
        path.mkdir()
    for child_name, child in tree.children.items():
        if child.__class__.__name__ == "Blob":
            with open(os.path.join(tree_path, child_name),
                      mode="wb") as blob_file:
                blob_file.write(bytes(child))
        elif child.__class__.__name__ == "Tree":
            unload_tree(child, os.path.join(tree_path, child_name))
