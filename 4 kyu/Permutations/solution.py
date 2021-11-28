def permutations(string):
    if len (string) == 1:
        return string
    answer = []
    for x in string:
        answer = answer + list(map(lambda p: x + p, permutations(string.replace(x,'',1))))
    return set(answer)
