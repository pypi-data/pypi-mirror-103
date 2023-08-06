import os
import shutil

def delete(path, recursive=False):
	if not recursive:
		os.rmdir(path)
	else:
		shutil.rmtree('/path/to/your/dir/')

def create(path):
	os.mkdir(path)