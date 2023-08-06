import os

def pause():
	input("EPICO: Press ENTER to continue...")

class Base:
	def __str__(self):
		return type(self).__name__