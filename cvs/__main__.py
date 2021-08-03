#!/usr/bin/env python3
import argparse

from cvs.add import add
from cvs.init import init
from cvs.commit import commit


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
    parser.add_argument('-add',
                        metavar='path',
                        help='updates file or folder of cvs index')
    parser.add_argument('-commit',
                        metavar='message',
                        help='commit changes')
    return parser.parse_args()


def main():
    """
    Process parsed console arguments and run server.
    """
    try:
        args_dict = vars(parse_arguments())
        if args_dict['init']:
            init()
        elif args_dict['add']:
            add(args_dict['add'])
        elif args_dict['commit']:
            commit(args_dict['commit'])
    except Exception as e:
        print(f"{type(e).__name__} at line"
              f" {e.__traceback__.tb_lineno} of {__file__}: {e}")


if __name__ == '__main__':
    main()
