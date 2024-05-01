
# the result (green, yellow, grey) for a given guess with given answer
def guess_result(guess, ans):
    # Keep track of which letters have already been seen
    # This ensures letters are not double counted with yellow/greens
    ans_letters = {} 
    for c in ans:
        if c not in ans_letters: ans_letters[c] = 0
        ans_letters[c] += 1
    yellow = []
    green = []
    grey = set()
    for i,c in enumerate(guess):
        # If in correct position, mark as green
        if (ans[i] == c):
            green.append((c, i))
            if (ans_letters[c] == 0):
                for i in range(len(yellow)):
                    if (yellow[i][0] == c):
                        yellow.pop(i)
                        break
            else:
                ans_letters[c] -= 1
        
        # If in the word, mark as yellow
        elif (c in ans_letters):
            if(ans_letters[c] == 0): continue
            yellow.append((c, i))
            ans_letters[c] -= 1
            
        # If not in the word, mark as gray
        else:
            grey.add(c)
    return (green, yellow, grey)

# filters poss_answers down given the result of last guess
# inefficient?
def filter_answers(poss_answers, ans_by_letter, green, yellow, grey):
    # Remove all words with gray letters
    new_answers = poss_answers.difference(*[ans_by_letter[c] for c in grey])
    
    # Only include words with all yellow letters
    new_answers = new_answers.intersection(*[ans_by_letter[c] for c,i in yellow])
    
    # Find words to remove based on letter position
    to_remove = set()
    for ans in new_answers:
        # Remove words without greens in correct position
        for c,i in green:
            if (ans[i] != c):
                to_remove.add(ans)
                break
        # Remove words with yellows in wrong position
        for c,i in yellow:
            if (ans[i] == c):
                to_remove.add(ans)
                break
                
    return new_answers - to_remove

# Read in result from user e.g. -+-=+
#   - is gray
#   + is yellow
#   = is green
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

# Choose best possible move given previous info
def play_turn(poss_answers, valid_guesses, ans_by_letter):
    for guess in valid_guesses:
        # Find average number of answers filtered across all possible answers
        valid_guesses[guess] = sum(len(filter_answers(poss_answers, ans_by_letter, *guess_result(guess, ans))) for ans in poss_answers) / len(poss_answers)
        
        # Prioritize guesses that are valid answers
        if guess in poss_answers: valid_guesses[guess] /= 1.1
    
    # Sort by best guesses
    s_guesses = sorted((item[1], item[0]) for item in valid_guesses.items())
    return s_guesses

# Read in files
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