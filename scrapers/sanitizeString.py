def cleanString(inputStr):
	for char in ["®", "/", "'", '"', "[", "]", "(", ")", "`"]:
		inputStr = inputStr.replace(char, "")
	return inputStr
