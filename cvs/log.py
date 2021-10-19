from cvs.branch import is_branch_exist
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
        commit_hash = ((heads_refs_path / head_content).read_text()
                       if is_branch_exist(head_content) else head_content)
    except FileNotFoundError:
        print(f'Branch {head_content} does not exist.')
        return
    while commit_hash:
        try:
            commit_text = (commits_path / commit_hash).read_text()
        except FileNotFoundError:
            print(f'Commit {commit_hash} does not exist.')
            return
        commit_match = COMMIT_REGEX.match(commit_text)
        try:
            print('\033[34m' + f'commit {commit_hash}' + '\033[0m\n' +
                  f'\033[31mDate: {commit_match.group("date")}\n\n\033[0m'
                  f'{commit_match.group("message")}\n')
        except AttributeError:
            print(f'{commit_hash} file does not match the commit format.')
            return
        past_commit_hash = commit_hash
        commit_hash = get_commit_parent_hash(commit_hash)
        print('\033[35m' + 'Changed files:\n' + '\033[0m')
        if commit_hash:
            tree_hash1 = get_commit_tree_hash(commit_hash)
            tree_hash2 = get_commit_tree_hash(past_commit_hash)
            tree1 = read_tree(tree_hash1)
            tree2 = read_tree(tree_hash2)
            only_index_tree, only_commit_tree = get_trees_diff(tree1,
                                                               tree2)
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
