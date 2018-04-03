/*  	Name: Ryan Lanciloti
		Email: ryanjl9@iastate.edu
		CPRE 185 Section A  
		PP: 5

        <Reflection 1 What were you trying to learn or achieve?>
			So I didn't know what I should do and I was thinking about the cipher I made last week
			and thought about making a code cracking piece of software. Shortly after I realized
			that I'm not smart enough to do that so I went onto codeabby and explored some of the
			ideas and found mastermind. I used to play it on car rides and I figured it would be
			easy and fun to make so I just did that. I really didn't learn much but it was still fun
			to do.
		
        <Reflection 2 Were you successful? Why or Why not?>
			I was successful, I was able to make MasterMind in C. The only issue is that I was getting
			buffer overflow issues if the user entered any more than 5 characters and I couldn't figure
			out a way to fix that without going really far out of my way. I know if I expanded the buffer
			past 6, I wouldn't have to worry about the user putting in too many letters but they could still
			overload it. I tried using fgets but that was giving me weird results so I stopped messing with
			it.

		<Reflection 3 Would you do anything differently if starting this program over?  If so, explain what.>
			If I had to start over, I would probably try to fix the buffer overflow some how. I would also
			try to make the instructions easier for others to understand.
		
		<Reflection 4 Think about the most important thing you learned when writing this piece of code.  What was it and explain why it was significant.>
			The most important thing I leanred would have to be that pointers can't be used as *p++, it has
			to be p+=1 or else you get really weird results. I might also try to incorperate arrays into the
			program a bit more.

		<Other questions/comments for Instructors>
			As mentioned above, don't type too many letters or else you'll break the program. Otherwise
			this was a fun program to make. It's rather difficult to be honest. I recommend a game or two.
			
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

void init(int num[]);
void checkAnswer(char user[], int num[], int* p, int* o);

void main(){
	int num[5];
	char user[6];
	int right = 0;
	int counter = 0;
	
	int rightOverall = 0;
	int rightOrder = 0;
	
	srand(time(NULL));
	
	init(num);
	
	int x;
	
	printf("\t\tMastermind in C\n\t\tObjective: Guess the 5 digit code\n\t\tFeedback: (Correct Order-Correct number, wrong order)\n\n");
	
	while(!right && counter != 15){
		printf("\nMoves left (%d): Please input a 5 digit number guess > ", 15-counter);
		fflush(stdout);
		scanf("%s", user);
		if(strlen(user) == 5){
			checkAnswer(user, num, &rightOrder, &rightOverall);
			if(rightOrder == 5){
			printf("\n\t\tYOU WIN!!\n\n");
			break;
		}
			printf("%d-%d\n", rightOrder, rightOverall);
			rightOrder = 0;
			rightOverall = 0;
		}
		counter++;
	}
	if(counter == 15){
		printf("\n\t\tYou Lose - The right answer was ");
		int y;
		for(y = 0; y < 5; y++){
			printf("%d", num[y]);
		}
		printf("\n\n");
	}
}

void init(int num[]){
	int x;
	int y;
	for(x = 0; x < 5; x++){
		y = rand() % 10;
		num[x] = y;
	}
}

void checkAnswer(char user[], int num[], int* p, int* o){
	int x, y;
	int u;
	int blackList[5] = {-1};
	for(x = 0; x < 5; x++){
		u = user[x] - '0';
		if(u == num[x]){
			blackList[x] = 1;
			*p+=1;
		}else{
			blackList[x] = 0;
		}
	}
	
	for(x = 0; x < 5; x++){
		for(y = 0; y < 5; y++){
			u = user[x] - '0';
			if(num[y] == u && x!=y && blackList[y] != 1 && blackList[x] != 1){
				*o+=1;
				break;
			}
			//printf("%d - %d:%d:%d\n", x+1, u, num[y], *o);
		}
	}
}






