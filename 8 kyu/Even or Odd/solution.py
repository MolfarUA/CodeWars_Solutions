def even_or_odd(number):
    if number % 2 == 0:
        return "Even"
    else:
        return "Odd"
###############
def even_or_odd(number):
    return 'Odd' if number % 2 else 'Even'
###############
def even_or_odd(number):
  return ["Even", "Odd"][number % 2]
###############
def even_or_odd(number):
  return 'Even' if number % 2 == 0 else 'Odd'
###############
def even_or_odd(number):
  return 'Odd' if number & 1 else 'Even'
###############
def even_or_odd(number):
  # number % 2 will return 0 for even numbers and 1 for odd ones.
  # 0 evaluates to False and 1 to True, so we can do it with one line
  return "Odd" if number % 2 else "Even"
####################
even_or_odd=lambda n:'EOvdedn'[n%2::2]
################
even_or_odd = lambda number: "Odd" if number % 2 else "Even"
#################
def even_or_odd(number):
  if number % 2 == 0:
    return "Even"
  else:
    return "Odd"
###################
def even_or_odd(number):
  return number % 2 and 'Odd' or 'Even'
###################
def even_or_odd(number):
    if number % 2:
        return "Odd"
    return "Even"
################
even_or_odd=lambda n:('Even','Odd')[n%2]
###################
def even_or_odd(number):
  return ("Even", "Odd")[number%2]
###################
def even_or_odd(number):
    status = ""
    if number % 2 == 0:
        status = "Even"
    else:
        status = "Odd"
    
    return status
###################
even_or_odd = lambda n: ["Even","Odd"][n % 2]
###################
def even_or_odd(number):
    even_or_odd = {0: "Even", 1: "Odd"}
    return even_or_odd[number % 2]
#####################
even_or_odd = lambda i: 'Odd' if i&1 else 'Even'
################
def even_or_odd(n):
    return "Odd" if n & 1 else "Even"
##################
def even_or_odd(number):
  output = ["Even", "Odd"]
  return output[(number % 2)]
