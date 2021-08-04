import os
import shutil


def clean_directory(dir_path: str):
    for child in [os.path.join(dir_path, child) for child in os.listdir(dir_path) if child != '.cvs'][:]:
        if os.path.isfile(child):
            os.remove(child)
        elif os.path.isdir(child):
            shutil.rmtree(child)
