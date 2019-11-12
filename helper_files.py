import os
import platform


def get_max_path_len(list_of_duplicates):
    max = 0
    for elem in list_of_duplicates:
        path = elem['path']
        if len(path) > max:
            max = len(path)
    return max


def modification_date(path_to_file):
    if platform.system() == 'Windows':
        return os.path.getmtime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        return stat.st_mtime


def file_size(path_to_file):
    return os.path.getsize(path_to_file)
