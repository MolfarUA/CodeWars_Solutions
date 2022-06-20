57e8f757085f7c7d6300009a



def plane_seat(a):
    front, middle, back = (range(1,21), range(21,41), range(41,61))
    left, center, right = ('ABC', 'DEF', "GHK")
    x, y = ('', '')
        
    if int(a[:-1]) in front:    x = 'Front-'
    if int(a[:-1]) in middle:   x = 'Middle-'
    if int(a[:-1]) in back:     x = 'Back-'

    if a[-1] in left:    y = 'Left'
    if a[-1] in center:  y = 'Middle'
    if a[-1] in right:   y = 'Right'
    
    return x+y if all((x,y)) else 'No Seat!!'
_______________________________
def plane_seat(a):
    n, c = int(a[:-1]), a[-1]
    side = "Left" if c in "ABC" else "Middle" if c in "DEF" else "Right" if c in "GHK" else ""
    depth = "Front" if 0 < n < 21 else "Middle" if 20 < n < 41 else "Back" if 40 < n < 61 else ""
    return f"{depth}-{side}" if depth and side else "No Seat!!"
_______________________________
def plane_seat(a):
    row = int(a[:-1])
    seat = a[-1]
    
    if row > 60 or seat not in 'ABCDEFGHK':
        return 'No Seat!!'
        
    if row <= 20:
        end = 'Front'
    elif row <= 40:
        end = 'Middle'
    else:
        end = 'Back'
        
    if seat in 'ABC':
        side = 'Left'
    elif seat in 'DEF':
        side = 'Middle'
    else:
        side = 'Right'
        
    return f'{end}-{side}'
_______________________________
def plane_seat(a):
    section = ['Front','Middle','Back',None]
    cluster = {'ABC':'Left','DEF':'Middle','GHK':'Right'}
    my_section = section[((int(a[:-1])-1)//20)]
    my_cluster = [v for k,v in cluster.items() if a[-1].upper() in k]
    return "No Seat!!" if not (my_section and my_cluster) else "{}-{}".format(my_section,my_cluster[0])
_______________________________
def plane_seat(a):
    num, alpha = int(a[:-1]), a[-1]
    if num > 60 or alpha in 'IJ' or alpha > 'K':
        return 'No Seat!!'
    section = ('Front', 'Middle', 'Back')[(num > 20) + (num > 40)]
    cluster = ('Left', 'Middle', 'Right')[(alpha > 'C') + (alpha > 'F')]
    return f'{section}-{cluster}'
_______________________________
def plane_seat(a):
    a, b = int(a[:-1]), a[-1:]
    a, b = 'Front' if a>0 and a<21 else 'Middle' if a<41 else 'Back' if a<61 else '', 'Left' if b in 'ABC' else 'Middle' if b in 'DEF' else 'Right' if b in 'GHK' else ''
    return 'No Seat!!' if not (a and b) else a+'-'+b
_______________________________
import string
def plane_seat(a):
    number = int(a[:-1])
    letter = a[-1]
    result = ""
    alphabet = string.ascii_uppercase.replace("IJ", "")
    left = alphabet[:3]
    middle = alphabet[3:6]
    right = alphabet[6:11]
    if 1 <= number <= 20:
        result += "Front-"
    elif 21 <= number <= 40:
        result += "Middle-"
    elif 41 <= number <= 60:
        result += "Back-"
    else:
        return "No Seat!!"
    
    if letter in left:
        result += "Left"
    elif letter in middle:
        result += "Middle"
    elif letter in right:
        result += "Right"
    else:
        return "No Seat!!"
    return result
_______________________________
def plane_seat(a):
    res = ''
    if int(a[:-1]) <= 20: res += 'Front-'
    elif int(a[:-1]) <= 40: res += 'Middle-'
    elif int(a[:-1]) <= 60: res += 'Back-'
    else: return 'No Seat!!'
    if a[-1] in 'ABC': res += 'Left'
    elif a[-1] in 'DEF': res += 'Middle'
    elif a[-1] in 'GHK': res += 'Right'
    else: return 'No Seat!!'
    return res
_______________________________
def plane_seat(a):
    seat = {'A': 'Left','B': 'Left','C': 'Left','D': 'Middle','E': 'Middle',
            'F': 'Middle','G': 'Right','H': 'Right','K': 'Right'}
    position =''
    front_back, left_right = a[:-1], a[-1]
    if(int(front_back) >= 1 and int(front_back) < 21): position = 'Front'
    elif(int(front_back) > 20 and int(front_back) < 41): position = 'Middle'
    else: position ='Back'
    
    if(left_right not in seat): return 'No Seat!!'
    if(int(front_back) > 60 or int(front_back) < 0): return 'No Seat!!'
    
    
    return f'{position}-{seat[left_right]}'
_______________________________
def plane_seat(a):
    a, b = int(a[:-1]), a[-1:]
    a, b = 'Front' if a>0 and a<21 else 'Middle' if a<41 else 'Back' if a<61 else '', 'Left' if b in 'ABC' else 'Middle' if b in 'DEF' else 'Right' if b in 'GHK' else ''
    return 'No Seat!!' if not (a and b) else a+'-'+b
