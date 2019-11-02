import hashlib, os

def AddDictElem(arr, dictionary):
	if arr[0] in dictionary:
		dictionary[arr[0]].append(arr[1])
	else:
		dictionary[arr[0]] = []
		dictionary[arr[0]].append(arr[1])
	return dictionary

def GetHashofFilesInDir(directory, verbose=0):
	hashTable = {}
	if not os.path.exists (directory):
		return -1

	try:
		for root, dirs, files in os.walk(directory):
			for names in files:
				if verbose == 1:
					print('Hashing', names)
				filepath = os.path.join(root,names)
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
					hashTable = AddDictElem([fileHash.hexdigest(), filepath], hashTable)
				file.close()

	except:
		import traceback
		# Print the stack traceback
		traceback.print_exc()
		return -2

	return hashTable


result = GetHashofFilesInDir('.', 1)
print(result)