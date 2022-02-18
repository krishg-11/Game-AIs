from wordle_functions import *
import time
import json
     
valid_guesses, answers, ans_by_letter = read_files("valid_guesses.txt", "valid_answers.txt")

for guess in valid_guesses:
    start = time.time()
    guess_results = sum(len(filter_answers(answers, ans_by_letter, *guess_result(guess, ans))) for ans in answers)
    valid_guesses[guess] = guess_results / len(answers)
    print(guess, valid_guesses[guess], time.time() - start)
    
# print(valid_guesses)
print(min(valid_guesses.keys(), key = lambda x:valid_guesses[x]))
json.dump(valid_guesses, open("first_guess.json", "w"))
    
'''
Best First Words:
word    average answers left
-----------------------------
roate   86.175
raise   87.299
raile   87.892
soare   88.509
irate   88.706
orate   88.822
artel   89.347
ariel   89.387
arise   89.619
taler   91.011
'''
        
        