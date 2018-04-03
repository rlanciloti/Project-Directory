#Written by Ryan Lanciloti

#This file was to keep the __main__.py file clean

import guiController, listChecker, logicClass

def main():
 
	#Initial prompt, returns english or spanish
	x = guiController.startup()
			
	#What list, returns name of list
	if x != '':
		y = guiController.selectList()
	else:
		return 
	
	
	"""Checks y's length, if the length is none then the program quits, else it goes to 
	the logicClass file to get the words from the list to quiz you on. Unknown why you have 
	to add 1 to z"""
	if y != ():
		z = listChecker.listLength(y)
	else:
		return
		
	if z != False:
		c = logicClass.listSelecter(y, z + 1)
	else:
		return 
	
	"""Tells the program whether to quiz in english or spanish and then it goes through and
	asks you the questions."""
	g = logicClass.EorS_return(x)