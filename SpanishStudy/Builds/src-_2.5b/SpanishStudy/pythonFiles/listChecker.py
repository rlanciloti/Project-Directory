#Written by Ryan Lanciloti

#In charge of getting all the information from the lists directory

import os, re

#Checks to see what is in the list directory and returns a list of it
def inList():
	path = os.getcwd()
	#Changes to the correct initial path
	""" Subnote: __main__.py won't run unless in the same folder as this file because
	when the __main__.py is ran in a terminal setting, terminal runs the file as if it was
	one folder up (i.e if __main__.py file path was in
	/users/ryan/desktop/gitHub/Side-Project/'SpanishStudy', you'd have to run the 
	__main__.py file in /users/ryan/desktop/gitHub/Side-Project using 'python "StudySpanish"', 
	it searches for the 'lists' directory in the 'Side-Project' directory instead of one 
	level down where it's located in the 'SpanishStudy' directory), but if you want to 
	run the __main__.py in a text editor such as TextWrangler for dev reasons (hint: this 
	was the biggest of pains to figure out, so much trial and error, mostly error) you will 
	have to remove the '/SpanishStudy' form the line below because when the __main__.py is
	ran from a text editor such as IDLE (wouldn't recommend using IDLE for this one due to 
	the fact IDLE has compatibility issues  with easygui.py, I will be working on a version that uses
	wxPython for the gui's for further customization and to improve compatibility; I only used	
	easygui for ease of access) it is set in the actual directory that __main__.py is instead
	of one directory up. This is due to the fact that when you run from a terminal, you have to 
	call the directory that __main__.py is in from the directory one layer up, but when ran 
	from a text editor, it doesn't have to call it from one directory up."""
	
	""" I recommend putting __main__.py in the 'pythonFiles' directory, removing from the imports
	on __main__.py, 'the pythonFiles.' (i.e instead of 'import pythonFiles.logicClass as logicClass'
	put import logicClass), and changing the __init__.py file to has the correct hierarchy structure.
	The reason I didn't have the __main__.py file in pythonFiles directory is because their wouldn't
	have been a reason to use __init__.py, so basically I made it more work to practice good programming.
	P.S. if you read this entire thing, you deserve a cookie."""
	
	os.chdir(path + '/lists')
	x = []
	x.append(os.listdir('.'))
	os.chdir('..')
	
	return x[0]

#Figures out what is a .txt in the directory
def validObject():
	x = []
	cyclelist = inList()
	for element in cyclelist:
		if re.search('.txt', element):
			x.append(element)	
	return x

#Returns the length of the list
def listLength(list, usePath = True):
	#Fail Safe: If the person clicks 'Cancel' this won't run
	if list != None:
		if usePath:
			os.chdir('lists')
		with open(list+'.txt', "r") as file:
			os.chdir('..')
			return len(file.readlines())	
	else:
		return False