def longest(s1, s2):
    uniques = []
    for char in s1:
        if char not in uniques:
            uniques.append(char)
    for char in s2:
        if char not in uniques:
            uniques.append(char)
    return ''.join(sorted(uniques))
