#%% Read in dictionary
filename = "../scrabble.txt"
dict = {line.lower().strip() for line in open(filename)} # can use set where key = first letter of word
dict = {x for x in dict if len(x) > 2}

#%% Input letters and data validation
letters = input("What are your letters: ").lower().strip()
assert len(letters) == 6

all_words = set()
#%% BFS
openset = [("", letters)]
while(openset):
    curr,left = openset.pop(0)
    if (curr in dict):
        all_words.add(curr)
    for i,c in enumerate(left):
        new_word = curr + c
        new_left = left[:i] + left[i+1:]
        openset.append((new_word, new_left))

#%% Output
output = list(all_words)
output.sort(key=lambda x: len(x))
print("\n".join(output))
        

