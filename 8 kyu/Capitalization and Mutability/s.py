595970246c9b8fa0a8000086


def capitalizeWord(word):
    return word.capitalize()
______________________
def capitalizeWord(s):
    return s.title()
______________________
capitalizeWord = str.capitalize
______________________
def capitalizeWord(word):
    return word[0].upper() + word[1:]
______________________
def capitalizeWord(word):
    return word.title()
______________________
def capitalize_word(word):
    return word.capitalize()
______________________
def capitalizeWord(word):
    return word[:1].upper() + word[1:]
______________________
def capitalizeWord(word):

    c=  word[0].upper()+word[1:]

    return c
______________________
def capitalize_word(word):
    word = word.lower()
    return word.title()
______________________
def capitalize_word(word):
    if len(word) == 1:
        return str(word[0].upper())
    elif len(word) > 1:
        Answer = f"{str(word[0].upper())}"
        for item in word[1:]:
            Answer += str(item)
        return Answer
______________________
def capitalize_word(word):
    wordConverted = list(word)
    
    wordConverted[:1] = [x.upper() for x in wordConverted[:1]]
    
    return ''.join(wordConverted)
______________________
def capitalize_word(word):
    wordl = list(word)
    wordl[0] = wordl[0].upper()
    output = ""
    for element in wordl:
        output = output + str(element)
    return output
