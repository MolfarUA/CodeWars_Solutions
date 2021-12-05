def what_is(x):
    if x is 42:
        return 'everything'
    elif x == 42 * 42:
        return 'everything squared'
    else:
        return 'nothing'
#############3
dict = {
    42 : "everything",
    42 * 42 : "everything squared"
}

def what_is(x):
    return dict.get(x, "nothing")
###############
what_is = lambda x: 'everything' if x == 42 else \
          'everything squared' if x == 42**2 else 'nothing'
#############
def what_is(x):
    answer = 'nothing';
    if x == 42:
        answer = 'everything';
        return answer;
    elif x == 1764:
        answer = 'everything squared';
        return answer;
    else:
        return answer;
    
