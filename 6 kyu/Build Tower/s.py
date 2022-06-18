576757b1df89ecf5bd00073b


def tower_builder(n):
    return [("*" * (i*2-1)).center(n*2-1) for i in range(1, n+1)]
_____________________________
def tower_builder(n_floors):
    if n_floors == 0:
        return []
        
    count = 1
    result = []

    for i in range(1, n_floors + 1):
        stars = '*' * (2 * i - 1)
        space = ' ' * (n_floors - i)
        result.append(space + stars + space)
    
    return result
_____________________________
def tower_builder(n):
    return [" " * (n - i - 1) + "*" * (2*i + 1) + " " * (n - i - 1) for i in range(n)]
_____________________________
def tower_builder(n_floors):
    tower = []
    spacing = n_floors - 1
    stars = 1
    for i in range(0, n_floors):
        tower.append(' ' * spacing + '*' * stars + spacing * ' ')
        stars += 2
        spacing -= 1
    return tower
_____________________________
def tower_builder(n):
    length = n * 2 - 1
    return ['{:^{}}'.format('*' * a, length) for a in xrange(1, length + 1, 2)]
_____________________________
def tower_builder(n_floors):
    width = 2*n_floors-1
    return [("*"*(2*level+1)).center(width) for level in range(n_floors)]
_____________________________
def tower_builder(n):
    if n == 1:
        return ['*']
    arr = []
    start = ''
    second = ''
    finish = ''
    for i in range(2*n-1):
        if i != n-1:
            start += ' '
        else:
            start += '*'
        if i >= n-2 and i <= n:
            second += '*'
        else:
            second += ' '
        finish += '*'
    arr.append(start)
    if n > 2:
        arr.append(second)
        for i in range(1, n-2):
            line = ' '
            for j in range(1, len(arr[i])-1):
                if arr[i][j+1] == '*':
                    line += '*'
                else:
                    line += ' '
                if len(line) >= len(arr[i])//2:
                    line = line + '*' + line[::-1]
                    break
            arr.append(line)
    arr.append(finish)
    return arr
_____________________________
def tower_builder(n_floors):
    str_len = n_floors * 2 - 1
    text = ''
    num_item = 1
    result = []
    for i in range(n_floors):
        num_space = int((str_len - num_item) / 2)
        text = ' ' * num_space + '*' * num_item + ' ' * num_space
        result.append(text)
        num_item += 2
    return result
_____________________________
def tower_builder(n_floors):
    tower = []

    for x in range(1, n_floors+1):
        tower.append("{space1}{stars}{space2}".format(space1= ' '*((n_floors - x)), stars= '*' * ((2*x) - 1), space2=  ' '*(n_floors - x)))
    
    return tower
_____________________________
def tower_builder(n):
    res = []
    for x in range(1, n*2+1, 2):
        i = int((n*2-x-1)/2)*' '
        res.append(i + x*'*' + i)
    return res
_____________________________
def tower_builder(n_floors):
    tower = []
    block = '*' * (n_floors * 2 - 1)
    for i in range(1, n_floors+1):
        tower.append(block)
        spaces = ' ' * i
        block = spaces + '*' * (n_floors * 2 - (i * 2)-1) + spaces
    return tower[::-1]
_____________________________
def tower_builder(n):
    i,j=n-1,1
    t=[]
    while i>-1:
        t.append(" "*i+"*"*j+" "*i)
        i-=1
        j+=2
    return(t)
_____________________________
def tower_builder(n_floors):
    string = []
    count = 1
    for i in range(1, n_floors+1):
        n_floors -= 1
        string.append(' ' * n_floors + '*' * count + ' ' * n_floors)
        count += 2
    return string
_____________________________
def tower_builder(n_floors):
    sup_list = []
    sup_list2 = []
    for n in range(1, n_floors * 2, 2):
        ann = '*' * n
        sup_list.append(ann)
    maximum = len(sup_list[-1])

    for x in sup_list:
        simbol = int((maximum - len(x)) / 2)
        base = " " * simbol
        sup_list2.append(base + x + base)

    return sup_list2
