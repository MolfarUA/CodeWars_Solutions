def number(lines):
    res = []
    if len(lines)==0:
        return []
    for i,item in enumerate(lines):
        res.append("{}: {}".format(i+1,item))
    return res
###########
def number(lines):
  return ['%d: %s' % v for v in enumerate(lines, 1)]
############
def number(lines):
    return ["{0}: {1}".format(i + 1, lines[i]) for i in xrange(len(lines))]
###########
def number(lines):
    return ['{}: {}'.format(n, s) for (n, s) in enumerate(lines, 1)]
###########
def number(lines):
    count = 1
    for x in range(len(lines)):
        lines[x] = str(count)+ ": " + lines[x]
        count += 1
    return lines
###########
def number(lines):
    res = []
    for i, el in enumerate(lines):
        line = f"{i+1}: {el}"
        res.append(line)
    return res
###########
def number(lines):
    n_list=[]
    for i in range(len(lines)):
        buf=str(i+1)+": "+str(lines[i])
        n_list.append(buf)
    return n_list
###########
def number(lines):
    if not lines:
        return lines
    return [f'{i}: {line}' for i, line in enumerate(lines, 1)]
###########
def number(lines):
    count=0
    lst=[]
    for x in lines:
        count+=1
        new_string=str(count) + ': ' +  x
        lst.append (new_string)
    return lst
############
def number(lines):
    return [f"{line+1}: " + lines[line] for line in range(len(lines))]
############
def number(lines):
    new_lines = []
    for i in range(1, len(lines)+1):
        new_lines.append(f"{i}: {lines[i-1]}")
    return new_lines
#############
def number(lines):
    new_string =[]
    number = 1
    for string in lines:
        new_string.append(str(number) + ": " + string)
        number += 1
    return new_string
#############
def number(lines):
    n = 1
    line = []
    for x in lines:
        line.append(str(n) + ': ' + x)
        n += 1
    return line
#############
def number(lines):
    #------------- specfiying format
    #        \   \
    return ['{}: {}'.format(n, s) for (n, s) in enumerate(lines, 1)]
    #                       \   \                \         \     \
    #--------------------------------------------------------------
    #                       vars assigned       enumerate items in list
    #                       to format           but start at 1 rather than 0
###########
def number(lines):
    line_num = []
    for i,c in enumerate(lines):
        line_num.append((f'{i+1}: {c}'))
    return line_num
