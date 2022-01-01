#%% Import libraries
from os import pathsep
import sys

#%% Dictionary of letter values
letterScores = {"A":1, 
                "B":4, 
                "C":4, 
                "D":2, 
                "E":1, 
                "F":4, 
                "G":3, 
                "H":3, 
                "I":1, 
                "J":10, 
                "K":5, 
                "L":2, 
                "M":4, 
                "N":2, 
                "O":1, 
                "P":4, 
                "Q":10, 
                "R":1, 
                "S":1, 
                "T":1, 
                "U":2, 
                "V":5, 
                "W":4, 
                "X":8, 
                "Y":3, 
                "Z": 10}

#%% Helper methods
def printBoard(board):
    print('\n'.join([board[ind:ind+N] for ind in range(0, len(board), N)]))
    
def createBoard():
    TL = {0,10,24,30,36,40,80,84,90,96,110,120}
    TW = {2,8,22,32,88,98,112,118}
    DW = {12,16,20,56,64,100,104,108}
    DL = {26,28,46,52,68,74,92,94}

    board = ""
    for i in range(NSquare):
        if(i in TL):
            board += "3"
        elif(i in TW):
            board += '9'
        elif(i in DW):
            board += '4'
        elif(i in DL):
            board += '2'
        else:
            board += '.'
    return board

def fillHoriz(board, pos, word):
    tempPos = pos-1
    while(tempPos >= 0 and board[tempPos] not in openChars and tempPos not in rightEdge): #Include anything connected to the left
        tempPos -= 1
    word = board[tempPos+1:pos] + word
    pos = tempPos + 1
    
    tempPos = pos + len(word)
    while(tempPos<NSquare and board[tempPos] not in openChars and tempPos not in leftEdge): #Include anything connected to the right
        tempPos += 1
    word += board[pos+len(word):tempPos]
    
    return pos,word

def fillVert(board, pos, word):
    tempPos = pos-N
    # include anything connected above
    while(tempPos >= 0 and board[tempPos] not in openChars):
        tempPos -= N
    word = board[tempPos+N:pos:N] + word
    pos = tempPos + N

    tempPos = pos+len(word)*N
    # include anything connected below
    while(tempPos < NSquare and board[tempPos] not in openChars):
        tempPos += N
    word += board[pos+len(word)*N:tempPos:N]
    
    return pos, word

def doMove(board,pos,dir,word): #Put given move onto board and return (new board, score for move)
    deltaPos = 1 if dir=="H" else N
    scoreSum = 0
    multipliers = 1
    for char in word:
        if(board[pos] == "9"):
            multipliers *= 3
            scoreSum += letterScores[char]
        elif(board[pos] == "4"):
            multipliers *= 2
            scoreSum += letterScores[char]
        elif(board[pos] == "3"):
            scoreSum += 3*letterScores[char]
        elif(board[pos] == "2"):
            scoreSum += 2*letterScores[char]
        elif(board[pos] == "." or board[pos] == char):
            scoreSum += letterScores[char]
        else:
            print("INVALID MOVE: Tried placing tile over a different tile")
            sys.exit(0)
        board = board[:pos] + char + board[pos+1:]
        pos += deltaPos
    return board, scoreSum*multipliers

def validMove(board, pos, dir, word):
    if(word not in allWords):
        return 0
    totalPoints = 0
    _, score = doMove(board, pos, dir, word)
    totalPoints += score
    if(dir == "H"):
        pos, word = fillHoriz(board, pos, word)
        for i in range(len(word)):
            newPos = pos+i
            if(board[newPos] not in openChars):
                continue
            startPos = newPos-N
            while(startPos>=0 and board[startPos] not in openChars):
                startPos -= N
            startPos += N
            
            endPos = newPos+N
            while(endPos<NSquare and board[endPos] not in openChars):
                endPos += N
            
            vertWord = board[startPos:newPos:N] + word[i] + board[newPos+N:endPos:N]
            if(len(vertWord)>1):
                if(vertWord not in allWords):
                    return False
                else:
                    _, score = doMove(board, startPos, "V", vertWord)
                    totalPoints += score
                
            
    if(dir == "V"):
        pos, word = fillVert(board, pos, word)
        for i in range(len(word)):
            newPos = pos+i*N
            if(board[newPos] not in openChars):
                continue
            startPos = newPos-1
            while(startPos>= 0 and startPos not in rightEdge and board[startPos] not in openChars):
                startPos -= 1
            startPos += 1
            
            endPos = newPos + 1
            while(endPos<NSquare and endPos not in leftEdge and board[endPos] not in openChars):
                endPos += 1
            
            horizWord = board[startPos:newPos]+word[i]+board[newPos+1:endPos]
            if(len(horizWord) > 1):
                if(horizWord not in allWords):
                    return False
                else:
                    _, score = doMove(board, startPos, "H", horizWord)
                    totalPoints += score
    return totalPoints


#%% Read Inputs
movesFile = open(sys.argv[1])
currHand = sys.argv[2].upper()
wordsFile = open("../scrabble.txt")
# movesFile = open("moves.txt")
# currHand = "ALQXECP"
# wordsFile = open("../scrabble.txt")

#%% Global variables
global allWords, openChars, leftEdge, rightEdge, topEdge, bottomEdge, N, NSquare
N = 11
NSquare = N**2
allWords = {word.strip().upper() for word in wordsFile}
openChars = set('.2349')
leftEdge = set(range(0, NSquare, N))
rightEdge = set(range(10, NSquare, N))
topEdge = set(range(0, N))
bottomEdge = set(range(NSquare-N, NSquare))


#%% Assemble Current Board
board = createBoard()
for line in movesFile:
    pos, dir, word, *_ = line.split(' ')
    pos = int(pos)
    word = word.strip().upper()
    score = validMove(board, pos, dir, word)
    print("Points Scored:", score)
    board,_ = doMove(board, pos, dir, word)
print("Starting Board:")
printBoard(board)
print()


#%% Build base openset for DFS
openset = [] #DFS list -- format of each element: (startPos, dir, wordSoFar, tilesLeftInHand)
for ind,char in enumerate(board):
    if(char in openChars):
        continue
    for newInd in [ind-1, ind+1, ind+N, ind-N]:
        if(newInd<0 or newInd>=NSquare):
            continue
        if(newInd==ind-1 and newInd in rightEdge):
            continue
        if(newInd==ind+1 and newInd in leftEdge):
            continue
        if(board[newInd] not in openChars):
            continue
        for i in range(len(currHand)):
            openset.append((newInd, "H", currHand[i], currHand[:i]+currHand[i+1:]))
            openset.append((newInd, "V", currHand[i], currHand[:i]+currHand[i+1:]))
        
    
#%% DFS Brute Force
closedSet = set()
possMoves = set() #list of all potential moves -- format of each element: (pointsFromMove, (pos, dir, word))
while openset:
    pos,dir,word,hand = openset.pop()
    if((score:=validMove(board, pos, dir, word))):
        if(not hand):
            score += 35
        possMoves.add( (score, (pos,dir,word)) )

    if(not hand):
        continue
    if(dir == "H"): #Word is being made horizontally
        pos, word = fillHoriz(board, pos, word)
        
        if(pos not in leftEdge): #try adding letter to the left
            newPos = pos-1
            while(board[newPos] not in openChars):
                newPos -= 1
                if(newPos in rightEdge or newPos<0): break
            if(newPos >= 0 and newPos not in rightEdge):
                tempWord = board[newPos+1:pos] + word
                for i in range(len(hand)):
                    tile = hand[i]
                    newWord = tile + tempWord
                    newHand = hand[:i] + hand[i+1:]
                    newNeighbor = (newPos, dir, newWord, newHand)
                    if(newNeighbor not in closedSet):
                        openset.append(newNeighbor)
                        closedSet.add(newNeighbor)
                    #(startPos, dir, wordSoFar, tilesLeftInHand)
                    
        if(pos+len(word)-1 not in rightEdge):  # try adding letter to the right
            newPos = pos+len(word)
            while(board[newPos] not in openChars):
                newPos += 1
                if(newPos in leftEdge or newPos>=NSquare):break
            if(newPos < NSquare and newPos not in leftEdge):
                tempWord = word + board[pos+len(word):newPos]
                for i in range(len(hand)):
                    tile = hand[i]
                    newWord = tempWord + tile
                    newHand = hand[:i] + hand[i+1:]
                    newNeighbor = (pos, dir, newWord, newHand)
                    if(newNeighbor not in closedSet):
                        openset.append(newNeighbor)
                        closedSet.add(newNeighbor)
                
    elif(dir == "V"): #word is being made vertically
        pos, word = fillVert(board, pos, word)
        
        if(pos not in topEdge):
            newPos = pos - N
            while(board[newPos] not in openChars):
                newPos -= N
                if(newPos < 0): break
            if(newPos >= 0):
                tempWord = board[newPos+N:pos:N] + word
                for i in range(len(hand)):
                    tile = hand[i]
                    newWord = tile + tempWord
                    newHand = hand[:i] + hand[i+1:]
                    newNeighbor = (newPos, dir, newWord, newHand)
                    if(newNeighbor not in closedSet):
                        openset.append(newNeighbor)
                        closedSet.add(newNeighbor)
                    
        if(pos+len(word)*N-N not in bottomEdge):
            newPos = pos + len(word)*N
            while(board[newPos] not in openChars):
                newPos += N
                if(newPos >= NSquare): break
            if(newPos < NSquare):
                tempWord = word + board[pos+len(word)*N:newPos:N]
                for i in range(len(hand)):
                    tile = hand[i]
                    newWord = tempWord + tile
                    newHand = hand[:i] + hand[i+1:]
                    newNeighbor = (pos, dir, newWord, newHand)
                    if(newNeighbor not in closedSet):
                        openset.append(newNeighbor)
                        closedSet.add(newNeighbor)
       
#%% Print out best possible moves                 
possMoves = sorted(list(possMoves), reverse=True)
for i,data in enumerate(possMoves[:20]):
    score, tup = data
    startPos, dir, word = tup
    print(f'{i+1}. {startPos}{dir} {word} -- Score: {score}')


    


