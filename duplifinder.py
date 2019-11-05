import hashlib
import os
import sys
import traceback
import platform
from datetime import datetime


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
                    if not buf: break
                    file_hash.update(buf)
                    hash_table = add_elem_to_dict(
                        [file_hash.hexdigest(), filepath], hash_table)
                file.close()

    except:
        return -1

    return hash_table


def get_readable_datetime(unixtime):
    return datetime.utcfromtimestamp(unixtime).strftime('%m.%d.%Y %H:%M:%S')


def modification_date(path_to_file):
    if platform.system() == 'Windows':
        return os.path.getmtime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        return stat.st_mtime


def display_usage():
    print('usage: duplifinder <path to directory>')


def is_this_unixtime_min(list_of_duplicates, elem):
    if min(list_of_duplicates, key = lambda elem : elem['unixtime']):
        return True
    return False


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
    query += "s} {:10s}"
    return query


def print_small_table(list_of_duplicates):
    query = form_query_for_format(list_of_duplicates)
    for elem in list_of_duplicates:
        path = elem['path']
        datetime = get_readable_datetime(elem['unixtime'])
        print(query.format(path, datetime))


def display_result(dictionary):
    f_dictionary = filter_the_dictionary(dictionary)
    print('You have ' + str(len(f_dictionary)) + ' set of duplicates here:')
    if len(f_dictionary) > 0:
        for key in f_dictionary:
            if len(f_dictionary[key]) > 1:
                print('This files are duplicates:')
                for elem in f_dictionary[key]:
                    elem['unixtime'] = modification_date(elem['path'])
                print_small_table(f_dictionary[key])
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
