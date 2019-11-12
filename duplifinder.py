import hashlib
import os
import sys
import traceback
import platform
from datetime import datetime
import argparse
import random


__version__ = 1.0


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
    if get_min_unixtime(list_of_duplicates, elem) == get_max_unixtime(list_of_duplicates, elem):
        return datetime
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


def get_hash_of_files_in_dir(argv, verbose):
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


def filter_the_depth(dictionary, depth=-1):
    df_dictionary = {}
    if depth < 0:
        return dictionary
    for key in dictionary:
        for elem in dictionary[key]:
            if elem['path'].count('/') <= depth + 1:
                df_dictionary = add_elem_to_dict(
                    [key, elem['path']], df_dictionary)
    return df_dictionary


def get_max_path_len(list_of_duplicates):
    max = 0
    for elem in list_of_duplicates:
        path = elem['path']
        if len(path) > max:
            max = len(path)
    return max


def form_query_for_format_snd(list_of_duplicates):
    query = "{:"
    query += str(get_max_path_len(list_of_duplicates) + 5)
    query += "s} {:<7s} {}"
    return query


def form_query_for_format_sord(list_of_duplicates):
    query = "{:"
    query += str(get_max_path_len(list_of_duplicates) + 5)
    query += "s} {}"
    return query


def form_query_for_format(list_of_duplicates):
    query = "{}"
    return query


def form_query_chooser(list_of_duplicates, args):
    if args.size and args.datetime:
        return form_query_for_format_snd(list_of_duplicates)
    elif args.size or args.datetime:
        return form_query_for_format_sord(list_of_duplicates)
    else:
        return form_query_for_format(list_of_duplicates)


def form_query_executer(query, path, size, datetime):
    if args.size and args.datetime:
        print(query.format(path, size, datetime))
    elif args.size:
        print(query.format(path, size))
    elif args.datetime:
        print(query.format(path, datetime))
    else:
        print(query.format(path))


def sort_by_datetime(list_of_duplicates):
   if len(list_of_duplicates) <= 1:
       return list_of_duplicates
   else:
       q = random.choice(list_of_duplicates)
       s_dups = []
       m_dups = []
       e_dups = []
       for elem in list_of_duplicates:
           if elem['unixtime'] > q['unixtime']:
               s_dups.append(elem)
           elif elem['unixtime'] < q['unixtime']:
               m_dups.append(elem)
           else:
               e_dups.append(elem)
       return sort_by_datetime(s_dups) + e_dups + sort_by_datetime(m_dups)


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
            path = elem['path']
            if args.human_readable:
                size = bytes_to_human(elem['size'])
            else:
                size = str(elem['size'])
            if args.color:
                datetime = str(color_chooser(dictionary[key], elem))
            else:
                datetime = get_readable_datetime(elem['unixtime'])
            form_query_executer(query, path, size, datetime)
        print('')
    else:
        print('There are no duplicates.')


def fetch_extra_data(dictionary):
    for key in dictionary:
        for elem in dictionary[key]:
            elem['unixtime'] = modification_date(elem['path'])
            elem['size'] = file_size(elem['path'])
    return dictionary


def display_error(result):
    print("Something went wrong.")
    traceback.print_exc()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='duplifinder', usage='%(prog)s <path> [-v] [-h] [-c] [-d INT] [-s [-H]] [-V] [-t [-S]]')
    parser.add_argument('path', type=str, help='define the directory path')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s v' + str(__version__))
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
        if dictionary != -1:
            d_dictionary = filter_the_depth(dictionary, args.depth)
            fd_dictionary = filter_the_dictionary(d_dictionary)
            efd_dictionary = fetch_extra_data(fd_dictionary)
            display_results(efd_dictionary, args)
        else:
            display_error(result)
