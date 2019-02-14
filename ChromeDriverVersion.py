import sys

macpath = "/Docs/macdriver"
windowspath = "/Docs/windowsdriver.exe"
linuxpath = "/Docs/linuxdriver"

currentPath = ""

os = sys.platform

def getPath():
	global currentPath
	if(currentPath == ""):
		if(os == "linux"):
			currentPath = linuxpath
		elif(os == "win32" or os == "cygwin"):
			currentPath = windowspath
		elif(os == "darwin"):
			currentPath = macpath

		return currentPath
	else:
		return currentPath
