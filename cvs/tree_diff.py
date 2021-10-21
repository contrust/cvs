from cvs.hash_object import Tree, Blob


def get_trees_diff(tree1: Tree, tree2: Tree) -> list:
    left_only = Tree()
    right_only = Tree()
    for name in set(tree1.children.keys()).union(set(tree2.children.keys())):
        if name not in tree1.children:
            right_only.children[name] = tree2.children[name]
        elif name not in tree2.children:
            left_only.children[name] = tree1.children[name]
        else:
            if (tree1.children[name].update_hash() !=
                    tree2.children[name].update_hash()):
                if isinstance(tree1.children[name], Tree) and\
                        isinstance(tree1.children[name], Tree):
                    sub_left_only, sub_right_only = get_trees_diff(
                        tree1.children[name], tree2.children[name])
                    left_only.children[name] = sub_left_only
                    right_only.children[name] = sub_right_only
                else:
                    left_only.children[name] = tree1.children[name]
                    right_only.children[name] = tree2.children[name]
    return [left_only, right_only]


def get_tree_children_names(tree: Tree):
    for child_name, child in tree.children.items():
        if isinstance(child, Blob):
            yield [child_name, child]
        else:
            for sub_child_name, blob in get_tree_children_names(child):
                yield [f'{child_name}/{sub_child_name}', blob]
