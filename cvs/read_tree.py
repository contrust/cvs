from cvs.hash_object import Tree, Blob
from cvs.config import trees_path, blobs_path
import re

TREE_LINE_REGEX = re.compile(r'(?P<type>(Blob|Tree)) '
                             r'(?P<hash>\w{40}) '
                             r'(?P<name>.+)')


def read_tree(tree_hash: str) -> Tree:
    with open(str(trees_path / tree_hash)) as tree_file:
        tree = Tree()
        for line in tree_file:
            match = TREE_LINE_REGEX.match(line.strip())
            if match.group('type') == 'Blob':
                child_blob = Blob(data=(blobs_path / match.group('hash'))
                                  .read_bytes())
                tree.children[match.group('name')] = child_blob
            elif match.group('type') == 'Tree':
                child_tree = read_tree(match.group('hash'))
                tree.children[match.group('name')] = child_tree
        return tree
