
# Epico

Just some epic python utilities


##  Functions
 ###  epico.pause()
Pauses the terminal and waits for input to continue.

 ###  epico.dir.delete(path, recursive=False)
 Deletes the specified path. recursive is defaulted to false.

 ###  epico.dir.create(path)
 Creates the specified directory.

 ###  epico.file.create(filename, encoding=None)
 Creates the specified file. ecoding defaults to None.

 ###  epico.file.append(filename, data, encoding=None)
 Appends data to an **already existing** file.

 ###  epico.file.write(filename, data, encoding=None)
 Overwrites data to an **already existing** file.

 ###  epico.file.delete(filename)
 Deletes the specified file

 ###  epico.file.exists(filename)
 Detects if a file exists, returns True or False.

 ###  epico.file.read(filename, mode='s')
Reads the contents of a file, returns a string normally, but if mode set to '*l*' it becomes a list 
 
 ###  epico.thread.runfunc(function)
 Runs the specified function in a thread, and continues on in the code while that function is running