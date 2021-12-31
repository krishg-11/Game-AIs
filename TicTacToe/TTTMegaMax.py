import sys
global constraints
import msvcrt

global humTkn
humTkn = "a"
board = "........."
for x in sys.argv[1:]:
    x = x.upper()
    if(x == "X" or x == "O"):
        humTkn = x
    else:
        assert len(x) == 9
        assert len(list(filter(lambda char: char in "XO.", x))) == 9
        board = x
global N
N = int(len(board)**0.5)
rows = [set(range(x,x+N)) for x in range(0,len(board),N)]
cols = [set(range(x,len(board),N)) for x in range(N)]
diag1 = set(range(0,len(board),N+1))
diag2 = set(range(N-1,len(board)-1,N-1))
diags = [diag1,diag2]


constraints = rows+cols+diags
def possMoves(board):
    return({p for p,val in enumerate(board) if val=="."})

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

def megaMax(board, tkn):
    eg = endGame(board)
    if (eg == 0): return {"W":set(),"L":set(), "D":board} #returning board is dummy, just needs to be non-empty
    elif (eg == 1 or eg == -1): return {"W":set(), "L":board, "D":set()}
    res = {"W":set(), "L":set(), "D":set()}
    for move in possMoves(board):
        newBrd = board[:move] + tkn + board[move+1:]
        Mm = megaMax(newBrd, flipToken(tkn))
        if(Mm["W"]):
            brdCat = "L"
        elif(Mm["D"]):
            brdCat = "D"
        elif(Mm["L"]):
            brdCat = "W"

        res[brdCat].add(move)
    return res

def input():
    spot = msvcrt.getch()
    try:
        spot = int(spot)
    except:
        pass
    return spot

def flipToken(tkn):
    return "X" if tkn == "O" else "O"

def output(board):
    global N
    for i in range(0,len(board),N):
        print(board[i:i+N])
    print()

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

def compMove(board):
    global humTkn
    options = megaMax(board, flipToken(humTkn))
    print(options)
    if(options["W"]):
        spotNow = options["W"].pop()
    elif(options["D"]):
        spotNow = options["D"].pop()
    else:
        spotNow = options["L"].pop()
    board = board[:spotNow] + flipToken(humTkn) + board[spotNow+1:]
    return board


count = 0
for x in board:
    if(x=="X"):count+=1
    elif (x=="O"):count-=1
tkn = "X" if count<=0 else "O"
if(humTkn=="a"):
    humTkn = flipToken(tkn)

print("You are", humTkn, "and I am", flipToken(humTkn))
print()
print("Indexing Scheme:")
output("012345678")

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

