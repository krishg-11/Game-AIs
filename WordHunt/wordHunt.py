import sys

class TreeNode:
    def __init__(self, val, children = {}):
        self.val = val # character
        self.children = children # dictionary -> {value of subNode:subNode}
    
    def hasChildren(self):
        return len(self.children) > 0
    
## Import dictionary and build tree
filename = "../scrabble.txt"
head = TreeNode("_", {})
for line in open(filename):
    word = line.lower().strip()
    if (len(word) < 3):
        continue
    currNode = head
    for c in word:
        if (c not in currNode.children):
            currNode.children[c] = TreeNode(c, {})
        currNode = currNode.children[c]
    
dict = {line.lower().strip() for line in open(filename)} # can use set where key = first letter of word
dict = {x for x in dict if len(x) > 2}

## Get board from input and data validate
if (len(sys.argv) > 1):
    board = sys.argv[1]
else:
    board = input("What is your board: ")
# board = "EANEOHNDLRROTHTS"
board = board.lower()
assert len(board) == 16

## Globals
N = 4

topEdge = set(range(N))
bottomEdge = set(range(N**2 - N,N**2))
leftEdge = set(range(0, N**2, N))
rightEdge = set(range(N-1, N**2, N))

deltaPos = set()
for delta_r in [-1,0,1]:
    for delta_c in [-1,0,1]:
        if(delta_r == delta_c == 0):
            continue
        deltaPos.add(delta_r * N + delta_c)
        
deltaSansLeft = deltaPos - {-N-1, -1, N-1}
deltaSansRight = deltaPos - {-N+1, 1, N+1}

## DFS
output = []
openset = [(c, head.children[c], i, {i}, [i]) for i,c in enumerate(board)]
while openset:
    curr, node, pos, prev, path = openset.pop()
    if (curr in dict):
        output.append((curr, path))
    if (not node.hasChildren()):
        continue
    
    if(pos in leftEdge):
        delta_pos = deltaSansLeft
    elif(pos in rightEdge):
        delta_pos = deltaSansRight
    else:
        delta_pos = deltaPos
        
    for delta in delta_pos:
        new_pos = pos + delta
        if (new_pos < 0 or new_pos >= N**2 or new_pos in prev):
            continue
        new_char = board[new_pos]
        if (new_char not in node.children):
            continue
        new_node = node.children[new_char]
        new_word = curr + new_char
        new_prev = prev | {new_pos}
        new_path = path + [new_pos]
        openset.append((new_word, new_node, new_pos, new_prev, new_path))

clean_output = []
words = set()
for word, path in output:
    if (word in words):
        continue
    words.add(word)
    clean_output.append((word, path))
    
clean_output.sort(key=lambda x: len(x[0]))
for word,path in clean_output:
    path = " -> ".join(map(str, path))
    print(word, path, sep = "\t")
        


'''
1. Build dictionary tree
2. DFS -> openset = [(curr, treeNode, pos, {prevPos}, [path])]
    if curr is word --> add to output
    if treeNode has no kids: continue
    try all new positions:
        new_char = board[new_pos]
        new_word = curr + new_char
        new_node = treeNode.children[new_char]
        new_prev = prevPos | {pos}
        new_path = path + [pos]
        append to openset

'''
