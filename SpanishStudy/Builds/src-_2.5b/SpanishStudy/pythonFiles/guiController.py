#Written by Ryan Lanciloti

#What controls all of the GUI's 

import easygui, listChecker, __main__
import TkinterGUI as tk

#Easy default title
title = 'Spanish Study'
#Enables easyGUI or Tkinter
easyGUI = False

#Prompts the user for spanish or english quizzing
def startup():
	if easyGUI == True:
		x = easygui.buttonbox(msg = 'Please select whether you want to be' +
		' quized in either Spanish or English', title = title, choices=('Spanish', 'English'))
		if x =='Spanish':
			return 'spanish'
		elif x == 'English':
			return 'english'
	else:
		var = tk.Startup()
		if var.close != True:
			return var.answer

#List of all possible lists the be quizzed from
def selectList():
	if easyGUI == True:
		y = listChecker.validObject()
		x = easygui.choicebox(msg = 'Please select a list of words'\
		, title = title, choices = y)
		return x
	else:
		var = tk.SelectList(listChecker.validObject())
		if var.close != True:
			return var.answer
		
#The box that the user uses to type their answer
def userQuestion(languageValue):
	if easyGUI == True:
		x = easygui.enterbox(msg = "Enter the word for " + languageValue, title = title)
		return x
	else:
		var = tk.UserQuestion(languageValue)
		if var.close != True:
			return var.answer
			
#Tells the user what answers were wrong
def wrongAnswer(x, word):
	if easyGUI == True:
		c = 2
		eng = ''
		spanish = ''
		leng = len(x)
		for y in x:
			if c % 2 == 0:
				eng = x[c-2]
				c += 1
			else:
			   spanish = x[c-2]
			   c += 1
			   texbox = easygui.msgbox('You put %s instead of %s\n for %s' % (eng, spanish, word[c-2]))
			   eng = ''
			   spanish = ''
	else:	
		c = 2
		eng = ''
		spanish = ''
		leng = len(x)
		for y in x:
			if c % 2 == 0:
				eng = x[c-2]
				c += 1
			else:
			   spanish = x[c-2]
			   c += 1
			   var = tk.WrongAnswer(eng, spanish, word[(c/2)-2])
			   if var.clear != True:
			   	   return 
			   else: 
				   eng = ''
				   spanish = ''		   