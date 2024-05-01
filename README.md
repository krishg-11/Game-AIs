# Game-AIs
AI bots to play various games and solve puzzles (Sudoku, WordsWithFriends, etc.). Never lose to your friends again! Use these bots to play the perfect game every time. DISCLAIMER: I am not responsible for you losing your friends because you took the fun out of the game by using an AI bot to beat them.

"scrabble.txt" holds the dictionary of words that is shared across all programs. This can be replaced by another dictionary of words in the same format (programs are not case-sensitive). 

## Anagrams
This program is used to play the GamePigeon game Anagrams. When the program runs it will ask for an input which will be the sequence of letters that you have. The program will then output all the possible words that can be made from these letters, which you can input into the game.

## Sudoku
This program can be used to solve a Sudoku puzzle. The puzzle can be passed as a command line argument but if it is omitted then the user will be prompted for input. The program will output the solved board with all blanks filled in, if the given board is solvable. 

### Input format
The input should match the sudoku board with blanks represented by a period (".") and a standard symbol set ranging from 1-9 followed by A-Z. Generally, for 9x9 sudoku boards only symbols 1-9 will be used. The board should be flattened and passed in as a string e.g. a 9x9 board would be passed in as an 81-character string. 

Sample inputs are provided in the given files

## TicTacToe
The program will play the game Tic-Tac-Toe perfectly. The program can take up to 2 command line arguments. The first argument is the user's choice of which token they would like to be (X or O); default is O. The second argument is a given starting board; the default is a blank board ("........."). Both arguments are optional.

X is the first to play. Whenever it is the user's turn, the program will prompt the user for where they would like to make their move. The positions are represented by the indexing scheme displayed by the program ranging from 0-9. This is more intuitive to understand when the program runs.

Note that two varying algorithms (minimax and negamax) are provided but they work the same from the user's perspective. The difference in the algorithms lies in the perspective of the program as it plays the game. These algorithms are identical in performance/efficiency. 

## Word Bites
This program is used to play the GamePigeon game Word Bites. Input can be passed as a command line argument but if it is omitted then the user will be prompted for input. There are 3 required inputs:
1. The single blocks you are given. The single blocks should be given as 1-character letters that are comma separated.
2. The horizontal blocks you are given. The left-most character goes first then the right-most. The horizontal blocks should be given as 2-character sequences that are comma separated
3. The vertical blocks you are given. The top character goes first then the bottom. The vertical blocks should be given as 2-character sequences that are comma separated

The program will output all the words that you can make with the given blocks. The outputted words are sorted so that the longest words are printed out last. Since most command lines auto-scroll with output, this makes it easy to start from the bottom and work up. This way, you can input the largest words and get the most points quickly.

## WordHunt
This program is used to play the GamePigeon game Word Hunt. Input can be passed as a command line argument but if it is omitted then the user will be prompted for input. The input should represent the given board as a sequence of 16 characters. The program will then output all the possible words that can be made from the board as well as the path used to make these words (so it easy for the user to find on their screen). The outputted words are sorted so that the longest words are printed out last. Since most command lines auto-scroll with output, this makes it easy to start from the bottom and work up. This way, you can input the largest words and get the most points quickly.

## Wordle
The wordle_player.py script is used to play the NYT game Wordle. The program asks for what word you guessed and what the outcome of that guess was. From this information, it provides you with a few options for the best next guess.

Since the optimal first guess does not change game-to-game, a separate script wordleFirstWord.py finds the optimal first word. The results of this script are stored in first_guess.json. According to the program, the best first guess is "roate." 

The wordle_performance.py script is an exploratory script that analyzes the performance of our wordle bot by testing it against all potential wordle games. The current wordle bot solves a wordle game in an average of 3.495 guesses. It also keeps track of the number of times each word is guessed by the AI. These results are stored in guess_counts.json. Other interesting details about the bot's guesses are shown at the bottom of the file.

The wordle_functions.py script stores the meat of the code but can not be run on its own. All other scripts use the functions in wordle_functions.py.

## WordsWithFriends
This program is used to play the game Words with Friends (similar to Scrabble). It takes in two command line inputs (detailed below). It then prints out the best possible moves that the user can make with their current hand and the number of points that each move will give the user. 
### Inputs
The first input is a file name for a file that contains the sequence of moves thus far in the game. A sample moves file is given in moves.txt. This is used to construct the current board. Each move goes on its own line and consists of three, space-separated parts:
1. The position of the first letter of the word (indexed with 0 as the top-left of the board and 120 as the bottom-right)
2. The direction of the word (H for horizontal or V for vertical)
3. The word itself

The second input is the user's current hand, represented as a sequence of the letters in the hand.
