
# the result (green, yellow, grey) for a given guess with given answer
def guess_result(guess, ans):
    ans_letters = {}
    for c in ans:
        if c not in ans_letters: ans_letters[c] = 0
        ans_letters[c] += 1
    yellow = []
    green = []
    grey = set()
    for i,c in enumerate(guess):
        if (ans[i] == c):
            green.append((c, i))
            if (ans_letters[c] == 0):
                for i in range(len(yellow)):
                    if (yellow[i][0] == c):
                        yellow.pop(i)
                        break
            else:
                ans_letters[c] -= 1
        elif (c in ans_letters):
            if(ans_letters[c] == 0): continue
            yellow.append((c, i))
            ans_letters[c] -= 1
        else:
            grey.add(c)
    return (green, yellow, grey)

# filters poss_answers down given the result of last guess
# inefficient?
def filter_answers(poss_answers, ans_by_letter, green, yellow, grey):
    new_answers = poss_answers.difference(*[ans_by_letter[c] for c in grey])
    new_answers = new_answers.intersection(*[ans_by_letter[c] for c,i in yellow])
    
    to_remove = set()
    for ans in new_answers:
        for c,i in green:
            if (ans[i] != c):
                to_remove.add(ans)
                break
        for c,i in yellow:
            if (ans[i] == c):
                to_remove.add(ans)
                break
                
    return new_answers - to_remove

def read_result(result, guess):
    yellow = []
    green = []
    grey = set()
    for i,x in enumerate(result):
        if (x == "-"):
            grey.add(guess[i])
        elif (x == "+"):
            yellow.append((guess[i], i))
        else:
            green.append((guess[i], i))
    
    return green, yellow, grey

def play_turn(poss_answers, valid_guesses, ans_by_letter):
    for guess in valid_guesses:
        valid_guesses[guess] = sum(len(filter_answers(poss_answers, ans_by_letter, *guess_result(guess, ans))) for ans in poss_answers) / len(poss_answers)
        if guess in poss_answers: valid_guesses[guess] /= 1.1
    s_guesses = sorted((item[1], item[0]) for item in valid_guesses.items())
    return s_guesses

def read_files(guess_file, answers_file):
    valid_guesses = {word.strip():0 for word in open(guess_file)}
    answers = {word.strip() for word in open(answers_file)}

    ans_by_letter = {}
    for ans in answers:
        for c in ans:
            if c not in ans_by_letter:
                ans_by_letter[c] = set()
            ans_by_letter[c].add(ans)
    return valid_guesses, answers, ans_by_letter