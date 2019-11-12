from helper_files import get_max_path_len
import argparse


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


def form_query_executer(query, path, size, datetime, args):
    if args.size and args.datetime:
        print(query.format(path, size, datetime))
    elif args.size:
        print(query.format(path, size))
    elif args.datetime:
        print(query.format(path, datetime))
    else:
        print(query.format(path))
