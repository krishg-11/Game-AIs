#%% Import libraries
import sys
import msvcrt

#%% Input board/player or use default values + data validation
global humTkn
humTkn = "O"
board = "........."
for x in sys.argv[1:]:
    x = x.upper()
    if(x == "X" or x == "O"):
        humTkn = x
    else:
        assert len(x) == 9
        assert len(list(filter(lambda char: char in "XO.", x))) == 9
        board = x
#%% Define Global Variables
global N
N = int(len(board)**0.5)
rows = [set(range(x,x+N)) for x in range(0,len(board),N)]
cols = [set(range(x,len(board),N)) for x in range(N)]
diag1 = set(range(0,len(board),N+1))
diag2 = set(range(N-1,len(board)-1,N-1))
diags = [diag1,diag2]

global constraints
constraints = rows+cols+diags

#%% return set of possible moves (open positions)
def possMoves(board):
    return({p for p,val in enumerate(board) if val=="."})

#%% Return winner of game if game is over (1=X win, -1=O win, 0=draw, ""=game not over)
def endGame(pzl):
    global constraints
    for cs in constraints:
        csVals = {pzl[x] for x in cs}
        spot = csVals.pop()
        if(len(csVals)==0 and spot!="."):
            return 1 if spot == "X" else -1
    if("." not in pzl):
        return 0
    return ""

#%% Run minimax
def minimax(board, tkn): #return a dict of {move:board evaluation (1,0,-1)}
    eg = endGame(board)
    if eg != "": return {-1:eg}

    rst = {}
    for move in possMoves(board):
        newBrd = board[:move] + tkn + board[move+1:]
        newTkn = flipToken(tkn)
        mmx = minimax(newBrd, newTkn)
        brdEval = min(mmx.values()) if tkn == "X" else max(mmx.values())
        rst[move] = brdEval
    return rst

#%% Take in user input 
def input():
    spot = msvcrt.getch()
    try:
        spot = int(spot)
    except:
        pass
    return spot

#%% Flip current token
def flipToken(tkn):
    if(tkn =="X"): return("O")
    else:  return("X")

#%% Output board aesthetically
def output(board):
    global N
    for i in range(0,len(board),N):
        print(board[i:i+N])
    print()

#%% Take in move input, validate, and do move on board
def humanMove(board):
    print("What is your move?")
    empties = possMoves(board)
    spot = input()
    while(spot not in empties):
        if(spot == b'\x1b'):
            sys.exit()
        print("Not possible move, try again")
        spot = input()
    board = board[:spot] + tkn + board[spot+1:]
    return board

#%% Computer does best possible move
def compMove(board):
    global humTkn
    options = minimax(board, flipToken(humTkn))
    print(options)
    optionsTuple = [(options[spot], spot) for spot in options]
    spotNow = max(optionsTuple)[-1] if humTkn == "O" else min(optionsTuple)[-1]
    board = board[:spotNow] + flipToken(humTkn) + board[spotNow+1:]
    return board

#%% Instantiating game
count = 0
for x in board:
    if(x=="X"):count+=1
    elif (x=="O"):count-=1
tkn = "X" if count<=0 else "O"

print("You are", humTkn, "and I am", flipToken(humTkn))
print()
print("Indexing Scheme:")
output("012345678")

#%% Play game until over
while(endGame(board)==""):
    output(board)
    if(tkn == humTkn):
        board = humanMove(board)
    else:
        board = compMove(board)

    tkn = flipToken(tkn)

output(board)
eg = endGame(board)
if(eg == 0):
    print("DRAW")
elif(eg == 1):
    print("X WINS")
else:
    print("O WINS")

#print(minimax(board))


#X ALWAYS GOES FIRST
#given board, find all possible positions for next move (all empty spots -- trivial)
#given board, find out if at end of game (X wins, O Wins, Draw)
#Compute # of distinct games possible (Order matters)
#Compute # of distinct end boards possible (how many where 1.X wins 2.O Wins 3.Draw)
    #3 set of all distinct games possible (1 where all X wins, all O wins, all Draws)
#

#Play a game with a human (recieve no input, or recieve token (X or O, token that human is using), or starting board)
#Assume empty board or computer is next move if not given
#Play game to completion
#Computer playing to win
#Display board (3x3)

#Computer makes move --> displays --> pauses and asks for user input --> tells who win at end
#exit if user hits esc key
#user inputs index position (0-8, no enter key)
#not input function


#minimum level should always achieve(assume facing another perfect player who will always make best choice)
#Assume function tells us for every possible move the outcome of the game (both players play perfectly)
#   Can we then write such a function in terms of itself?
#1 means X wining, 0 means tie, -1 means O winning
#def MINIMAX/classifyMoves(board): #return a dict of {move:board evaluation (1,0,-1)}
    #if board is terminal: return {-1:(1,0,-1)}
    #tkn = "X" or "O" #tkn of player to move next
    #resultsDct = {}
    #for move in allMoves:
        #newBrd = #bard after tkn inputted
        #mmx = minimax(newBrd)
        #brdEvaluation = max(mmx.values()) if tkn == "X" else min(mmx.values())

# %%
