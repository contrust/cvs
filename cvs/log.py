from cvs.branch import is_branch_exist
from cvs.color import colorize, PINK, BLUE, RED
from cvs.commit import get_commit_parent_hash
from cvs.config import commits_path, head_path, heads_refs_path
from cvs.commit import COMMIT_REGEX, get_commit_tree_hash
from cvs.read_tree import read_tree
from cvs.diff import get_trees_diff, get_tree_children_names


def log():
    try:
        head_content = head_path.read_text()
    except FileNotFoundError:
        print('Head file does not exist.')
        return
    try:
        new_commit_hash = ((heads_refs_path / head_content).read_text()
                           if is_branch_exist(head_content) else head_content)
    except FileNotFoundError:
        print(f'Branch {head_content} does not exist.')
        return
    while new_commit_hash:
        try:
            commit_text = (commits_path / new_commit_hash).read_text()
        except FileNotFoundError:
            print(f'Commit {new_commit_hash} does not exist.')
            return
        commit_match = COMMIT_REGEX.match(commit_text)
        try:
            print(colorize(f"commit {new_commit_hash}\n", BLUE) +
                  colorize(f'Date: {commit_match.group("date")}\n\n', RED) +
                  f'{commit_match.group("message")}\n')
        except AttributeError:
            print(f'{new_commit_hash} file does not match the commit format.')
            return
        past_commit_hash = new_commit_hash
        new_commit_hash = get_commit_parent_hash(new_commit_hash)
        print(colorize('Changed files:\n', PINK))
        if new_commit_hash:
            trees = []
            for commit_hash in new_commit_hash, past_commit_hash:
                try:
                    tree_hash = get_commit_tree_hash(commit_hash)
                except AttributeError:
                    print(f'Commit file {commit_hash} '
                          f'does not match the format.')
                    return
                try:
                    tree = read_tree(tree_hash)
                except AttributeError:
                    print(f'Tree file {tree_hash} '
                          f'does not match the format.')
                    return
                trees.append(tree)
            only_index_tree, only_commit_tree = get_trees_diff(*trees)
            left_dict = {x: y for x, y in
                         get_tree_children_names(only_index_tree)}
            right_dict = {x: y for x, y in
                          get_tree_children_names(only_commit_tree)}
            names_of_changed = sorted(list(set(left_dict.keys()).union(
                set(right_dict.keys()))))
        else:
            past_tree_hash = get_commit_tree_hash(past_commit_hash)
            comparison_tree = read_tree(past_tree_hash)
            names_of_changed = sorted(list(map(lambda x: x[0],
                                               get_tree_children_names(
                                                   comparison_tree))))
        for name in names_of_changed:
            print(name)
        print()
