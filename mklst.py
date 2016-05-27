
help_string = """
  Autor: Oleg Pedorenko, IP-31
  04.10.2015
  Program: mklst.py
  Call like that:
  python program arg1 arg2 [arg3, arg4 ....]
  where:
      arg1 - name of the file to make a listing for, or
             a regular expression for a bunch of such files
      arg2 - name of a file for listing output
      arg3, arg4, ... - the names of files in the order you want
             to see them in the output. For files not listed here
             here the order is undefined.
  If you want to compile your files using javac to get error
  messages, change the compile variable to True.
"""

import subprocess
import os.path
import sys
import glob
import time
import datetime

if(len(sys.argv) < 3):
    print help_string
else:
    files = glob.glob(sys.argv[1])
    #Constructing list of all libraries
    libs = glob.glob("lib\*.*")
    l = ''
    for lib in libs:
        l = l + ';' + lib
    libs = l[1:]
    compile = False
    newFiles = []
    filesCopy = files[:]
    if(len(sys.argv) > 3):
        for name in sys.argv[3:]:
            for file in files:
                if(name in file):
                    newFiles.append(file)
                    filesCopy.remove(file)
                    break
        files = newFiles + filesCopy
    print 'Processing', files
    if(len(files)!=1):
        f = open(sys.argv[2], "w")
        f.close()
        for f in files:
            subprocess.call(["python", sys.argv[0], f, sys.argv[2]])
    else:
        sourceFile = files[0]
        lf = open(sys.argv[2], 'a')
        compileTime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        sourceTime = os.path.getmtime(sourceFile)
        sourceTime = datetime.datetime.fromtimestamp(sourceTime).strftime('%Y-%m-%d %H:%M:%S')
        lf.write("\n")
        lf.write('Compiling ' + sourceFile + ": \n")
        lf.write('Source file timestamp: ' + sourceTime + '\n')
        lf.write('Compiled at: ' + compileTime + '\n')
        lf.write('\n')
        sourceFileReader = open(sourceFile, "r")
        i = 0
        for line in sourceFileReader:
            i = i + 1
            lf.write("\t%3d. %s" % (i, line))
        err = ''
        if(compile):
            sp = subprocess.Popen(["javac", "-cp", libs, "-g:lines", "-d", "bin", "-sourcepath", "src", sourceFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (out, err) = sp.communicate()
        lf.write("\n")
        if(len(err) == 0):
            lf.write(str(i) + " lines: No errors")
        else:
            lf.write(err)
        lf.write('\n\n')
