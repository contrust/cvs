import difflib
from cvs.branch import is_branch_exist
from cvs.color import colorize, PINK
from cvs.hash_object import Blob
from cvs.commit import get_commit_tree_hash, is_commit_exist
from cvs.config import heads_refs_path, tags_refs_path
from cvs.read_tree import read_tree
from cvs.tag import is_tag_exist, get_tag_commit_hash
from cvs.tree_diff import get_trees_diff, get_tree_children_names


def is_binary_string(string: bytes) -> bool:
    chars = bytearray({7, 8, 9, 10, 12, 13, 27} |
                      set(range(0x20, 0x100)) - {0x7f})
    return bool(string.translate(None, chars))


def diff(ref_name1, ref_name2):
    trees = []
    for ref_name in ref_name1, ref_name2:
        try:
            commit_hash = get_commit_hash_by_ref_name(ref_name)
        except AttributeError:
            print(f'Can not parse tag {ref_name} file.')
            return
        if commit_hash is None:
            print(f'There is no commit, branch or tag with {ref_name} name')
            return
        tree_hash = get_commit_tree_hash(commit_hash)
        tree = read_tree(tree_hash)
        trees.append(tree)
    left_only, right_only = get_trees_diff(*trees)
    left_dict = {x: y for x, y in get_tree_children_names(left_only)}
    right_dict = {x: y for x, y in get_tree_children_names(right_only)}
    for name in sorted(list(
            set(left_dict.keys()).union(set(right_dict.keys())))):
        data1 = left_dict.get(name, Blob(data=b'')).data
        data2 = right_dict.get(name, Blob(data=b'')).data
        if data1 or data2:
            if not is_binary_string(data1) and not is_binary_string(data2):
                data1, data2 = map(
                    lambda x: x.decode('utf-8').splitlines(), [data1, data2])
                diff_lines = list(difflib.unified_diff(data1, data2,
                                                       name, name))
                print(colorize(name, PINK))
                for i in diff_lines[2:]:
                    print(('\033[32m' if i.startswith('+') else
                           ('\033[31m' if i.startswith('-') else '')) +
                          i + '\033[0m')
                print()
            else:
                print(f'{colorize(name, PINK)} binary file size '
                      f'was changed from {len(data1)} to {len(data2)} bytes\n')
    print(end="")


def get_commit_hash_by_ref_name(name: str) -> str:
    if is_commit_exist(name):
        return name
    if is_branch_exist(name):
        commit_hash = (heads_refs_path / name).read_text()
        return commit_hash
    if is_tag_exist(name):
        commit_hash = get_tag_commit_hash(name)
        return commit_hash
    return None