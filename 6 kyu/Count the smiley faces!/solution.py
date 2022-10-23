583203e6eb35d7980400002a


from re import findall
def count_smileys(arr):
    return len(list(findall(r"[:;][-~]?[)D]", " ".join(arr))))
__________________________
def count_smileys(arr):
    eyes = [":", ";"]
    noses = ["", "-", "~"]
    mouths = [")", "D"]
    count = 0
    for eye in eyes:
        for nose in noses:
            for mouth in mouths:
                face = eye + nose + mouth
                count += arr.count(face)
    return count
__________________________
import re

def count_smileys(arr):
    return sum(1 for s in arr if re.match(r'\A[:;][-~]?[)D]\Z',s))
__________________________
def count_smileys(arr):
    count = 0
    if not arr:
      return 0
    smileys = [":)", ";)", ":~)", ";~)", ":-)", ";-)", ":D", ";D", ":~D", ";~D", ":-D", ";-D"]
    for i in arr:
      if i in smileys:
        count += 1
    return count
__________________________
def count_smileys(arr):
    import re
    smiley = re.compile(r"[:;][-~]?[)D]")
    return sum(bool(re.match(smiley, el)) for el in arr)
__________________________
def count_smileys(arr):
    c = 0
    print(arr)
    smilyFaces = [':D', ':~)', ';~D', ':)', ';-D', ';D', ':-D']

    for i in arr:
        if i in smilyFaces:
            c += 1
    return c
__________________________
def count_smileys(arr):
    eyes = [':', ';']
    noses = ['-', '~', '']
    mouthes = [')', 'D']
    num = 0
    
    for i in arr:
        if len(i) == 3:
            if i[0] in eyes:
                if i[1] in noses:
                    if i[2] in mouthes:
                        num+=1
        if len(i) == 2:
            if i[0] in eyes:
                if i[1] in mouthes:
                        num+=1
            
    return num#the number of valid smiley faces in array/list
__________________________
def count_smileys(arr):
    eyes = (':', ';')
    nose = ('-', '~')
    mouth = (')', 'D')
    
    counter = 0
    
    for face in arr:
        if len(face) == 2:
            if face[0] in eyes and face[1] in mouth:
                counter += 1
        elif len(face) == 3:
            if face[0] in eyes and face[1] in nose and face[2] in mouth:
                counter += 1
        else:
            counter += 0
    return counter
__________________________
def count_smileys(arr):
    lst = [i + j + k for i in ':;' for j in ('', '-', '~') for k in ')D']
    return sum(w in lst for w in arr)
__________________________
def count_smileys(arr,p=[':-)', ':-D', ':~)', ':~D', ';-)', ';-D', ';~)', ';~D', ':)', ':D', ';)', ';D']):
    return sum(x in p for x in arr)
__________________________
def count_smileys(arr):
    sum = 0
    count = 0
    print (arr)
    allowed = [":", ";", ")", "D", "-", "~"]
    for smile in arr:
        if not smile[0] in allowed or not smile[1] in allowed:
            continue 
        if len(smile) == 3:
            if not smile[2] in allowed:
                continue 
            
        if smile[0] in (":", ";") and smile[len(smile)-1] in (")", "D"):
                sum +=1
    return sum
