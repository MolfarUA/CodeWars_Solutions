56f6ad906b88de513f000d96


def bonus_time(salary, bonus):
    return "${}".format(salary * (10 if bonus else 1))
_________________________
def bonus_time(salary, bonus):
    return f"${salary * 10 if bonus else salary}"
_________________________
def bonus_time(salary, bonus):
    return '$' + str(salary * [1,10][bonus])
_________________________
def bonus_time(salary, bonus):
    return "$" + str(salary * 10) if bonus == True else "$" + str(salary)
_________________________
bonus_time = lambda salary, bonus: '${}'.format(salary * 10 if bonus else salary)
_________________________
def bonus_time(salary, bonus):
    if bonus: salary = salary * 10
    return str.format('${0}', salary)
_________________________
def bonus_time(sum, bonus):
    x = "$"
    if bonus == True:
        sum = sum * 10
        return x + str(sum)
    elif bonus != True:
        return x + str(sum)
_________________________
def bonus_time(salary, bonus):
    y = "$"
    if bonus == True:
        salary = salary * 10
        return y + str(salary)
    else:
        return y + str(salary)
_________________________
def bonus_time(salary, bonus):
    print(salary, bonus)
    if bonus == True:
        return "$" + str(salary * 10)
    else:
        return "$" + str(salary)
