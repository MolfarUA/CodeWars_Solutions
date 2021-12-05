def calculate_age(year_of_birth, current_year):
    diff = abs(current_year - year_of_birth)
    plural = '' if diff == 1 else 's'
    if year_of_birth < current_year:
        return 'You are {} year{} old.'.format(diff, plural)
    elif year_of_birth > current_year:
        return 'You will be born in {} year{}.'.format(diff, plural)
    return 'You were born this very year!'
###########
def calculate_age(old, new):
    if old == new: return "You were born this very year!"
    elif old < new: return "You are 1 year old." if new-old == 1 else 'You are %.f years old.' %(new-old)
    else: return "You will be born in 1 year." if old-new == 1 else 'You will be born in %.f years.' %(old - new)
##############
def calculate_age(year_of_birth, current_year):
    year = (year_of_birth - current_year)
    c1 = f"You are {abs(year)} {['year','years'][abs(year)!=1]} old."
    c2 = f"You will be born in {year} {['year','years'][year!=1]}."
    return 'You were born this very year!' if not year else [c1,c2][year >0 ]
############
def calculate_age(birth, year):
    if birth == year:
        return 'You were born this very year!'
    return [f'You will be born in {birth-year} year{"s"*(birth-year != 1)}.', f'You are {year-birth} year{"s"*(year-birth != 1)} old.'][birth < year]
#############
def calculate_age(year_of_birth, current_year):
    if current_year - year_of_birth == 0:
        return "You were born this very year!"
    elif current_year - year_of_birth == 1:
        return "You are 1 year old."
    elif current_year - year_of_birth == -1:
        return "You will be born in 1 year."
    elif current_year - year_of_birth > 1:
        return f"You are {current_year - year_of_birth} years old."
    elif current_year - year_of_birth < -1:
        return f"You will be born in {abs(current_year - year_of_birth)} years."
#######
def calculate_age(year_of_birth, current_year):
    diff = current_year - year_of_birth
    if diff < 0:
        return f"You will be born in {abs(diff)} {'year' if diff == -1 else 'years'}."
    if diff > 0:
        return f"You are {diff} {'year' if diff == 1 else 'years'} old."
    return "You were born this very year!"
##########
def calculate_age(y1, y2):
    if y1 == y2:
        return "You were born this very year!"
    elif y1 - y2 == 1:
        return "You will be born in 1 year."
    elif y2- y1 == 1:
        return "You are 1 year old."
    elif y1 < y2:
        return "You are " + str(y2 - y1) + " years old."
    else:
        return "You will be born in " + str(y1 - y2) + " years."
#############
def calculate_age(b, curr):
    end = " year" if abs(b-curr) == 1 else " years"
    if b > curr:
        return "You will be born in " + str(b - curr) + end + "."
    elif b < curr:
        return "You are " + str(curr-b) + end + " old."
    else:
        return "You were born this very year!"
