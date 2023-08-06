import os

def pause():
	input("EPICO: Press ENTER to continue...")

def init(self):
	self.super().__init__()

class Base:
	def __str__(self):
		f = self()
		return type(f).__name__