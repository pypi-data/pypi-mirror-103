import os

def pause():
	input("EPICO: Press ENTER to continue...")

class Base:
	def __init__(self):
		self.string = str(self)
		self.int = 0
	def __str__(self):
		return self.string
	def __int__(self):
		return self.int
	def set_data(self, string, integer):
		self.string = string
		self.int = integer