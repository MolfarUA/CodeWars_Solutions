def accum(s):
    result = ''
    for i in range(len(s)):
        result += s[i].upper() + s[i].lower() * i + ('-')
    return result[:-1]
#########################################
def accum(s):
    return '-'.join(c.upper() + c.lower() * i for i, c in enumerate(s))
#########################################
def accum(s):
    output = ""
    for i in range(len(s)):
        output+=(s[i]*(i+1))+"-"
    return output.title()[:-1]
###########################################
def accum(s):
    i = 0
    result = ''
    for letter in s:
        result += letter.upper() + letter.lower() * i + '-'
        i += 1
    return result[:len(result)-1]
##########################################
def accum(s):
    return "-".join([((j*(i+1)).capitalize()) for i,j in enumerate(s)])
######################################
def accum(s):
    str = ""
    for i in range(0, len(s)):
        str += s[i].upper()
        str += s[i].lower()*i
        if i != len(s)-1:
            str += "-"
    return str
