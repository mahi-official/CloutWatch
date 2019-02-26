import sys
import errorLog

macpath = "Docs/macosdriver/chromedriver"
windowspath = "Docs/windowsdriver/chromedriver.exe"
linuxpath = "Docs/linuxdriver/chromedriver"

currentPath = ""

os = sys.platform


def getPath():
	try:
		global currentPath
		if(currentPath == ""):
			if(os == "linux"):
				currentPath = linuxpath
			elif(os == "win32" or os == "cygwin"):
				currentPath = windowspath
			elif(os == "darwin"):
				currentPath = macpath

			print("ChromeDriver found: " + currentPath)
			return currentPath
		else:
			return currentPath
	except Exception as e:
		print(e)
		errorLog.log(e)