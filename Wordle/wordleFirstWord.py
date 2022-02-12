'''
Go thru list of possible answers
    - keep counter for each letter
        - occurences in each position and total occurences (sum of all positions)

Go thru list of possible guesses
    - give each word a score
        - for each letter in the w
            - + total occurences of that letter (hyperparemter)
            - + 5*occurences of that letter in that position (hyperparemter) 
            
print out ranked list

TODO:
    account for duplicate letters
-------------------------------------------------------------------------------------------
go thru each guess
    for each possible answer, see the outcome of the guess (yellow, green, etc.)
        see how many remaining words this outcome leaves u with
    average the num of remaining words
'''
import time
import json

# the result (green, yellow, grey) for a given guess with given answer
# @return regex pattern for greens, 
def guess_result(guess, ans):
    ans_letters = set(ans)
    yellow = set()
    green = []
    grey = set()
    for i,c in enumerate(guess):
        if (ans[i] == c):
            green.append((c, i))
        elif (c in ans_letters):
            yellow.add(c)
        else:
            grey.add(c)
    return (green, yellow, grey)

# filters poss_answers down given the result of last guess
def filter_answers(poss_answers, green, yellow, grey):
    new_answers = poss_answers.difference(*[ans_by_letter[c] for c in grey])
    new_answers = new_answers.intersection(*[ans_by_letter[c] for c in yellow])

    to_remove = set()
    for ans in new_answers:
        for c,i in green:
            if (ans[i] != c):
                to_remove.add(ans)
                break
    new_answers =  new_answers - to_remove
    return new_answers
        

valid_guesses = {word.strip():0 for word in open("valid_guesses.txt")}
answers = {word.strip() for word in open("valid_answers.txt")}

ans_by_letter = {}
for ans in answers:
    for c in ans:
        if c not in ans_by_letter:
            ans_by_letter[c] = set()
        ans_by_letter[c].add(ans)

for guess in valid_guesses:
    start = time.time()
    guess_results = sum(len(filter_answers(answers, *guess_result(guess, ans))) for ans in answers)
    valid_guesses[guess] = guess_results / len(answers)
    print(guess, valid_guesses[guess], time.time() - start)
    
# print(valid_guesses)
print(min(valid_guesses.keys(), key = lambda x:valid_guesses[x]))
json.dump(valid_guesses, open("first_guess.json", "w"))
    
        
        