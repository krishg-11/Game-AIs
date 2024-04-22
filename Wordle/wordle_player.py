from wordle_functions import *
            
valid_guesses, answers, ans_by_letter = read_files("valid_guesses.txt", "valid_answers.txt")

while True:
    guess = input("What is your guess: ").lower()
    assert len(guess) == 5
    result = input("What was your result (= for green, + for yellow, - for grey): ")
    answers = filter_answers(answers, ans_by_letter, *read_result(result, guess))
    print(f"There are {len(answers)} possible answers left")
    
    print()
    if(len(answers) == 1):
        print(f"The wordle word of the day is: {answers}")
    else:
        print("The best guesses are:")
        top_guess =  play_turn(answers, valid_guesses, ans_by_letter)[:5]
        print("Word\t\t Avg # of guesses left")
        print("-"*40)
        for avg, word in top_guess:
            print(f"{word}\t\t|\t {avg:.3f}")
            
    print("\n"*2)
    # print("Your best guesses are: ",)
    # print()
    