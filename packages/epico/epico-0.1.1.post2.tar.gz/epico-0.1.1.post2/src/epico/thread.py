import threading

def runfunc(func):
	threading.Thread(target=func).start()