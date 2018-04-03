#Written by Ryan Lanciloti

#This file holds all menu commands associated with the Tkinter GUIs
import listChecker
import os, re

#Changing the directory to the lists

class addFile(): #Adds a new list to the list box
	def __init__(self):
		from TkinterGUI import NewList
		os.chdir('lists')
		num = 2
		self.list = NewList() #Creates a NewList object
		self.list.wait() #Waits until the window has been destroyed
		self.name = self.list.name #Gets the name of the object
		if self.name != '': #Checks if there is a name 
			file = open(self.name+'.txt', 'w') #Opens the file
			
			#Loops through the list of a list of spanish and english words
			for x in self.list.words:  
				if x != None:
					for y in x: #Loops through the single list of words 
						"""SIDE NOTE: This is required for the lists as failing to remove
						the '\n' will cause the list to have a space in between the lines, 
						this will cause the interpreter to make errors"""
						word = y.rstrip('\n') #Removes the newline special character
						#Basic sorting system
						if num % 2 == 0: 
							file.write('e: '+word+'\n')
							num+=1
						else:
							file.write('s: '+word+'\n')
							num+=1	
			file.close()
		os.chdir('..')

def delete_list(master): #Deletes an item from the list and out of the directory  
	list_id = master.curselection() #Item ID
	list = master.get(list_id) #Item Name
	os.chdir('lists')		
	os.remove(list+'.txt') #Removes it from the list
	os.chdir('..')

def editFile(title): #Allow editing of the files
	from listChecker import listLength
	from TkinterGUI import NewList
	allWords = [] #Placeholder list
	os.chdir('lists')
	
	with open(title+'.txt', 'r+') as file:
		eORs = 0 #Used in distribution of arrays
		num = 2 #Used for sorting
		for x in range(0, listLength(title, False)): #Iterates each line
			word = file.readline()
			if word[0:3] == 'e: ' or word[0:3] == 's: ': #Checks if word has the beginning
				allWords.append(word) #Appends it to the allWords
		listObject = NewList() #New instance of NewList()
		listObject.addTitle(title) #Puts the title into the title entry widget
		numOfElements = (len(allWords)/2)-1 #Finds out how many groups are needed
		
		for x in range(0,numOfElements): #Adds the needed groups
			listObject.addCanvas()
		
		for x in listObject.elements: #Loops through a list of all groups
			try: #Needed incase the element is empty
				#Puts the english and spanish words in an array
				var = [allWords[eORs], allWords[eORs+1]] 
				x.addValues(var) #Puts the values into the boxes
				eORs+=2 #Iterates up for the next box
			except IndexError:
				pass
		
		listObject.wait() #Waits till the box is destroyed
		file.seek(0) #Removes all content from the file originally 
		file.truncate()
		if title != listObject.name: #Checks if the old and new title don't match
			os.chdir('lists')
			os.renames(title+'.txt', listObject.name+'.txt') #Renames the title
			os.chdir('..')
		for x in listObject.words: #Iterates through all changes
			if x != None: #Checks if TclError has been passed
				for y in x: #Loops through single list of english and spanish words
					word = y.rstrip('\n') #Removes the '\n'
					if num % 2 == 0: #Sorts
						file.write('e: '+word+'\n') #Rewrites it to the file
						num+=1
					else: 
						file.write('s: '+word+'\n') #Rewrites it to the file
						num+=1			