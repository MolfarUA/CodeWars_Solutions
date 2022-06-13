def monty_hall(door, guesses):
    return round(100.0 * (len(guesses)-guesses.count(door))/len(guesses))
_________________________________________________
def monty_hall(c, p):
    print(c, p)
    return round((1 - (p.count(c) / len(p))) * 100)
_________________________________________________
def monty_hall(correct, guesses):
    return round(sum([correct != x for x in guesses]) / len(guesses) * 100)
_________________________________________________
def monty_hall(correct_door_number, participant_guesses):
    return round(100 * sum(1 for x in participant_guesses if x != correct_door_number) / len(participant_guesses))
_________________________________________________
def monty_hall(correct_door_number, participant_guesses):
    return 100 - int(round(sum(guess == correct_door_number for guess in participant_guesses) / len(participant_guesses) * 100, 0))
_________________________________________________
def monty_hall(correct_door_number, participant_guesses):
    count = 0
    for i in participant_guesses:
        if i == correct_door_number:
            count +=1
    return round((1 - count/len(participant_guesses))*100)
_________________________________________________
def monty_hall(correct_door_number, participant_guesses):
    len1=len(participant_guesses)
    count=0
    for i in participant_guesses:
        if i ==correct_door_number:
            count+=1
    count=len1-count
    print (count, correct_door_number, participant_guesses)
    return round(count*100/len1)
