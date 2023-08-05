import os
from contextlib import contextmanager


@contextmanager
def change_cwd(path: str):
    original_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(original_cwd)


def check_path_exists(path: str, error_msg: str):
    if not os.path.exists(path):
        raise Exception(f"{error_msg} {path}")


def get_basename(path: str) -> str:
    return os.path.splitext(os.path.basename(path))[0]


def get_extension(path: str) -> str:
    return os.path.splitext(path)[1]


def ensure_dir(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
