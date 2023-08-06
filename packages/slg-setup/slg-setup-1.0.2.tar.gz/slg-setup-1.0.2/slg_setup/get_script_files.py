from os import listdir
from os.path import isfile, join


def get_script_files():
    try:
        files = [
            f"scripts/{f}" for f in listdir('./scripts')
            if isfile(join('./scripts', f))]
    except FileNotFoundError:
        return []
    return files
