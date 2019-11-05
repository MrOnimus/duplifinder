import hashlib
import os
import sys
import traceback
import platform
from datetime import datetime


class Colors:
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'


def color_print(some_string, color):
    if color == 'red':
        return Colors.fg.red + some_string + Colors.reset
    elif color == 'green':
        return Colors.fg.green + some_string + Colors.reset
    elif color == 'cyan':
        return Colors.fg.cyan + some_string + Colors.reset
    elif color == 'purple':
        return Colors.fg.purple + some_string + Colors.reset
    elif color == 'yellow':
        return Colors.fg.yellow + some_string + Colors.reset
    elif color == 'underline':
        return Colors.underline + some_string + Colors.reset


def color_chooser(list_of_duplicates, elem):
    datetime = get_readable_datetime(elem['unixtime'])
    if get_min_unixtime(list_of_duplicates, elem) == elem['unixtime']:
        return color_print(datetime, 'red')
    elif get_max_unixtime(list_of_duplicates, elem) == elem['unixtime']:
        return color_print(datetime, 'green')
    else:
        return datetime


def add_elem_to_dict(arr, dictionary):
    key = arr[0]
    val = arr[1]

    if key not in dictionary:
        dictionary[key] = []
    dictionary[key].append({
        'path': val
    })
    return dictionary


def get_hash_of_files_in_dir(argv, verbose=0):
    directory = str(argv[0])
    hash_table = {}

    if not os.path.exists(directory):
        print('This is not a valid directory.')
        return -1

    try:
        for root, dirs, files in os.walk(directory):
            for names in files:
                if verbose == 1:
                    print('Hashing', names)
                filepath = os.path.join(root, names)
                try:
                    file = open(filepath, 'rb')
                except:
                    # You can't open the file for some reason
                    file.close()
                    continue
                file_hash = hashlib.sha256()
                while True:
                    buf = file.read(4096)
                    if not buf:
                        break
                    file_hash.update(buf)
                    hash_table = add_elem_to_dict(
                        [file_hash.hexdigest(), filepath], hash_table)
                file.close()

    except:
        return -1

    return hash_table


def get_readable_datetime(unixtime):
    return datetime.utcfromtimestamp(unixtime).strftime('%m.%d.%Y %H:%M:%S')


def file_size(path_to_file):
    return os.path.getsize(path_to_file)


def modification_date(path_to_file):
    if platform.system() == 'Windows':
        return os.path.getmtime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        return stat.st_mtime


def display_usage():
    print('usage: duplifinder <path to directory>')


def get_min_unixtime(list_of_duplicates, target_elem):
    min_unixtime = True
    for elem in list_of_duplicates:
        if min_unixtime == True or min_unixtime > elem['unixtime']:
            min_unixtime = elem['unixtime']
    return min_unixtime


def get_max_unixtime(list_of_duplicates, target_elem):
    max_unixtime = True
    for elem in list_of_duplicates:
        if max_unixtime == True or max_unixtime < elem['unixtime']:
            max_unixtime = elem['unixtime']
    return max_unixtime


def filter_the_dictionary(dictionary):
    f_dictionary = {}
    for key in dictionary:
        if len(dictionary[key]) > 1:
            f_dictionary[key] = dictionary[key]
    return f_dictionary


def get_max_path_len(list_of_duplicates):
    max = 0
    for elem in list_of_duplicates:
        path = elem['path']
        if len(path) > max:
            max = len(path)
    return max


def form_query_for_format(list_of_duplicates):
    query = "{:"
    query += str(get_max_path_len(list_of_duplicates) + 5)
    query += "s} {:<5d} {}"
    return query


def print_table(list_of_duplicates):
    query = form_query_for_format(list_of_duplicates)
    for elem in list_of_duplicates:
        path = elem['path']
        size = elem['size']
        colored_datetime = str(color_chooser(list_of_duplicates, elem))
        print(query.format(path, size, colored_datetime))


def display_result(dictionary):
    f_dictionary = filter_the_dictionary(dictionary)
    if len(f_dictionary) > 0:
        greetings = 'You have '
        greetings += str(len(f_dictionary))
        greetings += ' set of duplicates here:'
        print(color_print(greetings, 'underline'))
        print('')
        for key in f_dictionary:
            if len(f_dictionary[key]) > 1:
                print('This files are duplicates:')
                for elem in f_dictionary[key]:
                    elem['unixtime'] = modification_date(elem['path'])
                    elem['size'] = file_size(elem['path'])
                print_table(f_dictionary[key])
                print('')
    else:
        print('There are no duplicates.')


def display_error(result):
    print("Something went wrong.")
    traceback.print_exc()


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) > 0:
        result = get_hash_of_files_in_dir(args, 0)
        if result != -1:
            display_result(result)
        else:
            display_error(result)
    else:
        display_usage()
