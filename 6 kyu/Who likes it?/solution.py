def likes(names):
    n = len(names)
    if n == 0:
        return "no one likes this"
    if n == 1:
        return names[0] + ' likes this'
    if n == 2:
        return names[0] + ' and ' + names[1] + ' like this'
    if n == 3:
        return names[0] + ', ' + names[1] + ' and ' + names[2] + ' like this'
    if n >= 4:
        return names[0] + ', ' + names[1] + ' and ' + str(n - 2) + \
            ' others like this'
##################
def likes(names):
    n = len(names)
    return {
        0: 'no one likes this',
        1: '{} likes this', 
        2: '{} and {} like this', 
        3: '{}, {} and {} like this', 
        4: '{}, {} and {others} others like this'
    }[min(4, n)].format(*names[:3], others=n-2)
##################
def likes(names):
    # make a dictionary d of all the possible answers. Keys are the respective number
    # of people who liked it.
    
    # {} indicate placeholders. They do not need any numbers but are simply replaced/formatted
    # in the order the arguments in names are given to format
    # {others} can be replaced by its name; below the argument "others = length - 2"
    # is passed to str.format()
    d = {
        0: "no one likes this",
        1: "{} likes this",
        2: "{} and {} like this",
        3: "{}, {} and {} like this",
        4: "{}, {} and {others} others like this"
        }
    length = len(names)
    # d[min(4, length)] insures that the appropriate string is called from the dictionary
    # and subsequently returned. Min is necessary as len(names) may be > 4
    
    # The * in *names ensures that the list names is blown up and that format is called
    # as if each item in names was passed to format individually, i. e.
    # format(names[0], names[1], .... , names[n], others = length - 2
    return d[min(4, length)].format(*names, others = length - 2)
################
def likes(names):
    formats = {
            0: "no one likes this",
            1: "{} likes this",
            2: "{} and {} like this",
            3: "{}, {} and {} like this",
            4: "{}, {} and {others} others like this"
        }
    n = len(names)
    return formats[min(n,4)].format(*names, others=n-2)
##############
def likes(names):
    if len(names) == 0:
        return "no one likes this"
    elif len(names) == 1:
        return "%s likes this" % names[0]
    elif len(names) == 2:
        return "%s and %s like this" % (names[0], names[1])
    elif len(names) == 3:
        return "%s, %s and %s like this" % (names[0], names[1], names[2])
    else:
        return "%s, %s and %s others like this" % (names[0], names[1], len(names)-2)
################
def likes(names):
    namez=names[:]
    msg=['no one likes this','{0} likes this','{0} and {1} like this','{0}, {1} and {2} like this','{0}, {1} and {remains} others like this']
    return msg[min(4,len(namez))].format(*namez,remains=len(namez)-2)
###################
def likes(names):
    if len(names) == 0:
        return 'no one likes this'
    elif len(names) == 1:
        return str(names[0]+' likes this')
    elif len(names) == 2:
        return str(names[0]+' and '+names[1]+' like this')
    elif len(names) == 3:
        return str(names[0]+', '+names[1]+' and '+names[2]+' like this')
    else:
        return str(names[0]+', '+names[1]+' and '+str(len(names)-2)+' others like this')
############
def likes(names):
    """Convert list of names into strings of likes

    Args:
        names (list): List of string names

    Returns:
        str

    Examples:
        >>> likes(['Pavel', 'Yury', 'Sveta'])
        'Pavel, Yury and Sveta like this'
    """
    if not names:
        return 'no one likes this'
    if len(names) == 1:
        first = ''
        second = names[0]
    elif len(names) == 2:
        first = names[0]
        second = names[1]
    elif len(names) == 3:
        first = ', '.join(names[:2])
        second = names[-1]
    else:
        first = ', '.join(names[:2])
        second = '%d others' % (len(names) - 2)
    if first:
        return first + ' and ' + second + ' like this'
    else:
        return second + ' likes this'
###############
def likes(names):
    if not names:
        return "no one likes this"
    size = len(names)
    if size == 1:
        return "%s likes this" % names[0]
    if size == 2:
        return "%s and %s like this" % (names[0], names[1])
    if size == 3:
        return "%s, %s and %s like this" % (names[0], names[1], names[2])
    if size >= 4:
        return "%s, %s and %s others like this" % (names[0], names[1], len(names[2:]))
################
def likes(names):
    total = len(names)
    return ( 'no one likes this' if total == 0 else
             '%s likes this' % names[0] if total == 1 else
             '%s and %s like this' % (names[0], names[1]) if total == 2 else
             '%s, %s and %s like this' % (names[0], names[1], names[2]) if total == 3 else
             '%s, %s and %s others like this' % (names[0], names[1], total-2) )
##############
def likes(names):
    if not names: names = ['no one']
    if len(names) > 3: names[2:] = ['%d others' % (len(names) - 2)]
    people = ('{}' + ', {}' * (len(names) == 3) + ' and {}' * (len(names) > 1)).format(*names)
    return people + ' like%s this' % ('s' * (len(names) < 2))
##############
LIKES_0 = 'no one likes this'
LIKES_1 = '%s likes this'
LIKES_2 = '%s and %s like this'
LIKES_3 = '%s, %s and %s like this'
LIKES_4 = '%s, %s and %s others like this'
LIKES = {
    0: LIKES_0, 
    1: LIKES_1, 
    2: LIKES_2, 
    3: LIKES_3, 
    }

def likes(names):
    if len(names) >= 4:
        return LIKES_4 % (names[0], names[1], len(names)-2)
    return LIKES[len(names)] % tuple(names)
##############
def likes(names):
    #your code here
    if bool(names):
        if len(names) == 1:
            return '{} likes this'.format(names[0])
        elif len(names) == 2:
            return '{} and {} like this'.format(names[0], names[1])
        else:
            val = '{} others'.format(len(names[2:]))
            if names[2] == names[-1]:val = names[2]
            return '{} and {} like this'.format(', '.join(names[:2]), val)
    return 'no one likes this'
