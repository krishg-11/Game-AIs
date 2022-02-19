from wordle_functions import *
import json
import time

valid_guesses, answers, ans_by_letter = read_files("valid_guesses.txt", "valid_answers.txt")

move_counts = {}
guess_counts = {guess:{i:0 for i in range(5)} for guess in valid_guesses}

first_word = "roate"

for ans in answers:
    start = time.time()
    guess = first_word
    result = guess_result(guess, ans)
    guess_counts[guess][0] += 1
    # print(f"Guessed {guess} with result {result}")
    poss_answers = filter_answers(answers, ans_by_letter, *result)
    move_count = 1
    while len(result[0]) != 5:
        guess = play_turn(poss_answers, valid_guesses, ans_by_letter)[0][1]
        result = guess_result(guess, ans)
        guess_counts[guess][move_count] += 1
        # print(f"Guessed {guess} with result {result}")
        poss_answers = filter_answers(poss_answers, ans_by_letter, *result)
        move_count += 1
    print(f"Solved {ans} in {move_count} moves and {time.time()-start:.3f} seconds")
    move_counts[ans] = move_count

avg_moves = sum(move_counts[ans] for ans in move_counts) / len(move_counts)
print("Average moves taken:", avg_moves)
json.dump(guess_counts, open("guess_counts.json", "w"))

'''
Average moves taken: 3.495
Average time taken: 36.4 seconds
Most common guesses:
    roate guessed 2315 times 
    slimy guessed 195 times
    siled guessed 158 times 
    lysin guessed 112 times
    silen guessed 106 times 
    slick guessed 104 times 
    sling guessed 84 times 
    shunt guessed 84 times 
    bludy guessed 71 times 
    scion guessed 66 times 
Most common second guess:
    bench was 2nd guess 22 times 
    abamp was 2nd guess 19 times 
    abaft was 2nd guess 15 times 
    panda was 2nd guess 13 times 
    cadgy was 2nd guess 13 times 
    phang was 2nd guess 12 times 
    hawms was 2nd guess 12 times 
    kemps was 2nd guess 11 times 
    gimpy was 2nd guess 11 times 
    cupid was 2nd guess 11 times 
'''
        