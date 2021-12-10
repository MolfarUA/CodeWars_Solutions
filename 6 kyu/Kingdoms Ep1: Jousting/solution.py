def joust(list_field: tuple, v_knight_left: int, v_knight_right: int) -> tuple:
    if v_knight_left == 0 and v_knight_right == 0:
        return list_field
    
    len1, len2 = len(list_field[0]), len(list_field[1])
    left_point, right_point = 2, len1 - 3
    
    while left_point < right_point:
        left_point += v_knight_left
        right_point -= v_knight_right
        
    return (" " * (left_point - 2) + "$->" + " " * (len1 - left_point -1),
           " " * right_point + "<-P" + " " * (len2 - right_point - 3))
  
#############
def joust(list_field: tuple, v_knight_left: int, v_knight_right: int) -> tuple:
    if v_knight_left == 0 and v_knight_right == 0:
        return list_field
    
    len1, len2 = len(list_field[0]), len(list_field[1])
    left_point, right_point = 2, len1 - 3
    
    while left_point < right_point:
        left_point  += v_knight_left
        right_point -= v_knight_right
    
    return (" " * (left_point - 2) + "$->" + " " * (len1 - left_point - 1),
            " " * right_point      + "<-P" + " " * (len2 - right_point - 3))
  
###########
def joust(lf: tuple, vkl: int, vkr: int) -> tuple:
    pos1 = lf[0].find(">")
    pos2 = lf[1].find("<")
    
    if pos1 >= pos2 or vkl == 0 and vkr == 0:
        return lf
    
    while pos2 > pos1:
        pos1 += vkl
        pos2 -= vkr
        
    res1 = list(" " * len(lf[0]))
    res2 = list(" " * len(lf[0]))
    
    res1[pos1] = "$->"
    res2[pos2] = "<-P"
    
    return ("".join(res1[2:]), "".join(res2[:-2]))
  
###############
from math import ceil

def joust(field, vL, vR):
    d, v = len(field[0]) - 5, vL + vR
    if v == 0 or d <= 0:
        return field
    (kL, kR), t = field, ceil(d / v)
    dL, dR = (-t * vL), (t * vR)
    return (kL[dL:] + kL[:dL], kR[dR:] + kR[:dR])
  
#############
def joust(list_field, left, right):

    if left == right == 0: return list_field
    x, y, length = 2, len(list_field[1])-3, len(list_field[0])
    
    while x < y:
        x += left
        y -= right
        
    _1, _2 = length * " ", length * " "
    _1 = _1[:x-2] + "$->" + _1[x+1:]
    _2 =   _2[:y] + "<-P" + _2[y+3:]
    
    return _1, _2
  
##############
from math import ceil
def joust(field, v1, v2):
    l = len(field[0])
    if v1+v2==0 or l<6: 
        return field
    s = ceil((l-5)/(v1+v2))
    s1 = s*v1 ; s2 = s*v2
    return (" "*s1 +'$->'+' '*(l-s1-3), " "*(l-s2-3) +'<-P'+' '*s2)
  
###############
def joust(list_field: tuple, v_knight_left: int, v_knight_right: int) -> tuple:
    FL = len(list_field[0])
    LK = list_field[0]
    RK = list_field[1]
    
    if LK.find(">") >= RK.find("<") or (v_knight_left == 0 and v_knight_right == 0):
        return list_field
    else:
        while LK.find(">") < RK.find("<"):
            LK = (v_knight_left*" "+LK.rstrip(" ")).ljust(FL, " ")
            RK = (RK.lstrip(" ")+" "*v_knight_right).rjust(FL, " ")
        return (LK,RK)
      
###############
def is_the_clash(l: str, r: str) -> bool:
    pos_l = l.find(">")
    pos_r = r.find("<")
    return pos_l >= pos_r

def move_knight(k_str: str, steps: int) -> str:
    which_knight = "l" if "$" in k_str else "r"
    if which_knight == 'l':
        res = k_str[-steps:] + k_str[:-steps]
    else:
        res = k_str[steps:] + k_str[:steps]
    return res


def joust(list_field: tuple, v_knight_left: int, v_knight_right: int) -> tuple:
    if v_knight_left == 0 and v_knight_right == 0:
        return list_field
    
    while not is_the_clash(*list_field):
        list_field = (move_knight(list_field[0], v_knight_left), move_knight(list_field[1], v_knight_right))
    return list_field
  
################
def joust(list_field: tuple, v_knight_left: int, v_knight_right: int) -> tuple:
    knight = list_field[0]
    spear = list_field[1]
    if len(knight) == 3:
        return list_field
    if v_knight_left == 0 and v_knight_right == 0:
        return list_field
    left_arrow = 2
    right_arrow = len(spear) - 3
    while left_arrow < right_arrow and left_arrow < len(spear) and right_arrow >= 0:
        print(left_arrow, right_arrow)
        if v_knight_left != 0:
            knight = " " * v_knight_left + knight
            knight = knight[:-v_knight_left]
        if v_knight_right != 0:
            spear = spear[v_knight_right:] + (" " * v_knight_right)
        left_arrow += v_knight_left
        right_arrow -= v_knight_right
        print(knight)
        print(spear)
    return (knight, spear)
  
################
def joust(list_field: tuple, v_knight_left: int, v_knight_right: int) -> tuple:
    
    (knight_left, knight_right) = list_field;
    
    for char in knight_left:
        if(knight_left.index('>') >= knight_right.index('<') or (v_knight_left == 0 and v_knight_right == 0)): return list_field
        else:
            knight_left = f"{v_knight_left*' '}{knight_left[0:(len(knight_left) - v_knight_left)]}"
            knight_right = f"{knight_right[(v_knight_right):]}{v_knight_right*' '}"
            list_field = (knight_left, knight_right)
            
################
def joust(list_field: tuple, v_knight_left: int, v_knight_right: int) -> tuple:
    kl = list(list_field[0])
    kr = list(list_field[1])
    print(list_field)
    while True:
        pl = kl.index('>')
        pr = kr.index('<')
        print(kl, pl)
        print(kr, pr)
        if pl >= pr:
            sol = [''.join(n) for n in (kl, kr)]
            print(sol)
            return (sol[0], sol[1])
        if v_knight_left == 0 and v_knight_right == 0:
            return list_field
        for i in range(v_knight_left):
            kl.pop()
            kl.insert(0, ' ')
        for i in range(v_knight_right):
            del kr[0]
            kr.append(' ')
            
#################
def joust(list_field: tuple, vl, vr) -> tuple:
    if vl + vr == 0:
        return list_field
    l, r = list_field
    while l.index('>') < r.index('<'):
        l = l[-vl:] + l[:-vl]
        r = r[vr:] + r[:vr]
    return l, r
  
###############
def joust(list_field: tuple, v_knight_left: int, v_knight_right: int) -> tuple:
    kl_str = list_field[0]
    kr_str = list_field[1]
    kl_spear_position = kl_str.find('>') # 3
    kr_spear_position = kr_str.find('<')
    
    # return kl_spear_position, kr_spear_position
    
# na tym etapie wiem jaka jest pozycja grotów
# "$->    " # spear position is 2 (range 0 to 6) or -7
# "    <-P" # spear position is 4 (range 0 to 6) or -3
    for i in range(len(list_field[0])):
        if kl_spear_position < kr_spear_position:
            kl_spear_position += v_knight_left
            kr_spear_position -= v_knight_right
            # print('running')
        else:
            if kl_spear_position > len(list_field[0]):
                kl_spear_position = len(list_field[0])
                if kr_spear_position < 0:
                    kr_spear_position = 0
            # return f'clash at ($->) {kl_spear_position} and (<-P) {kr_spear_position}'
            break

    
    kl_track = ""
    for field in range(len(list_field[0]) + 2):
        if field < (kl_spear_position - 2) or field > (kl_spear_position + 2):
            kl_track = kl_track + ' '
        elif field == kl_spear_position:
            kl_track = kl_track + '$->'           
    print(kl_track)

        
    kr_track = ""
    for field in range(len(list_field[0])):
        if field < kr_spear_position or field > (kr_spear_position + 2):
            kr_track = kr_track + ' '
        elif field == kr_spear_position:
            kr_track = kr_track + '<-P'
    print(kr_track)

    jousting = (kl_track, kr_track)
    
    return jousting
  
####################
def joust(list_field: tuple, v_knight_left: int, v_knight_right: int) -> tuple:
    if v_knight_left == 0 and v_knight_right == 0:
        return list_field
    else:
        list_field_list = [list_field[0], list_field[1]]
        while list_field_list[0].index(">") < list_field_list[1].index("<"):
            list_field_list[0] = ((" " * v_knight_left) + list_field_list[0])[:len(list_field_list[0])]
            list_field_list[1] = (list_field_list[1] + (" " * v_knight_right))[v_knight_right:]
        return (list_field_list[0], list_field_list[1])
