def number_to_string(num):
    return str(num)
################
def number_to_string(num):
    try:
        return str(num)
    except:
        return None
##################
number_to_string = str
###############
number_to_string = lambda n: str(n)
###############
def number_to_string(num):
    return "{}".format(num)
##############
def number_to_string(num):
  if num < 0: return "-" + number_to_string(-num)
  if num == 0: return "0"
  
  s = ''
  
  while num > 0:
      a = num % 10
      s = chr(ord('0') + a) + s
      num = num // 10
      
  return s
####################
def number_to_string(num):
    return "%s" % num
###################
def number_to_string(num):
    num = int(num)
    num = str(num)
    return num
##################

def number_to_string(num):
    s = "0123456789"
    ret = ""
    n = 1
    isNegative = False

    #Check to see if the number is negative
    if(num < 0):
        num = num*-1
        isNegative = True 

    
    #123 % 10 = 3        First Digit
    #123 % 100 = 23      Second Digit = 23 - First Digit
    #123 % 1000 = 123    Third Digit = 123 - 2nd digit*10 - first digit

    while num != 0:
        d = num%10**n
        num = num - d
        ret += s[int(d/10**(n-1))]
        n += 1

    #if the number is negative then insert the '-' sign. 
    if isNegative: ret+="-"

    return ret[::-1]
