def make_negative( number ):
    if number == 0:
        return 0
    elif number > 0:
        return number * -1
    else:
        return number
################
def make_negative( number ):
    return -abs(number)
################
def make_negative( number ):
    return -number if number>0 else number
##############
def make_negative( number ):
    return (-1) * abs(number)
##############
def make_negative(number):
    if number >= 0:
        return (0 - number)
    else:
        return number
###############
def make_negative(n):
    return n if n <= 0 else -n
###############
def make_negative( number ):
    return number - number * 2 if number > 0 else number
###############
def make_negative( number ):
    if "-" in str(number):
      return(number)
    else:
      return int("-" + str(number))
################
def make_negative(number):
    return number if number <= 0 else number * -1
###############
def make_negative( number ):
    return 0 - abs(number)
###############
def make_negative( number ):
    number = int(number)      #Converts the given number into int type
    
    sq = (number)**(2)        #Squares the number. This will remove the negative sign.
    sqr = int((sq)**(0.5))    #Square roots the square of the number(sq). This will return the original/given number without any negative (-) sign.
    
    neg = (-+sqr)             #Adds a negative sign to sqr
    
    return neg
##################
import math as Mathematics
def make_negative( number ):
    if int(number) != 0:
        number_but_better = Mathematics.factorial(abs(number)) * 0
        number2 = number_but_better + number
        number3 = abs(number2)
        number4 = number2 * 0.1 * -1 * 10
        return -abs(number)
    else: return 0
###################
def make_negative( number ):
    return -number if number >= 0 else number
###################
def make_negative( number ):
    if number==0:
        return 0
    elif abs(number)==number:
        return -number
    else:
        return number
#################
def make_negative( number ):
    if number <= 0:
        return number 
    else:
        return ((number / number)-1)- number 
#################
def make_negative( number ):
    if number == 0:
        number = 0
    else:
        number = 0-abs(number)
    return number 
##################
def make_negative(n):
    if n < 0:
        return n
    else:
        return n * -1
