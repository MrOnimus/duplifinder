import hashlib
import os
import sys
import traceback


def addDictElem(arr, dictionary):
    key = arr[0]
    val = arr[1]

    if key not in dictionary:
        dictionary[key] = []
    dictionary[key].append(val)
    return dictionary


def getHashofFilesInDir(argv, verbose=0):
    directory = str(argv[0])
    hashTable = {}

    if not os.path.exists(directory):
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
                fileHash = hashlib.sha256()
                while 1:
                    # Read file in as little chunks
                    buf = file.read(4096)
                    if not buf:
                        break
                    fileHash.update(buf)
                    hashTable = addDictElem(
                        [fileHash.hexdigest(), filepath], hashTable)
                file.close()

    except:
        # Print the stack traceback
        traceback.print_exc()
        return -2

    return hashTable


def displayUsage():
    print('usage: duplifinder <path to directory>')


def displayResult(dictionary):
    print('You have duplicates here:')
    for key in dictionary:
        if len(dictionary[key]) > 1:
            print(dictionary[key])


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) > 0:
        result = getHashofFilesInDir(args, 0)
        displayResult(result)
    else:
        displayUsage()
