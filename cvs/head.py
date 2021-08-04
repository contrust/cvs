from cvs.config import head_path


def read_head() -> str:
    with open(str(head_path)) as index_file:
        index_data = index_file.read()
        return index_data


def write_head(data: str) -> None:
    with open(str(head_path), mode='w') as index_file:
        index_file.write(data)
