#Written by Ryan Lanciloti

#In charge of most of the logic and heavy lifting 

import random, guiController, os

#The spanish and english lists
englishList = []
spanishList = []

#Goes into the lists directory and finds all the lists and puts them in their respective array's
def listSelecter(list, length):
	#Opens the file
	os.chdir('lists')
	with open(list+'.txt', "r") as file:
		#bufferlist holds one spanish and one english word
		bufferlist = []
		#Place holder variables, to be assigned later
		englishWord = ''
		spanishWord = ''
		#Loop that will go until it reaches the end of the file
		for x in range(0,length):
			line = file.readline()
			bufferlist.append(line)
			if len(bufferlist) == 2:
				"""If bufferlist has to words, then it checks to see if the first letter is
				an 'e' and if so then it appends it to englishList after removing the new line
				short-cut and the \r short-cut (unknown what \r does) and vice versa for 's'."""
				for check in bufferlist:
					#Checks for 'e'
					checklen = check[0:1]
					if checklen == 'e':
						checkWordLength = len(check)
						#Removes the 'e: ' from the beginning
						englishWord = check[3:checkWordLength]
						#Remove the word from the bufferlist
						bufferlist.remove(check)
						#Removes escape characters
						nenglishWord = englishWord.rstrip("\n")
						#Also appends the word to englishList
						englishList.append(nenglishWord.rstrip('\r'))
					#Checks for 's'
					elif checklen == 's':
						checkWordLength = len(check)
						#Removes the 's: ' from the beginning
						spanishWord = check[3:checkWordLength]
						#Removes the word from the buffer list
						bufferlist.remove(check)
						#Removes escape characters
						nspanishWord = spanishWord.rstrip("\n")
						#Also appends the word to spanishList
						spanishList.append(nspanishWord.rstrip('\r'))

#Randomizes the order in which the words are displayed
def randomList():
    numList = []
    while len(numList) != len(spanishList):
    	#If you don't subtract 1, the index will be out of range (due to arrays starting at 0 instead of 1)
        y = random.randint(0, len(spanishList)-1)
        if y not in numList:
            numList.append(y)
    return numList

#Quizes the user and shows them what they got wrong
def EorS_return(inputs):
	#Buffer variables to hold values later
    i = 0
    b = 0
    #Array of wrong answers and the correct ones
    wrongAnswers = []
    words = [] #The word they answered for
    #Random list order
    numList = randomList()
    lenofList = len(numList)
    if inputs == 'english':
    	#Loop that waits until the entire list has been cycled through
        while lenofList:
        	#Gets a word to quiz with
            for x in numList:
            	#Lowers the length of the list
                lenofList -= 1
                #Gets the users answer 
                userAnswer = guiController.userQuestion(englishList[x])
                if userAnswer == None:
                	return 
                else:
					"""If they got it wrong then it will put it in the wrong answers array, along with
					the correct answer"""
					if userAnswer != spanishList[x]:
						#b is whether you have a wrong answer or not
						b += 1
						wrongAnswers.append(userAnswer)
						wrongAnswers.append(spanishList[x]) 
						words.append(englishList[x])
        #After the it's done asking for answers, it shows the user their wrong answers  
        else:
        	#b is the number of wrong answers so if it's more than 0, it tells you what you got wrong
            if b > 0:
                guiController.wrongAnswer(wrongAnswers, words)
    elif inputs == 'spanish':
    	#Loop that waits until the entire list has been cycled through
        while lenofList:
        	#Gets a word to quiz with
            for x in numList:
            	#Lowers the length of the list
                lenofList -= 1
                #Gets the users answer 
                userAnswer = guiController.userQuestion(spanishList[x])
                if userAnswer == None:
                	return
                else:
					"""If they got it wrong then it will put it in the wrong answers array, along with
					the correct answer"""
					if userAnswer != englishList[x]:
						#b is whether you have a wrong answer or not
						b += 1
						wrongAnswers.append(userAnswer)
						wrongAnswers.append(englishList[x])
						words.append(spanishList[x])
        #After the it's done asking for answers, it shows the user their wrong answers 
        else:
        	#b is the number of wrong answers so if it's more than 0, it tells you what you got wrong
            if b > 0:
                guiController.wrongAnswer(wrongAnswers, words)