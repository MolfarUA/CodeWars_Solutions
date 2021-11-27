def abbrev_name(name):
    initials = ''
    arr = name.split()
    for n in arr:
        initials += n[0].upper() + '.'
        
    print(initials[0:-1])
    return initials[0:-1]
