#!/usr/bin/env python3
import argparse

from cvs.modify import add, rm
from cvs.branch import create_branch, branch_list
from cvs.checkout import checkout
from cvs.config import cvs_directory_path
from cvs.init import init
from cvs.commit import commit, commit_list
from cvs.log import log
from cvs.diff import diff
from cvs.status import status
from cvs.tag import tag, tag_list


def parse_arguments():
    """
    Parse console arguments.
    """
    parser = argparse.ArgumentParser(
        prog=None if not globals().get('__spec__')
        else f'python3 -m {__spec__.name.partition(".")[0]}'
    )
    parser.add_argument('-init',
                        action='store_true',
                        help='make .cvs folder for further work with cvs')
    parser.add_argument('-status',
                        action='store_true',
                        help='show current branch or commit '
                             'you are working on')
    parser.add_argument('-log',
                        action='store_true',
                        help='show history of current commit')
    parser.add_argument('-add',
                        metavar='path',
                        help='add file or folder in cvs index')
    parser.add_argument('-rm',
                        metavar='path',
                        help='remove file or folder in cvs index')
    parser.add_argument('-diff',
                        metavar=('commit1', 'commit2'),
                        help='show changed files',
                        nargs=2)
    parser.add_argument('-commit',
                        metavar='message',
                        help='commit changes')
    parser.add_argument('-branch',
                        metavar='name',
                        help='create branch attached to current commit')
    parser.add_argument('-checkout',
                        metavar='name',
                        help='update files of working directory from '
                             'commit, tag or branch')
    parser.add_argument('-tag',
                        metavar=('name', 'message'),
                        help='create tag attached to current commit',
                        nargs=2)
    parser.add_argument('--commit-list',
                        action='store_true',
                        help='show all commit names')
    parser.add_argument('--tag-list',
                        action='store_true',
                        help='show all tag names')
    parser.add_argument('--branch-list',
                        action='store_true',
                        help='show all branch names')
    return parser.parse_args()


def main():
    """
    Process parsed console arguments and run server.
    """
    args_dict = vars(parse_arguments())
    if args_dict['init']:
        try:
            init()
        except FileNotFoundError:
            print('Some files or directories were removed while init.')
    elif not cvs_directory_path.exists():
        print('CVS is not inited.')
    elif args_dict['status']:
        status()
    elif args_dict['log']:
        log()
    elif args_dict['commit_list']:
        commit_list()
    elif args_dict['tag_list']:
        tag_list()
    elif args_dict['branch_list']:
        branch_list()
    elif args_dict['add']:
        add(args_dict['add'])
    elif args_dict['rm']:
        rm(args_dict['rm'])
    elif args_dict['diff']:
        diff(args_dict['diff'][0], args_dict['diff'][1])
    elif args_dict['commit']:
        commit(args_dict['commit'])
    elif args_dict['checkout']:
        checkout(args_dict['checkout'])
    elif args_dict['tag']:
        tag(args_dict['tag'][0], args_dict['tag'][1])
    elif args_dict['branch']:
        create_branch(args_dict['branch'])


if __name__ == '__main__':
    main()
