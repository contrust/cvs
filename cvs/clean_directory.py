import os


def clean_directory(dir_path: str):
    for child in [os.path.join(dir_path, child) for child in os.listdir(dir_path) if child != '.cvs'][:]:
        os.remove(child)


if __name__ == '__main__':
    clean_directory('hi')
