import pytest
import os
import shutil
from cvs.config import *
from cvs.init import init


@pytest.fixture(autouse=True, scope="function")
def cvs_init():
    abspath = os.path.abspath(__file__)
    dirname = os.path.dirname(abspath)
    os.chdir(dirname)
    (repository_path / 'temp').mkdir()
    os.chdir(repository_path / 'temp')
    init()
    yield
    os.chdir(dirname)
    shutil.rmtree('temp')


@pytest.fixture(scope="function")
def create_two_files():
    (repository_path / 'test1.txt').write_text('')
    (repository_path / 'test2.txt').write_text('')


@pytest.fixture(scope="function")
def create_dir_with_two_files():
    (repository_path / 'test_dir').mkdir()
    (repository_path / 'test_dir' / 'test1.txt').write_text('')
    (repository_path / 'test_dir' / 'test2.txt').write_text('')
