/*  	Name: Ryan Lanciloti
		Email: ryanjl9@iastate.edu
		CPRE 185 Section A  
		PP: 3

        <Reflection 1 What were you trying to learn or achieve?>

            So since I needed to use 2D arrays, I decided why not do some sort of cipher.
			When I was younger I was really into this idea and so I decided why not write
			a program to create a vigenere cipher.

        <Reflection 2 Were you successful? Why or Why not?>

			I was mostly successful. Inorder to make this practical, I had to sacrifice 
			the possibility of a UI which I didn't really like. I could have used the fopen
			to read a file but checking to see if the file existed or not would have been 
			too much of a pain.

		<Reflection 3 Would you do anything differently if starting this program over?  If so, explain what.>

			Using a 2D array was stupid. I could have easily offest the characters from adding and subracting
			chars. There was probably something I could have done better instead of a cipher but
			I really wanted to do this.

		<Reflection 4 Think about the most important thing you learned when writing this piece of code.  What was it and explain why it was significant.>

			I learned fgets and how to read in a line of text. I also learned that having two string both
			with a limit of 2^20 is bad bad bad. I couldn't printf to print simple text. It worked when I 
			had one variable that big, but the second one was a no go.

		<Other questions/comments for Instructors>
			
			!!!You NEED to take out all tabs from blocks of text, they do not work well for some reason.
			The only thing this thing can handel is '\n' characters, that's it.!!!
			
			So I decided to make this both encrypt and decrypt messages, because I figured it was useless without
			both. Since I had to sacrifice UI for the ability to just read in input, it's not that intuitive to use.
			
			Step 1: Create a file, lets call it "test.txt"
			Step 2: Put the keyword used for the encryption on the first line (It has to be one word).
			Step 3: Put the text you want to encrypt on the lines underneath the the keyword. The max
					size is 1024 characters per line.
			Step 4: Open the c file and make sure the function variable is set to 1
			Step 5: Compile the program
			Step 6: Run this command: "./program.exe < test.txt > out.txt"
			
			At this point the file is encrypted and ready to be distributed. Decrypting the file is much like 
			encrypting, just a few different steps.
			
			Step 1: Take the encrypted file, or "out.txt", whatever it was named.
			Step 2: Go to the top of the file and put the keyword ALONE on the first line.
			Step 3: Save and close the file
			Step 4: Open the c file and make sure the function variable is set to 0
			Step 4: Complile the program
			Step 5: Run this command: "./program.exe < out.txt > decrypt.txt"
			
			The keyword can be up to 100 characters long and it doesn't have to be an actual word, just a string
			or characters. This isn't a turn vigenere cipher as I couldn't figure out how to concantinate or append
			to the end of a string. The keyword starts over every new line. This means that any keyword longer than
			your longest line of text will not be utilized.
			
			Also it is smart to compile this program twice, once with the function set to 1 and another with
			the function set to 0. "decrypt.exe" and "encrypt.exe" for instance.
			
			I tried encrypting the first chapter of white fang and it didn't read any of the lines with quotes in
			them. I don't know why that is but I think it might have to do with fgets.
*/

#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define SIZE 1024

//vigenere cipher

void encrypt(char mes[], char mesKey[], char cip[27][27], char nMes[]);
void initC(char cipher[27][27]);
void initK(char keyword[], char mesKey[], int size);
void decrypt(char mes[], char mesKey[], char cip[27][27], char nMes[]);

void main(){
	
	int function = 0;
	
	char dump;
	char mes[SIZE];
	char mesKey[SIZE];
	char nMes[SIZE];
	
	char cipher[27][27];
	char keyword[101];
	
	initC(cipher);
	scanf("%s", keyword);

	if(function){
		while(!feof(stdin)){
			fgets(mes, SIZE, stdin);
			if(mes[strlen(mes)-1] == '\n'){
				mes[strlen(mes)-1] = '\0';
			}
			initK(keyword, mesKey, strlen(mes));
			encrypt(mes, mesKey, cipher, nMes);
			if(isalpha(nMes[0])){
				printf("%s\n", nMes);
			}
		}
	}else{
		while(!feof(stdin)){
			fgets(mes, SIZE, stdin);
			if(mes[strlen(mes)-1] == '\n'){
				mes[strlen(mes)-1] = '\0';
			}
			initK(keyword, mesKey, strlen(mes));
			decrypt(mes, mesKey, cipher, nMes);
			if(isalpha(nMes[0]) && !feof(stdin)){
				printf("%s\n", nMes);
			}
		}
	}
}

void initC(char cipher[27][27]){
	int x, y;
	
	for(y = 0; y < 26; y++){
		for(x = 0; x < 26; x++){
			if(y+x > 25){
				cipher[y][x] = 'a'+x+y-26;
			}else{
				cipher[y][x] = 'a'+x+y;
			}
		}
	}
}

void initK(char keyword[], char mesKey[], int size){
	int x;
	int count = 0;
	if(size == 0){
		return;
	}
	
	for(x = 0; x < size; x++){
		if(count < strlen(keyword)-1){
			mesKey[x] = keyword[count];
			count++;
		}else{
			mesKey[x] = keyword[count];
			count = 0;
		}
	}
	mesKey[size] = '\0';
}

void encrypt(char mes[], char mesKey[], char cip[27][27], char nMes[]){
	int x;
	for(x = 0; x < strlen(mes); x++){
		if(isalpha(mes[x])){
			nMes[x] = cip[tolower(mes[x]) - 97][tolower(mesKey[x]) - 97];
		}else{
			nMes[x] = mes[x];
		}
	}
	nMes[strlen(mes)] = '\0';
}

void decrypt(char mes[], char mesKey[], char cip[27][27], char nMes[]){
	int x;
	int i, j;
	for(x = 0; x < strlen(mes); x++){
		if(isalpha(mes[x])){
			for(i = 0; i < 26; i++){
				if(cip[tolower(mesKey[x])-97][i] == tolower(mes[x])){
					nMes[x] = cip[0][i];
				}
			}
		}else{
			nMes[x] = mes[x];
		}
	}
	nMes[strlen(mes)] = '\0';
}








