55cb632c1a5d7b3ad0000145



def hoopCount(n):
    return "Keep at it until you get it" if n<10 else "Great, now move on to tricks"
_____________________________
def hoopCount(n):
    if n>=10:
        return 'Great, now move on to tricks'
    else:
        return 'Keep at it until you get it'
_____________________________
def hoopCount(n):
    return "Great, now move on to tricks" if n >= 10 else "Keep at it until you get it"
_____________________________
def hoopCount(n):
    return ("Great, now move on to tricks", "Keep at it until you get it")[n < 10]
_____________________________
def hoopCount(n):
    if n > 9:
        return "Great, now move on to tricks"
    else: 
        return "Keep at it until you get it"
_____________________________
def hoop_count(n):
    messages = ['Keep at it until you get it','Great, now move on to tricks']
    return messages[0 if n < 10 else 1]
_____________________________
def hoop_count(n):
    result =""
    if(n >= 10):
        result = "Great, now move on to tricks"
    else:
        result = "Keep at it until you get it"
    return result

hoop_count(10)
_____________________________
def hoop_count(n):
    counter = 0
    for i in range(1, n + 1):
        counter += 1
    if counter >= 10:
        return 'Great, now move on to tricks'
    elif counter <= 9:
        return 'Keep at it until you get it'
_____________________________
def hoop_count(n):
    return "{s}".format(s="Keep at it until you get it" if n < 10 else "Great, now move on to tricks")
