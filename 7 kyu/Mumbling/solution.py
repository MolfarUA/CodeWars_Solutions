def accum(s):
    result = ''
    for i in range(len(s)):
        result += s[i].upper() + s[i].lower() * i + ('-')
    return result[:-1]
