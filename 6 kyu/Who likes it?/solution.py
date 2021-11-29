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
