import string

def high(x):
    scores = []
    letters = [i for i in string. ascii_lowercase]
    words = x.split(' ')
    current = 0
    for word in words:
        for letter in word:
            current += (letters.index(letter) + 1)
        scores.append(current)
        current = 0

    highest = scores.index(max(scores))

    return words[highest]
###############
