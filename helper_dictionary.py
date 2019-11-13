import random
import platform
import os


class Files:
    """This is class containing the file information"""

    def __init__(self, path):
        self.path = path
        self.unixtime = 0
        self.size = 0

    def modification_date(self):
        if platform.system() == 'Windows':
            self.unixtime = os.path.getmtime(self.path)
        else:
            stat = os.stat(self.path)
            self.unixtime = stat.st_mtime

    def file_size(self):
        self.size = os.path.getsize(self.path)


def add_elem_to_dict(arr, dictionary):
    key = arr[0]
    path = arr[1]

    if key not in dictionary:
        dictionary[key] = []
    file_info = Files(path)
    dictionary[key].append(file_info)
    return dictionary


def filter_the_dictionary(dictionary):
    f_dictionary = {}
    for key in dictionary:
        if len(dictionary[key]) > 1:
            f_dictionary[key] = dictionary[key]
    return f_dictionary


def sort_by_datetime(list_of_duplicates):
    if len(list_of_duplicates) <= 1:
        return list_of_duplicates
    else:
        q = random.choice(list_of_duplicates)
        s_dups = []
        m_dups = []
        e_dups = []
        for elem in list_of_duplicates:
            if elem.unixtime > q.unixtime:
                s_dups.append(elem)
            elif elem.unixtime < q.unixtime:
                m_dups.append(elem)
            else:
                e_dups.append(elem)
        return sort_by_datetime(s_dups) + e_dups + sort_by_datetime(m_dups)
