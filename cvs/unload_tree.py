from pathlib import Path

from cvs.hash_object import Tree, Blob
import os
from cvs.read_tree import read_tree


def unload_tree(tree: Tree, tree_path: str):
    path = Path(tree_path)
    if not path.exists():
        path.mkdir()
    for child in tree.children:
        if child.__class__.__name__ == "Blob":
            with open(os.path.join(tree_path, child.name), mode="wb") as child_file:
                child_file.write(bytes(child))
        elif child.__class__.__name__ == "Tree":
            unload_tree(child, os.path.join(tree_path, child.name))


if __name__ == '__main__':
    unload_tree(read_tree('94cf4418a32ce6631f3f7a33086788514c8b35d6'), './hi')