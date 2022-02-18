from wordle_functions import *
            
valid_guesses, answers, ans_by_letter = read_files("valid_guesses.txt", "valid_answers.txt")

while True:
    guess = input("What is your guess: ").lower()
    assert len(guess) == 5
    result = input("What was your result (= for green, + for yellow, - for grey): ")
    answers = filter_answers(answers, ans_by_letter, *read_result(result, guess))
    print(f"There are {len(answers)} possible answers left")
    print("Your best guesses are: ", play_turn(answers, valid_guesses, ans_by_letter)[:5])
    