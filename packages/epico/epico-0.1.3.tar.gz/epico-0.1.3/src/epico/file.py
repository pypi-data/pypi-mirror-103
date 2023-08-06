import os

def create(filename, encoding=None):
	if encoding == None:
		f = open(filename, "w")
	else:
		f = open(filename, "w", encoding=encoding)
	f.close()

def append(filename, data, encoding=None):
	if encoding == None:
		f = open(filename, "a")
	else:
		f = open(filename, "a", encoding=encoding)
	f.write(data)
	f.close()

def write(filename, data, encoding=None):
	if encoding == None:
		f = open(filename, "w")
	else:
		f = open(filename, "w", encoding=encoding)
	f.write(data)
	f.close()

def delete(filename):
	if os.path.exists(filename):
		os.remove(filename)
		return True
	else:
		return False

def exists(filename):
	return os.path.exists(filename)

def read(filename, mode='s'):
	modes = ['s', 'l']
	if not mode in modes:
		mode = 's'

	f = open(filename, "r")
	if mode == 's':
		return f.read()
	elif mode == 'l':
		l = []
		for x in f:
			l.append(x)
		return l
	else:
		return f.read()
	f.close()


