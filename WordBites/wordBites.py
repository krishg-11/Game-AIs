#%% Import Libraries
import sys

#%% Define TreeNode Class
class TreeNode:
    def __init__(self, val, children = {}):
        self.val = val # character
        self.children = children # dictionary -> {value of subNode:subNode}
    
    def hasChildren(self):
        return len(self.children) > 0
    
def getChildren(node, childs):
    for child in childs:
        if child not in node.children:
            return None
        node = node.children[child]
    return node
          
#%% Read in dictionary and build tree
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

#%% Take in input and data validate
if (len(sys.argv) == 4):
    single = sys.argv[1].split(",")
    horiz = sys.argv[2].split(",")
    vert = sys.argv[3].split(",")
else:
    single = input("List all single blocks: ").split(",")
    horiz = input("List all horizontal blocks: ").split(",")
    vert = input("List all vertical blocks: ").split(",")

assert all(len(x) == 1 for x in single)
assert all(len(x) == 2 for x in vert)
assert all(len(x) == 2 for x in horiz)
    
# single = ["A", "E", "N", "D"]
# horiz = ["BC", "OP", "JK", "FG"]
# vert = ["LM", "HI"]

#%% Build globals
single = [(char.lower(), 0) for char in single]
horiz = [(chars.lower(), 1) for chars in horiz]
vert = [(chars.lower(), 2) for chars in vert]

blocks = single + horiz + vert

#%% Build openset for DFS
openset = []
for i,(chars, dir) in enumerate(blocks):
    if (dir == 0):
        openset.append((chars, 1, getChildren(head, chars), {i}))
        openset.append((chars, 2, getChildren(head, chars), {i}))
    elif (dir == 1):
        openset.append((chars, 1, getChildren(head, chars), {i}))
        for c in chars:
            openset.append((c, 2, getChildren(head, c), {i}))
    else:
        openset.append((chars, 2, getChildren(head, chars), {i}))
        for c in chars:
            openset.append((c, 1, getChildren(head, c), {i}))
openset.sort()

#%% DFS
output = []
while openset:
    curr, dir, node, used = openset.pop()
    if (dir == 1 and len(curr) > 8):
        continue
    if (dir == 2 and len(curr) > 9):
        continue
    if (curr in dict):
        output.append(curr)
    if (node is None or not node.hasChildren()):
        continue
    for i,block in enumerate(blocks):
        if (i in used):
            continue
        chars,block_dir = block
        new_used = used | {i}
        if (block_dir == 0 or block_dir == dir):
            new_curr = curr + chars
            new_node = getChildren(node, chars)
            openset.append((new_curr, dir, new_node, new_used))
        else:
            for c in chars:
                new_curr = curr + c
                new_node = getChildren(node, c)
                openset.append((new_curr, dir, new_node, new_used))

#%% Outputting
output.sort(key=lambda x: len(x))
print("\n".join(output))


'''
blocks = [("A", 0), ("AB", 1), "(BC", 2), ...]
    blocks[0] = letters in block
    blocks[1] = key (0 is single, 1 is horiz, 2 is vert)
openset = [(curr, dir, treeNode, [used])]
    used stores indicies from blocks
    
1. build dict tree
2. DFS
    if curr is a word --> add to output
    if treeNode has no kids: continue
    for i,(letters,dir) in blocks:
        new_used = used + [i]
        if dir == 0
            new_curr = curr + letters
            new_node = node.children[letters]
        elif dir == 1
            new_curr = curr + letters
            new_node = node.children[letters[0]].children[letters[1]]
        elif dir == 2
            new_curr_1 = curr + letters[0]
            new_node
            new_curr_2 = curr + letters[1]
            new_node


Look for vertical words first:
    max len: 9
    min len: 3
    Try to make any word with:
        1. single letters
        2. vertical letters (together)
        3. ONLY left or ONLY right letter from horiz block
Look for all horizontal words:
    max len: 8
    min len: 3
    Try to make any word with:
        1. single letters
        2. horizontal letters (together)
        3. ONLY top or ONLY bottom letter from vert block
'''