from pathlib import Path

from cvs.hash_object import Tree, Blob


def unload_tree(tree: Tree, path: Path):
    if not path.exists():
        path.mkdir()
    for child_name, child in tree.children.items():
        if isinstance(child, Blob):
            (path / child_name).write_bytes(bytes(child))
        elif isinstance(child, Tree):
            unload_tree(child, (path / child_name))
