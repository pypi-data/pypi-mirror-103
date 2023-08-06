import os

def pause():
	input("EPICO: Press ENTER to continue...")

def check_type(value, type):
	try:
		type(value)
	except ValueError:
		return False
	else:
		return True