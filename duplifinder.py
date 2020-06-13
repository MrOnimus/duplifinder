import os
import sys
import hashlib
import traceback
import argparse
from helper_files import get_max_path_len
from helper_dictionary import add_elem_to_dict, filter_the_dictionary, sort_by_datetime
from helper_datetime import get_readable_datetime, get_max_unixtime, get_min_unixtime
from helper_colors import color_print
from helper_print import form_query_chooser, form_query_executer


__version__ = 1.0


symbols = ('B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')


def bytes_to_human(n):
    n = int(n)
    format = '%(value).1f%(symbol)s'
    if n < 0:
        raise ValueError("n < 0")
    prefix = {}
    for i, s in enumerate(symbols[1:]):
        prefix[s] = 1 << (i+1)*10
    for symbol in reversed(symbols[1:]):
        if n >= prefix[symbol]:
            value = float(n) / prefix[symbol]
            return format % dict(symbol=symbol, value=value)
    return format % dict(symbol=symbols[0], value=n)


def color_chooser(list_of_duplicates, elem):
    datetime = get_readable_datetime(elem.unixtime)
    if get_min_unixtime(list_of_duplicates, elem) == get_max_unixtime(list_of_duplicates, elem):
        return str(datetime)
    if get_min_unixtime(list_of_duplicates, elem) == elem.unixtime:
        return color_print(datetime, 'red')
    elif get_max_unixtime(list_of_duplicates, elem) == elem.unixtime:
        return color_print(datetime, 'green')
    else:
        return str(datetime)


def filter_the_depth(dictionary, depth=-1):
    df_dictionary = {}
    if depth < 0:
        return dictionary
    for key in dictionary:
        for elem in dictionary[key]:
            if elem.path.count('/') <= depth + 1:
                df_dictionary = add_elem_to_dict(
                    [key, elem.path], df_dictionary)
    return df_dictionary


def add_extra_data(dictionary):
    for key in dictionary:
        for elem in dictionary[key]:
            elem.modification_date()
            elem.file_size()
    return dictionary


def get_hash_of_files_in_dir(argv, verbose):
    directory = str(argv[0])
    hash_table = {}

    if not os.path.exists(directory):
        raise Exception('This is not a valid directory.')

    try:
        for root, dirs, files in os.walk(directory):
            for names in files:
                if verbose:
                    print('Hashing', names)
                filepath = os.path.join(root, names)
                try:
                    file = open(filepath, 'rb')
                except:
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
        traceback.print_exc()
        raise Exception('Something went wrong.')

    return hash_table


def display_results(dictionary, args):
    if len(dictionary) > 0:
        greetings = 'You have '
        greetings += str(len(dictionary))
        greetings += ' set of duplicates here:'
        print(color_print(greetings, 'underline'))
        print('')
        for key in dictionary:
            print('This files are duplicates: ')
            query = form_query_chooser(dictionary[key], args)
            if args.sort and args.datetime:
                dictionary[key] = sort_by_datetime(dictionary[key])
            for elem in dictionary[key]:
                path = elem.path
                if args.human_readable:
                    size = bytes_to_human(elem.size)
                else:
                    size = str(elem.size)
                if args.color:
                    datetime = color_chooser(dictionary[key], elem)
                else:
                    datetime = get_readable_datetime(elem.unixtime)
                form_query_executer(query, path, size, datetime, args)
            print('')
    else:
        print('There are no duplicates.')


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        raise Exception("Must be using Python 3.")

    parser = argparse.ArgumentParser(
        prog='duplifinder', usage='%(prog)s <path> [-v] [-h] [-c] [-d INT] [-s [-H]] [-V] [-t [-S]]')
    parser.add_argument('path', type=str, help='define the directory path')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s v' + str(__version__))
    parser.add_argument('-c', '--color', dest='color', action='store_true',
                        default=False, help='provides colored output')
    parser.add_argument('-d', '--depth', type=int, default=-1,
                        help='set depth of the search', metavar='INT')
    parser.add_argument('-s', '--size', dest='size', action='store_true',
                        default=False, help='provides size information')
    parser.add_argument('-H', '--human-readable', dest='human_readable', action="store_true",
                        default=False, help='makes size output human readable')
    parser.add_argument('-V', '--verbose', dest='verbose',
                        action="store_true", default=0, help='verbose output')
    parser.add_argument('-t', '--datetime', dest='datetime', action="store_true", default=False,
                        help='display datetime of last file modification')
    parser.add_argument('-S', '--sort', dest='sort', action='store_true', default=False,
                        help='sorts all files according to datetime they have been created')
    args = parser.parse_args()
    if args.path:
        dictionary = get_hash_of_files_in_dir(args.path, args.verbose)
        d_dictionary = filter_the_depth(dictionary, args.depth)
        fd_dictionary = filter_the_dictionary(d_dictionary)
        efd_dictionary = add_extra_data(fd_dictionary)
        display_results(efd_dictionary, args)
