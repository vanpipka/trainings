import os


def create_path(folder: str) -> None:
    if not os.path.isdir(folder):
        os.mkdir(folder)


def get_file_name(full_name: str) -> str:

    path_data = full_name.split("\\")
    return path_data[-1]


def get_path_from_file_name(full_name: str) -> str:
    path_data = full_name.split("\\")
    return "\\".join(path_data[:-1])


