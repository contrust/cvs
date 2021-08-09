# cvs

## Install

```sh
pip install .
```

## Usage

* Firstly, you should install cvs with 'pip install .'.
* Secondly, in your working directory you should execute 'python3 -m cvs -init' in terminal.
* After that, all the commands should be run from the same directory.

| Command | Description |
| --- | --- |
| python3 -m cvs -h | Show help message |
| python3 -m cvs -init | Make .cvs folder for further work with cvs |
| python3 -m cvs -status | Show current branch or commit you are working on |
| python3 -m cvs -log  | Show history of current commit |
| python3 -m cvs -add path | Add file or folder in cvs index |
| python3 -m cvs -rm path | Remove file or folder in cvs index |
| python3 -m cvs -commit message | Commit changes |
| python3 -m cvs -branch name | Create branch attached to current commit |
| python3 -m cvs -checkout name | Update files of working directory from commit, tag or branch |
| python3 -m cvs -tag name message | Create tag attached to current commit |
| python3 -m cvs --commit-list | Show all commit names |
| python3 -m cvs --tag-list | Show all tag names |
| python3 -m cvs --branch-list | Show all branch names |

## Author

👤 **Artyom Borisov**

* Github: [@contrust](https://github.com/contrust)
