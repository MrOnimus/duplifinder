def get_max_path_len(list_of_duplicates):
    max = 0
    for elem in list_of_duplicates:
        path = elem.path
        if len(path) > max:
            max = len(path)
    return max


