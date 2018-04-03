#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

#define COMMENT //

void init(int x, int y, char grid[y][x]);
int isValid(int x, int y, int cc[2], int nc[2], char grid[y][x]);
void checkCell(int x, int y, int pv[x*y][2], int cc[2], char grid[y][x], int numIterations);
void printGrid(int x, int y, char grid[y][x]);
int checkSurround(int x, int y, int cc[2], int nc[2], char grid[y][x]);
int printI(char s[]);
char printc(char s[]);
int move(char k, int x, int y, char grid[x][y], int cc[]);
int check(int x, int y, char grid[y][x], int direction, int cc[]);

void main(){
	
	srand(time(NULL));
	
	printf("\n\n\t\tWelcome to Ryan Lanciloti's Maze Generator\n\n");
	
	int x = printI("Please input an x value (recommend 15) < 50: ");
	int y = printI("Please input a y value (recommend 15) < 50: ");
	int numIterations = printI("Please input a number of iterations (recommend x*y*10): ");
	
	int i, j;
	
	char grid[y][x];
	
	int preVis[x*y][2];
	int curCell[2] = {1,1};
	int playPos[2] = {1,1};
	
	char key = 'l';
	int score = 0;
	int condition;
	
	init(x, y, grid);
	checkCell(x, y, preVis, curCell, grid, numIterations);
	
	grid[1][1] = '@';
	grid[y-2][x-2] = '*';
	grid[y-3][x-2] = '%';
	grid[y-2][x-3] = '%';
	grid[y-3][x-3] = '%';
	
	printf("\n");
	printGrid(x, y, grid);
	
	while(key != 'q'){
		key = printc("Please input a key (w/a/s/d/h/q) > ");
		fflush(stdout);
		if(key != 'q'){
			printf("\t\t\t\t\tScore: %d\n", score);
			condition = move(key, x, y, grid, playPos);
			if(condition == 2){
				score+= x*y;
				init(x, y, grid);
				printGrid(x, y, grid);
				checkCell(x, y, preVis, curCell, grid, numIterations);
				
				playPos[0] = 1;
				playPos[1] = 1;
	
				grid[1][1] = '@';
				grid[y-2][x-2] = '*';
				grid[y-3][x-2] = '%';
				grid[y-2][x-3] = '%';
				grid[y-3][x-3] = '%';
	
				printf("\n");
				printGrid(x, y, grid);
			}
			printGrid(x, y, grid);
		}
	}
}

void init(int x, int y, char grid[y][x]){
	int i,j;
	
	for(i = 0; i < y; i++){
		for(j = 0; j < x; j++){
			grid[i][j] = '#';
		}
	}
	grid[1][1] = '%';
}

void checkCell(int x, int y, int pv[x*y][2], int cc[2], char grid[y][x], int numIterations){
	int nextCell = rand() % 4;
	int wrong = 0;
	
	int i = 0;
	int iter = 0;
	int backTrack = 0;
	
	while(iter < numIterations && i < x*y*20){
		////COMMENT printGrid(x, y, grid);
		i++;
		if(nextCell == 0 && isValid(x, y, cc, (int[]){2, 0}, grid) && grid[cc[1]][cc[0]+1] != '%'){
			//COMMENT printf("%d\n", nextCell);
			//COMMENT printf("RChar: %c\n", grid[cc[1]][cc[0]+1]);
			grid[cc[1]][cc[0]+1] = '%';
			iter++;
			nextCell = rand() % 4;
			pv[iter][0] = cc[0];
			pv[iter][1] = cc[1];
			cc = (int[]){cc[0]+1, cc[1]};
			wrong = 0;
			backTrack = 0;
		}else if(nextCell == 1 && isValid(x, y, cc, (int[]){0, 2}, grid) && grid[cc[1]+1][cc[0]] != '%'){
			//COMMENT printf("%d\n", nextCell);
			//COMMENT printf("DChar: %c\n", grid[cc[1]+1][cc[0]]);
			grid[cc[1]+1][cc[0]] = '%';
			iter++;
			nextCell = rand() % 4;
			pv[iter][0] = cc[0];
			pv[iter][1] = cc[1];
			cc = (int[]){cc[0], cc[1]+1};
			wrong = 0;
			backTrack = 0;
		}else if(nextCell == 2 && isValid(x, y, cc, (int[]){-2, 0}, grid) && grid[cc[1]][cc[0]-1] != '%'){
			//COMMENT printf("%d\n", nextCell);
			//COMMENT printf("LChar: %c\n", grid[cc[1]][cc[0]-1]);
			grid[cc[1]][cc[0]-1] = '%';
			iter++;
			nextCell = rand() % 4;
			pv[iter][0] = cc[0];
			pv[iter][1] = cc[1];
			cc = (int[]){cc[0]-1, cc[1]};
			wrong = 0;
			backTrack = 0;
		}else if(nextCell == 3 && isValid(x, y, cc, (int[]){0, -2}, grid) && grid[cc[1]-1][cc[0]] != '%'){
			//COMMENT printf("%d\n", nextCell);
			//COMMENT printf("UChar: %c%c%c\n", grid[cc[1]-1][cc[0]-1], grid[cc[1]-1][cc[0]], grid[cc[1]-1][cc[0]+1]);
			grid[cc[1]-1][cc[0]] = '%';
			iter++;
			nextCell = rand() % 4;
			pv[iter][0] = cc[0];
			pv[iter][1] = cc[1];
			cc = (int[]){cc[0], cc[1]-1};
			wrong = 0;
			backTrack = 0;
		}else{
			//COMMENT printf("Wrong: %d\n", wrong);
			if(wrong < 4){
				wrong++;
				if(nextCell == 3){
					nextCell = 0;
				}else{
					nextCell++;
				}
			}else{
				//COMMENT printf("Back Track: %d:%d -> %d:%d\n", cc[0], cc[1], pv[iter-backTrack][0], pv[iter-backTrack][1]);
				cc[0] = pv[iter-backTrack][0];
				cc[1] = pv[iter-backTrack][1];
				wrong = 0;
				backTrack++;
			}
		}
		//COMMENT printf("I: %d Iter: %d PV: %d:%d\n", i, iter, pv[iter-1][0], pv[iter-1][1]);
		//printGrid(x, y, grid);
		//printf("%d, %d", cc[0], cc[1]);
	}
}
int isValid(int x, int y, int cc[2], int nc[2], char grid[y][x]){
	//COMMENT printf("CC: %d:%d NC: %d:%d x:%d y:%d\n", cc[0], cc[1], nc[0], nc[1], x, y);
	if(cc[0] + nc[0] >= 0 && cc[0] + nc[0] < x && cc[1] + nc[1] >= 0 && cc[1] + nc[1] < y){
		if(grid[cc[1]+nc[1]][cc[0]+nc[0]] != '%' & checkSurround(x, y, cc, nc, grid)){
			//COMMENT printf("TChar: %c\n", grid[cc[1]+nc[1]][cc[0]+nc[0]]);
			return 1;
		}
	}else{
		//COMMENT printf("FChar: %c\n", grid[cc[1]+nc[1]][cc[0]+nc[0]]);
		return 0;
	}
}
void printGrid(int x, int y, char grid[y][x]){
	int i,j;

	for(i = 0; i < y; i++){
		for(j = 0; j < x; j++){
			if(grid[i][j] == '#'){
				printf("%s%c", "\x1B[31m", grid[i][j]);
			}else if(grid[i][j] == '%'){
				printf("%s%c", "\x1B[36m", grid[i][j]);
			}else if(grid[i][j] == '@'){
				printf("%s%c", "\x1B[33m", grid[i][j]);
			}else if(grid[i][j] == '*'){
				printf("%s%c", "\x1B[32m", grid[i][j]);
			}
		}
		printf("\n");
	}
}
int checkSurround(int x, int y, int cc[2], int nc[2], char grid[y][x]){
	if(nc[1] == 2){
		if(grid[cc[1]+1][cc[0]-1] == '#' && grid[cc[1]+1][cc[0]+1] == '#' && grid[cc[1]+1][cc[0]] == '#'){
			//COMMENT printf("Approaching from top\n");
			return 1;
		}else{
			//COMMENT printf("Not Valid - CC: %d:%d NC: %d:%d\n", cc[0], cc[1], nc[0], nc[1]);
			return 0;
		}
	}else if(nc[1] == -2){
		if(grid[cc[1]-1][cc[0]-1] == '#' && grid[cc[1]-1][cc[0]+1] == '#' && grid[cc[1]-1][cc[0]] == '#'){
			//COMMENT printf("Left: %c (%d, %d) Right: %c (%d, %d)\n", grid[cc[1]][cc[0]-1], cc[0], cc[1]-1, grid[cc[1]][cc[0]+1], cc[0], cc[1]+1);
			//COMMENT printf("Approaching from bottom\n");
			return 1;
		}else{
			//COMMENT printf("Not Valid - CC: %d:%d NC: %d:%d\n", cc[0], cc[1], nc[0], nc[1]);
			return 0;
		}
	}else if(nc[0] == 2){
		if(grid[cc[1]-1][cc[0]+1] == '#' && grid[cc[1]+1][cc[0]+1] == '#' && grid[cc[1]][cc[0]+1] == '#'){
			//COMMENT printf("Approaching from left\n");
			return 1;
		}else{
			//COMMENT printf("Not Valid - CC: %d:%d NC: %d:%d\n", cc[0], cc[1], nc[0], nc[1]);
			return 0;
		}
	}else if(nc[0] == -2){
		if(grid[cc[1]-1][cc[0]-1] == '#' && grid[cc[1]+1][cc[0]-1] == '#' && grid[cc[1]][cc[0]-1] == '#'){
			//printf("Above: %c (%d, %d) Below: %c (%d, %d)\n", grid[cc[1]][cc[0]-1], cc[0], cc[1]-1, grid[cc[1]][cc[0]+1], cc[0], cc[1]+1);
			//COMMENT printf("Approaching from right\n");
			return 1;
		}else{
			//COMMENT printf("Not Valid - CC: %d:%d NC: %d:%d\n", cc[0], cc[1], nc[0], nc[1]);
			return 0;
		}
	}else{
		//COMMENT printf("Not Valid - CC: %d:%d NC: %d:%d\n", cc[0], cc[1], nc[0], nc[1]);
		return 0;
	}
	//COMMENT printf("Error\n");
}
int printI(char s[]){
	int v;
	printf(s);
	fflush(stdout);
	scanf(" %d", &v);
	printf("\n");
	return v;
}
char printc(char s[]){
	char v;
	printf(s);
	fflush(stdout);
	scanf(" %c", &v);
	printf("\n");
	return v;
}
int move(char k, int x, int y, char grid[y][x], int cc[]){
	int condition;
	if(k == 'w'){
		condition = check(x, y, grid, 0, cc);
		if(condition == 1){
			grid[cc[1] - 1][cc[0]] = '@';
			grid[cc[1]][cc[0]] = '%';
			cc[1] -= 1; 
			return 1;
		}else if(condition == 2){
			return 2;
		}
	}else if(k == 'a'){
		condition = check(x, y, grid, 1, cc);
		if(condition == 1){
			grid[cc[1]][cc[0]-1] = '@';
			grid[cc[1]][cc[0]] = '%';
			cc[0] -= 1;
			return 1;
		}else if(condition == 2){
			return 2;
		}
	}else if(k == 's'){
		condition = check(x, y, grid, 2, cc);
		if(condition == 1){
			grid[cc[1] + 1][cc[0]] = '@';
			grid[cc[1]][cc[0]] = '%';
			cc[1] += 1;
			return 1;
		}else if(condition == 2){
			return 2;
		}
	}else if(k == 'd'){
		condition = check(x, y, grid, 3, cc);
		if(condition == 1){
			grid[cc[1]][cc[0]+1] = '@';
			grid[cc[1]][cc[0]] = '%';
			cc[0] += 1;
			return 1;
		}else if(condition == 2){
			return 2;
		}
	}else if(k == 'h'){
		printf("w: up\na: left\ns: down\nd: right\nh: help\nq: quit\n\n");
	}else if(k == 'n'){
		return 3;
	}
}
int check(int x, int y, char grid[y][x], int direction, int cc[]){
	if(direction == 0){
		if(grid[cc[1] - 1][cc[0]] != '#' &&grid[cc[1] - 1][cc[0]] != '*'){
			return 1;
		}else if(grid[cc[1] - 1][cc[0]] == '*'){
			return 2;
		}else{
			return 0;
		}
	}else if(direction == 1){
		if(grid[cc[1]][cc[0]-1] != '#' &&grid[cc[1]][cc[0]-1] != '*'){
			return 1;
		}else if(grid[cc[1]][cc[0] + 1] == '*'){
			return 2;
		}else{
			return 0;
		}
	}else if(direction == 2){
		if(grid[cc[1]+1][cc[0]] != '#' &&grid[cc[1] + 1][cc[0]] != '*'){
			return 1;
		}else if(grid[cc[1] + 1][cc[0]] == '*'){
			return 2;
		}else{
			return 0;
		}
	}else if(direction == 3){
		if(grid[cc[1]][cc[0]+1] != '#' &&grid[cc[1]][cc[0]+1] != '*'){
			return 1;
		}else if(grid[cc[1]][cc[0]+1] == '*'){
			return 2;
		}else{
			return 0;
		}
	}
}







