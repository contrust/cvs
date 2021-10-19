import os

from cvs.clean_directory import clean_directory


def test_clean_everything_but_not_cvs_subdirectory(create_two_files,
                                                   create_dir_with_two_files):
    assert os.listdir('.') != ['.cvs']
    clean_directory('.')
    assert os.listdir('.') == ['.cvs']
