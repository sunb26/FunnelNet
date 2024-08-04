import os


def file_exists(path):
    return os.path.isfile(path)


def dir_exists(path):
    return os.path.isdir(path)


def create_dir(path):
    os.makedirs(path, exist_ok=True)


def clear_dir(path):
    if dir_exists(path):
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if file_exists(file_path):
                os.remove(file_path)
