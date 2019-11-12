from datetime import datetime


def get_readable_datetime(unixtime):
    return datetime.utcfromtimestamp(unixtime).strftime('%m.%d.%Y %H:%M:%S')


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
