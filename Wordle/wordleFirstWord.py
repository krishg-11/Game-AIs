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
roate	60.425
raise	61.001
raile	61.331
soare	62.301
arise	63.726
irate	63.779
orate	63.891
ariel	65.288
arose	66.021
raine	67.056'
'''
        
        