from cvs.hash_object import Tree, Blob


def parse_tree(tree_hash: str, tree_name: str = None) -> Tree:
    tree = Tree(tree_name)
    with open(f'.cvs/objects/trees/{tree_hash}') as tree_file:
        for line in tree_file:
            child_type, child_hash, child_name = line.strip().split()
            if child_type == 'Blob':
                with open(f'.cvs/objects/blobs/{child_hash}', mode='rb') as blob_file:
                    tree.children.append(Blob(blob_file.read(), child_name))
            elif child_type == 'Tree':
                tree.children.append(parse_tree(child_hash, child_name))
    return tree
