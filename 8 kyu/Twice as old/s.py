5b853229cfde412a470000d0


def twice_as_old(dad_years_old, son_years_old):
    return abs(dad_years_old - 2*son_years_old)
________________________________
def twice_as_old(d, s):
    return abs(d-2*s)
________________________________
def twice_as_old(dad_years_old, son_years_old):
    count = 0
    if son_years_old == 0:
        return dad_years_old
    elif dad_years_old / son_years_old > 2:
        while son_years_old * 2 != dad_years_old:
            dad_years_old += 1
            son_years_old += 1
            count += 1
        return count
    elif dad_years_old / son_years_old < 2:
        while son_years_old != 0 and son_years_old * 2 != dad_years_old:
            dad_years_old -= 1
            son_years_old -= 1
            count += 1
        return count
    else:
        return 0
________________________________
def twice_as_old(dad_years_old, son_years_old):
    return abs(2*son_years_old - dad_years_old)
________________________________
def twice_as_old(a, b):
    return abs(b * 2 - a)
________________________________
def twice_as_old(dad, son):
    if son*2==dad:
        return 0
    x=0
    while son*2!=dad:
        if son*2>dad:
            dad-=1
            son-=1
            x+=1
        else:
            dad+=1
            son+=1
            x+=1
    return x
________________________________
def twice_as_old(dad, son):
    for i in range(1,100):
        if dad + i == (son + i) * 2 or dad - i == (son - i) * 2:
            return i
    return 0
________________________________
def twice_as_old(dad_years_old, son_years_old):
    if dad_years_old != son_years_old:
        x = (dad_years_old - (son_years_old * 2))
        if x < 0:
            x = x * -1
        return x
________________________________
def twice_as_old(dad_years_old, son_years_old):
    return dad_years_old - (son_years_old * 2) if son_years_old < dad_years_old / 2 else -dad_years_old + (son_years_old * 2)
