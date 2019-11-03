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
    dictionary[key].append(val)
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
                    f1.close()
                    continue
                file_hash = hashlib.sha256()
                while 1:
                    # Read file in as little chunks
                    buf = file.read(4096)
                    if not buf:
                        break
                    file_hash.update(buf)
                    hash_table = add_elem_to_dict(
                        [file_hash.hexdigest(), filepath], hash_table)
                file.close()

    except:
        # Print the stack traceback
        traceback.print_exc()
        return -2

    return hash_table


def get_readable_datetime(unixtime):
    return datetime.utcfromtimestamp(unixtime).strftime('%Y-%m-%d %H:%M:%S')


def modification_date(path_to_file):
    if platform.system() == 'Windows':
        return os.path.getmtime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        return stat.st_mtime


def display_usage():
    print('usage: duplifinder <path to directory>')


def display_result(dictionary):
    #print('You have ' + str(len(dictionary)) + ' here:')
    for key in dictionary:
        if len(dictionary[key]) > 1:
            print('This files are duplicates:')
            for i, dup_elem in enumerate(dictionary[key]):
                print('  ' + str(i + 1) + '. ' + dup_elem + '  [ Date: ' +
                        str(
                            get_readable_datetime(
                                modification_date(dup_elem)
                                )
                            )
                        + ' ]')
            print('')


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) > 0:
        result = get_hash_of_files_in_dir(args, 0)
        display_result(result)
    else:
        display_usage()
