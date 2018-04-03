#Written by Ryan Lanciloti

#This is the file that creates all GUI's/Replaces the old guiController.py file
"""Fun Fact: This file alone, with all the space to look nice included, is over 100 lines
longer than all files in Version 1.0 put together"""

import sys
import listChecker
from Tkinter import *

class Startup(): #Replaces the startup function
	def __init__(self):
		self.guiShell = Tk() #Main frame
		self.answer = '' #The returned value
		self.closed = False #Error Handling
		
		self.guiShell.bind('WM_DELETE_WINDOW', self.close) #Closing window protocol
		
		#Question
		message = 'Please select whether you want\nto be quized in either Spanish or English' 
		
		frame1 = Frame(self.guiShell, width=500, height=175) #Frame1 holds the question
		frame1.pack(fill=BOTH)
		
		frame2 = Frame(self.guiShell) #Frame2 holds the buttons
		frame2.pack(fill=BOTH)
		#Column configuration was to ensure the buttons were in their proper place
		frame2.columnconfigure(0, minsize=242) #Half the size of the self.guiShell
		frame2.columnconfigure(1, minsize=242)
		
		#self.guiShell configuration
		self.guiShell.title('Select a language')
		self.guiShell.resizable(0,0) #To ensure the size can't be changed
		self.guiShell.geometry('485x130+500+300') #Sets the size of the GUI
		
		#Displays the question
		message = Label(frame1, text=message, font=('Times', 16)) 
		message.pack(pady=25)
		
		#First button
		spanishButton = Button(frame2, text='Spanish', command=self.returnSpanish)
		spanishButton.grid(row=0, column=0, padx=5, sticky=W)
		if spanishButton == 'spanish':
			return 'Spanish'
		
		#Second button
		englishButton = Button(frame2, text='English', command=self.returnEnglish)
		englishButton.grid(row=0, column=1, padx=1, sticky=E)
		if englishButton == 'english':
			return 'english'
			
		self.guiShell.mainloop() #Keeps the gui running until something says otherwise
		
	def returnSpanish(self): 
		self.guiShell.destroy()
		self.answer = 'spanish'
		
	def returnEnglish(self):
		self.guiShell.destroy()
		self.answer = 'english'
	
	def close(self): #Basic Function
		self.close = True

class SelectList(): #Replaces the selectList method
	def __init__(self, validObjects):
		self.guiShell = Tk() #Main Frame
		self.answer = None #The Returned Value
		self.close = False #Error Handling
		
		self.guiShell.bind('<Return>', lambda e: self.next()) #Returns the value after pressing enter
		self.guiShell.bind('WM_DELETE_WINDOW', self.close) #Closing window protocol
		
		menu = Menu(self.guiShell) #Makes a menu
		
		file = Menu(menu, tearoff=0) #Creates the file section
		file.add_command(label='New list', command=self.newList) #Adds a 'New list' option
		file.add_command(label='Delete list', command=self.deleteList) #Adds a 'Delete list' option
		file.add_command(label='Quit', command=lambda: self.guiShell.destroy()) #Adds a 'Quit' option
		
		edit = Menu(menu, tearoff=0) #Creates the edit section
		edit.add_command(label='Edit list', command=self.editList) #Adds an 'Edit list' option
		
		menu.add_cascade(label='File', menu=file) #Appends the file menu to the main menu
		menu.add_cascade(label='Edit', menu=edit) #Appends the edit menu to the main menu
		
		#The directions		
		directions= Label(self.guiShell, text='Please select your list of words from below:') 
		directions.pack()
		
		#frame1 holds the list box
		frame1 = Frame(self.guiShell, borderwidth=2, relief=RIDGE)
		frame1.pack(pady=5)
		
		#frame2 holds the buttons
		frame2 = Frame(self.guiShell)
		frame2.columnconfigure(0, minsize=200)
		frame2.columnconfigure(1, minsize=200)
		frame2.pack(fill=X)
		
		#List box that holds all the possible lists
		self.list = Listbox(frame1, selectmode=SINGLE, width=40, height=23)
		
		#Loops through all vaildObjects
		for item in validObjects:
			newItem = item[0:len(item)-4] #Removes .txt
			self.list.insert(END, newItem) #Adds the name to the list
		
		self.list.grid(row=0, column=0) #Grids the list
		
		self.list.bind('<Return>', self.next()) #Enter goes to the next thing
		
		scrollY = Scrollbar(frame1, orient=VERTICAL) #Ability to scroll up and down
		
		scrollX = Scrollbar(frame1, orient=HORIZONTAL) #Ability to scroll left and right 
		
		scrollY.configure(command=self.list.yview) #Sets the scroll bar to the list box
		self.list.configure(yscrollcommand=scrollY.set)
		
		scrollX.configure(command=self.list.xview) #Sets the scroll bar to the list box
		self.list.configure(xscrollcommand=scrollX.set)
		
		#First button
		next = Button(frame2, text='Next', command=self.next)
		next.grid(row=0, column=1, padx=50, pady=10, sticky=E)
		
		#Second button
		cancel = Button(frame2, text='Cancel', command=lambda: self.guiShell.destroy())
		cancel.grid(row=0, column=0, padx=50, pady=10, sticky=W)
		
		#Configures self.guiShell
		self.guiShell.config(menu=menu) #Sets the menubar to the gui
		self.guiShell.title('Select a list')
		self.guiShell.resizable(0,0) 
		self.guiShell.geometry('400x500+400+150')
		
		self.guiShell.mainloop()
	
	def next(self): #Goes to the next GUI
		self.answer = self.list.curselection() #Index of the selected element
		if self.answer == (): #Checks if the index is empty
			pass
		else:
			self.answer = self.list.get(self.answer) #Gets the title of the element
			self.guiShell.destroy() #Destroys the GUI
	
	def newList(self): #Allows the user to add new lists
		from menuCommands import addFile
		menu = addFile() #Creates the bridge between the GUI and the file
		if menu.name != '': #Checks if there is a name
			self.list.insert(END, menu.name) #Inserts the new list into the list box
	
	def editList(self): #Allows the user to edit previous lists
		from menuCommands import editFile
		nameID = self.list.curselection() #Selected ID
		name = self.list.get(nameID) #Selected name
		file = editFile(name) #Generates a writable GUI with all the old information there
		self.list.delete(0, END) #Deletes everything from the list box
		for item in listChecker.validObject(): #Rechecks for all available items and adds them to the list
			newItem = item[0:len(item)-4] #Gets names without '.txt'
			self.list.insert(END, newItem) #Inserts all valid elements into the list box
	
	def deleteList(self): #Deletes the list
		from menuCommands import delete_list
		delete_list(self.list) #Deletes the list from the computer
		self.list.delete(ACTIVE) #Deletes the list from the list box
	
	def close(self): #Basic Function
		self.close = True

class UserQuestion(): #Replaces the userQuestion method
	def __init__(self, languageValue):
		self.guiShell = Tk() #Main Frame
		self.answer = None #Returned Value
		self.close = False #Error Handling 
		
		#Directions
		directions = Label(self.guiShell, text='Please enter the translation for \n'+ '\"' +languageValue + '\"',
						   font=('Times', 14))
		directions.pack()
		
		#Were you write your answer
		self.textField = Entry(self.guiShell)
		self.textField.pack(fill=X, padx=5)
		
		#Enter will act as the next button
		self.textField.bind('<Return>', lambda e: self.next())
		self.guiShell.bind('WM_DELETE_WINDOW', self.delete)
		
		#Frame1 holds the buttons
		frame1 = Frame(self.guiShell)
		frame1.columnconfigure(0, minsize=175)
		frame1.columnconfigure(1, minsize=175)
		frame1.pack(fill=X)
		
		#First Button
		next = Button(frame1, text='Next', command=self.next)
		next.grid(row=0, column=1, padx=20, pady=5, sticky=E)
		
		#Second Button
		cancel = Button(frame1, text='Cancel', command=lambda: self.guiShell.destroy())
		cancel.grid(row=0, column=0, padx=20, pady=5, sticky=W)
		
		#self.guiShell configuration
		self.guiShell.title('Quiz')
		self.guiShell.resizable(0,0)
		self.guiShell.geometry('350x100+400+150')
		
		self.guiShell.mainloop()
		
	def next(self): #Goes to the next GUI
		if self.textField.get() != '': #Checks if the box is empty
			self.answer = self.textField.get() #Gets the list name
			self.guiShell.destroy()
	def delete(self): #Basic function
		self.close = True
		
class WrongAnswer(): #Replaces the wrongAnswer method
	def __init__(self, wrong, right, word):
		self.guiShell = Tk() #Main Frame
		self.close = False #Error Handling
		self.clear = False #Error Handling
		
		self.guiShell.bind('<Return>', self.next) #Destroys the box

		#Tells the user what they got wrong
		answer = Label(self.guiShell, text='You answered \'%s\' \ninstead of \'%s\'\nfor \'%s\'.' % (wrong, right, word),
					   font=('Times', 15))
		answer.pack()
		
		#First button
		cancel = Button(self.guiShell, text='Next', command=self.next)
		cancel.pack(side=RIGHT, padx=10, pady=3)
		
		#self.guiShell configuration
		self.guiShell.title('Wrong answers')
		self.guiShell.resizable(0,0)
		self.guiShell.geometry('350x100+400+150')
		
		self.guiShell.mainloop()
		
	def next(self):
		self.clear = True
		self.guiShell.destroy()

class NewList(): #Creates the GUI to input the new list
	def __init__(self):
		self.guiShell = Toplevel() #Main Frame
		self.words = [] #Holds the name of all the elements
		self.nextY = 0 #NW Y-postion of the next element
		self.elements = [] #List that holds the ID of all the elements
		self.frames = [] #List that holds the ID of all the element frames
		self.name = '' #Safety protocol for naming the list
		
		#Frame 1 holds the Title label and Entry widget
		frame1 = Frame(self.guiShell)
		frame1.columnconfigure(1, minsize=340)
		frame1.pack()
		
		#Frame2 hold the Canvas		
		frame2 = Frame(self.guiShell)
		frame2.pack()
		
		#Frame3 hold the Buttons
		frame3 = Frame(self.guiShell)
		frame3.columnconfigure(0, minsize=10)
		frame3.columnconfigure(1, minsize=207)
		frame3.columnconfigure(2, minsize=40)
		frame3.pack()
		
		#Canvas holds all the Element instances
		self.canvas = Canvas(frame2, width=380, height=220, bd=0)
		
		#Scrollbar for the canvas
		scrollbar = Scrollbar(frame2, orient=VERTICAL, command=self.canvas.yview)
		scrollbar.pack(side=RIGHT, fill=Y)
		
		#Canvas/Scrollbar configure
		self.canvas.configure(yscrollcommand=scrollbar.set)
		self.canvas.pack(side=LEFT)
		
		#Binding scrolling 		
		self.canvas.bind('<MouseWheel>', self.onMouseWheel)
		
		#Title label
		label = Label(frame1, text='Title:')
		label.grid(row=0, column=0)
		
		#Initial element
		self.addCanvas()
		
		#First Button
		add = Button(frame3, text='Add Group', command=self.addCanvas)
		add.grid(row=0, column=0, sticky=W, padx=5)
		
		#Second Button
		delete = Button(frame3, text='Delete Group', command=self.deleteCanvas)
		delete.grid(row=0, column=1, sticky=W, padx=0)
		
		#Third Button
		done = Button(frame3, text='Done', command=self.done)
		done.grid(row=0, column=2, sticky=E, padx=5)
		
		#Fourth Button
		self.title = Entry(frame1, width=45)
		self.title.grid(row=0, column=1, sticky=E, pady=5)
		
		#self.guiShell configure
		self.guiShell.title('New List')
		self.guiShell.resizable(0,0)
		self.guiShell.geometry('400x300+400+150')
		
	def wait(self): #For checks on when the GUI is destroyed
		self.guiShell.wait_window()
	
	def addCanvas(self): #Adds the element and frame window to the canvas
		master = self.canvas #Sets the master
		frame = Frame(master) #Frame holds an element
		element = Element(frame, master) #Creates an instance of element
		#Creates a frame window, necessary for widgets to appear on canvas 
		frame_window = master.create_window(0,self.nextY, anchor=NW) 
		master.itemconfigure(frame_window, window=frame) #Adds the frame window to the canvas
		self.nextY+=58 
		#Generates a region where you can scroll, import for height controll
		master.configure(scrollregion=(0,0,400,self.nextY)) 
		self.frames.append(frame) #Adds the frame to the frames list 
		self.elements.append(element) #Adds the element to the elements list
			
	def deleteCanvas(self): #Deletes the latest instance of element
		self.frames.pop(len(self.frames)-1).destroy() #Does this by destroying the frame
		self.nextY-=58 #Resets the y coordinate offset back to the value prior 
		
	#Used for editing	
	def addTitle(self, title): 
		self.title.insert(END, title) #Inserts a title into the entry widget 
			
	def done(self): #Goes to the next GUI
		self.name = self.title.get() #Gets the name of the file
		for x in self.elements: #Loops through the elements array
			self.words.append(x.getValues()) #Appends all those correct values 
		self.guiShell.destroy()
				
	def onMouseWheel(self, event): #Scroll event
		self.canvas.yview_scroll(event.delta, 'units')

class Element(): #Creates the little boxes which store a spanish and an english word 
	def __init__(self, master, canvas):
		self.more = False
		self.canvas = canvas #Canvas from NewList
		
		#Frame holds all the widgets
		frame = Frame(master, bd=2, relief=RIDGE)
		frame.columnconfigure(1, minsize=330)
		frame.pack()
		
		#Binds scrolling
		frame.bind('<MouseWheel>', self.onMouseWheel)
		
		#Label for English
		english = Label(frame, text='English:')
		english.grid(row=1, column=0)
		english.bind('<MouseWheel>', self.onMouseWheel)
		
		#Label for Spanish
		spanish = Label(frame, text='Spanish:')
		spanish.grid(row=2, column=0)
		spanish.bind('<MouseWheel>', self.onMouseWheel)
		
		#Entry for English
		self.eEntry = Entry(frame, width=44)
		self.eEntry.grid(row=1, column=1)
		
		#Entry for Spanish
		self.sEntry = Entry(frame, width=44)
		self.sEntry.grid(row=2, column=1)
		
	def getValues(self): #Gets the values from inside the entry box
		try: #Needed if the boxes are empty
			return [self.eEntry.get(), self.sEntry.get()]
		except TclError:
			pass
	#Used for editing		
	def addValues(self, words): #Used for inserting values into the entries 
		eORs = 2 #Sorting variable
		for x in words: #Loops through the list of all words
			if eORs % 2 == 0: #English
				word = words[0] #Gets the word from the array
				#Puts it in the Entry slot
				self.eEntry.insert(END, word[3:len(word)])  
				eORs+=1
			else: #Spanish
				word = words[1] #Gets the word from the array
				#Puts it in the Entry slot
				self.sEntry.insert(END, word[3:len(word)])
				eORs+=1
			
	def onMouseWheel(self, event): #Scrolling event
		self.canvas.yview_scroll(event.delta, 'units')	