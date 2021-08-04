from cvs.config import index_path


def read_index() -> str:
    with open(str(index_path)) as index_file:
        index_data = index_file.read()
        return index_data


def write_index(data: str) -> None:
    with open(str(index_path), mode='w') as index_file:
        index_file.write(data)
