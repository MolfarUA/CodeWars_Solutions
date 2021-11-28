def valid_parentheses(string):
    unmatched_opens = 0

    for character in string:
        if character == "(":
            unmatched_opens += 1
        elif character == ")":
            if unmatched_opens > 0:
                unmatched_opens -= 1
            else:
                return False

    return unmatched_opens == 0
#######################
def valid_parentheses(string):
    cnt = 0
    for char in string:
        if char == '(': cnt += 1
        if char == ')': cnt -= 1
        if cnt < 0: return False
    return True if cnt == 0 else False
###############
def valid_parentheses(string):
    count = 0
    for i in string:
        if i == "(":
            count += 1
        elif i == ")":
            count -= 1
        if count < 0:
            return False
    return count == 0
#################
def valid_parentheses(string):
    string = "".join(ch for ch in string if ch in "()")
    while "()" in string: string = string.replace("()", "")
    return not string
################
iparens = iter('(){}[]<>')
parens = dict(zip(iparens, iparens))
closing = parens.values()

def valid_parentheses(astr):
    stack = []
    for c in astr:
        d = parens.get(c, None)
        if d:
            stack.append(d)
        elif c in closing:
            if not stack or c != stack.pop():
                return False
    return not stack
###################
class Stack:
    """
    This is an implementation of a Stack.
    The "right" or "top" of this stack the end of the list.
    """

    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def is_empty(self):
        return self.items == []

    def size(self):
        return len(self.items)

def valid_parentheses(symbol_string):
    """
    This is a practice problem.
    It checks to see if parenthesis's are balanced
    :param symbol_string: String
    :return Bool:
    """

    stack = Stack()
    for char in symbol_string:
        if char == "(":
            stack.push("(")
        elif char == ")":
            if stack.is_empty():
                return False
            else:
                stack.pop()

    if not stack.is_empty():
        return False
    else:
        return True
####################################
import re

def valid_parentheses(s):
    try:
        re.compile(s)
    except:
        return False
    return True
###################
import re


_regex = "[^\(|\)]"


def valid_parentheses(string):
    string = re.sub(_regex, '', string)
    while len(string.split('()')) > 1:
        string = ''.join(string.split('()'))
    return string == ''
####################
def valid_parentheses(s):
    stack = 0
    for char in s:
        if char == '(':
            stack += 1
        if char == ')':
            if not stack:
                return False
            else:
                stack -= 1
    return not stack
################
def valid_parentheses(s):
    b = 0
    for c in s:
        if c == '(': b += 1
        if c == ')':
            b -= 1
            if b < 0: return False
    return b == 0
##################
def valid_parentheses(string):
    new = ''.join([i for i in string if i in '()'])
    while '()' in new:
        new = new.replace('()', '')
    return len(new) == 0
####################
def valid_parentheses(string):
  open_counter = 0 
  for i in string:
      if i=='(':         open_counter = open_counter + 1
      if i==')':         open_counter = open_counter - 1
      if open_counter<0: return False
  if open_counter==0:    return True
  return False
###############
valid_parentheses=lambda s:(not s) or s.count('(')==s.count(')')and s.rfind('(')<s.rfind(')')
###################
def valid_parentheses(string):
    string = "".join([x for x in string if x == "(" or x == ")"])
    before_reduce = len(string)
    string = string.replace('()', '')
    if string == '':
        return True
    elif before_reduce != len(string):
        return valid_parentheses(string)
    else:
        return False
####################
def valid_parentheses(string):
    string = ''.join(x for x in string if x in ('(',')'))
    while '()' in string:
         string = string.replace('()', '')
    return False if len(string) != 0 else True
################
def valid_parentheses(string):
    left = 0
    right = 0
    for i in string:
        print(i)
        if i == "(":
            left += 1
        elif i == ")":
            right += 1
            if right > left:
                return False
    return True if left == right else False
################
def valid_parentheses(string):
    string = [c for c in string if not c.isalpha()]
    string = "".join(string)
    while "()" in string:
        string = string.replace("()","")
    return True if len(string) == 0 else False
##############
def valid_parentheses(s):
    p = '()'
    s = ''.join([e  for e in s if e in '()'])
    while p in s:#
        s = s.replace(p,'')
    return not s
###################
import re
def valid_parentheses(string):
    s = re.sub('[^()]','',string)
    s = re.sub('\(\)','',s)
    return True if not s else valid_parentheses(s) if s != string else False
