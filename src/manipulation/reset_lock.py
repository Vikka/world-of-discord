from json import load, dump, loads
from os import walk
from pathlib import Path

from src.constants.JSON_KEY import LOCK


def get_user_files():
    user_path = Path('data/users/')

    f = []
    for (dirpath, dirnames, filenames) in walk(user_path):
        if not filenames:
            continue
        f.extend(f'{dirpath}\\{filename}' for filename in filenames)
    return f


def reset_lock(user_files):
    for file_name in user_files:
        with open(file_name) as file:
            user_characters = load(file)
        for c in user_characters.values():
            c[LOCK] = 0
        with open(file_name, 'w') as file:
            dump(user_characters, file)


def clean_lock():
    user_files = get_user_files()
    reset_lock(user_files)
