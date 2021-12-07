def ensure_question(s):
    return s + '?' if '?' not in s else s
###########
def ensure_question(s):
    return s.rstrip('?') + '?'
########
def ensure_question(s):
    if not s.endswith("?"):
        return s + "?"
    return s
##########
def ensure_question(s):
    return s if s.endswith('?') else s + '?'
########
def ensure_question(s):
    if s=="":
        return '?'
    if(s[-1]=='?'):
        return s
    else:
        return s+'?'
###########
def ensure_question(s):
    return f'{s}?'.replace('??', '?')
##########
ensure_question=lambda s:s+"?"*(not'?'in s)
#######
def ensure_question(s):
    return s+'?' if '?' not in s else s.replace('?','',s.count('?')-1)
###########
def ensure_question(s):
    return '?' if s == '' else (s + '?', s)[s[-1] == '?']
############
def ensure_question(s):
    return "?" if not len(s) else (s + '?' if s[-1] != '?' else s)
#############
def ensure_question(s):
    return f'{s}?' if s[-1:] != '?' else s
#############
def ensure_question(s):
    result = s
    if "?" not in result:
        result += "?"
    return result
