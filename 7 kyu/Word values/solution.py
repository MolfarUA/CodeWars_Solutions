def name_value(my_list):
    for i in range(len(my_list)):
        sum_chars = 0
        for j in my_list[i]:
            if j.isalpha():
                sum_chars += ord(j) - 96
        my_list[i] = sum_chars * (i + 1)
    return my_list
##########
def nameValue(myList):
    return [ i*sum(map(lambda c: [0, ord(c)-96][c.isalpha()], w.lower())) for i,w in enumerate(myList,1)]
#########
def nameValue(myList):
    from string import ascii_lowercase as alphabet
    value_map = dict(((letter, i) for i, letter in enumerate(alphabet, 1)))
    return [i * sum(value_map.get(letter, 0) for letter in name) for i, name in
            enumerate(myList, 1)]
###########
def name_value(my_list):
  result = []
  for i in range(len(my_list)):
      subtotal = 0
      for c in my_list[i]:
          if(c != ' '):
              subtotal += ord(c) - ord('a') + 1
      result.append(subtotal*(i+1))
  return result
###########
def name_value(s):
    return [sum(ord(c) - 96 for c in s[i] if c != ' ') * (i + 1) for i in range(0,len(s))]
############
def name_value(my_list):
    a = [list(i.replace(" ","")) for i in my_list]
    res = []
    for i,v in enumerate(a,1):
        val = []
        for j in v:
            val.append(ord(j)-96)
        res.append(sum(val)*i)
    return res
##############
def cnt(s):
    s = s.replace(" ","")
    return sum(map(lambda x: ord(x) - 96,s))

def name_value(my_list):
    return [*map(lambda x, y: x * cnt(y), range(1,len(my_list) + 1), my_list)]
###############
def str_val(s):
    return sum(ord(c) - ord('a') + 1 for c in s if c.isalpha())

def name_value(my_list):
    return [(p + 1)* str_val(s) for p, s in enumerate(my_list)]
##############
def name_value(my_list):
    return [sum(ord(k)-96 for k in x.replace(' ', ''))*(i+1) for i,x in enumerate(my_list)]
#############
def name_value(my_list):
    return [i*sum(ord(x)-96 for x in y.lower() if x.isalpha()) for i, y in enumerate(my_list, 1)]
#############
def name_value(my_list):
    result = []
    for a, b in enumerate(my_list):
        x = convert_str_to_int(b)
        result.append((a+1) * x)
    return result


def convert_str_to_int(s):
    result = 0
    for i in s:
        if i.isalpha():
            result += ord(i) - 96
    return result
#################
def name_value(my_list):
    ll = [list(l.replace(' ', '')) for l in my_list]
    print(ll)
    conv = [sum([ord(c)-96 for c in k]) for k in ll]
    return [i*k for i,k in enumerate(conv, start=1)]
