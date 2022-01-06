from itertools import permutations
import math
def equal_to_24(*aceg):
    ops = '+-*/'
    
    OPS = {
        '+': lambda a,b: a + b,
        '-': lambda a,b: a - b,
        '*': lambda a,b: a * b,
        '/': lambda a,b: a / b if b else math.inf
    }
    
    for b in ops:
        for d in ops:
            for f in ops:
                for (a,c,e,g) in permutations(aceg):
                    B,D,F = OPS[b], OPS[d], OPS[f]
                    for (i,exp) in enumerate(make_exp(a,B,c,D,e,F,g)):
                        if exp == 24:
                            return make_string(a,b,c,d,e,f,g)[i]
                            
                            
    return "It's not possible!"

def make_exp(a,b,c,d,e,f,g):
  return [ 
    f(d(b(a,c),e),g),
    d(b(a,c),f(e,g)),
    b(a,d(c,f(e,g))),
    b(a,f(d(c,e),g)),
    f(b(a,d(c,e)),g)]

def make_string(a,b,c,d,e,f,g):
    return [f"(({a}{b}{c}){d}{e}){f}{g}",
            f"({a}{b}{c}){d}({e}{f}{g})",
            f"{a}{b}({c}{d}({e}{f}{g}))",
            f"{a}{b}(({c}{d}{e}){f}{g})",
            f"({a}{b}({c}{d}{e})){f}{g}"]
_____________________________________________
from operator import add, sub, mul
from itertools import *

div = lambda x, y: 9999999 if y == 0 else x / y

def equal_to_24(*numbers):
  for a,b,c,d in permutations(numbers):
    for x,y,z in product([(add,'+'),(sub,'-'),(mul,'*'),(div,'/')], repeat=3):
      if 24 == x[0](y[0](a, b), z[0](c, d)):
        return '({}{}{}){}({}{}{})'.format(a,y[1],b,x[1],c,z[1],d)
      if 24 == x[0](y[0](z[0](a, b), c), d):
        return '(({}{}{}){}{}){}{}'.format(a,z[1],b,y[1],c,x[1],d)
      if 24 == x[0](y[0](a, z[0](b, c)), d):
        return '({}{}({}{}{})){}{}'.format(a,y[1],b,z[1],c,x[1],d)
      if 24 == x[0](a, y[0](b, z[0](c, d))):
        return '{}{}({}{}({}{}{}))'.format(a,x[1],b,y[1],c,z[1],d)
        
  return "It's not possible!"
_____________________________________________
from itertools import permutations


def equal_to_24(a1, b1, c1, d1):
    for (a, b, c, d) in permutations([a1, b1, c1, d1], 4):
        option = equal_to_24_with_2(a, b, c, d)
        if option:
            return option.replace("a", str(a)).replace("b", str(b)).replace("c", str(c)).replace("d", str(d))
        option = equal_to_24_with_3(a, b, c, d)
        if option:
            return option.replace("a", str(a)).replace("b", str(b)).replace("c", str(c)).replace("d", str(d))

    return "It's not possible!"


def equal_to_24_with_2(a, b, c, d):
    options = (
        [(a + b) + (c + d) - 24, "(a+b)+(c+d)"],
        [(a + b) + (c - d) - 24, "(a+b)+(c-d)"],
        [(a - b) + (c + d) - 24, "(a-b)+(c+d)"],
        [(a - b) + (c - d) - 24, "(a-b)+(c-d)"],
        [(a + b) - (c + d) - 24, "(a+b)-(c+d)"],
        [(a + b) - (c - d) - 24, "(a+b)-(c-d)"],
        [(a - b) - (c + d) - 24, "(a-b)-(c+d)"],
        [(a - b) - (c - d) - 24, "(a-b)-(c-d)"],
        [(a + b) * (c + d) - 24, "(a+b)*(c+d)"],
        [(a + b) * (c - d) - 24, "(a+b)*(c-d)"],
        [(a - b) * (c + d) - 24, "(a-b)*(c+d)"],
        [(a - b) * (c - d) - 24, "(a-b)*(c-d)"],
        [(a + b) / (c + d) - 24, "(a+b)/(c+d)"],
        [safe_div((a + b), (c - d)) - 24, "(a+b)/(c-d)"],
        [(a - b) / (c + d) - 24, "(a-b)/(c+d)"],
        [safe_div((a - b), (c - d)) - 24, "(a-b)/(c-d)"],
        [(a * b) - (c * d) - 24, "(a*b)-(c*d)"],
        [(a / b) - (c / d) - 24, "(a/b)-(c/d)"],
        [(a * b) - (c / d) - 24, "(a*b)-(c/d)"],
        [(a / b) - (c * d) - 24, "(a/b)-(c*d)"],
        [(a * b) + (c * d) - 24, "(a*b)+(c*d)"],
        [(a / b) + (c / d) - 24, "(a/b)+(c/d)"],
        [(a * b) + (c / d) - 24, "(a*b)+(c/d)"],
        [(a / b) + (c * d) - 24, "(a/b)+(c*d)"],

    )
    for option in options:
        if option[0] == 0:
            return option[1]
    return None


def equal_to_24_with_3(a, b, c, d):
    options = (
        [b + c + d, "(b+c+d)"],
        [b - c - d, "(b-c-d)"],
        [b * c * d, "(b*c*d)"],
        [b / c / d, "(b/c/d)"],
        [b + c - d, "(b+c-d)"],
        [b - c + d, "(b-c+d)"],
        [b + c / d, "(b+c/d)"],
        [b / c + d, "(b/c+d)"],
        [b + c * d, "(b+c*d)"],
        [b * c + d, "(b*c+d)"],
        [b / c - d, "(b/c-d)"],
        [b - c / d, "(b-c/d)"],
        [b * c - d, "(b*c-d)"],
        [b + c / d, "(b+c/d)"],
        [b / c * d, "(b/c*d)"],
        [b * c / d, "(b*c/d)"],
        [b - (c + d), "b-(c+d)"],
        [b - (c - d), "b-(c-d)"],
        [b * (c + d), "b*(c+d)"],
        [b * (c - d), "b*(c-d)"],
        [safe_div(b, (c + d)), "(b/(c+d))"],
        [safe_div(b, (c - d)), "(b/(c-d))"],
        [(b + c) * d, "((b+c)*d)"],
        [(b + c) / d, "((b+c)/d)"],
        [(b - c) * d, "((b-c)*d)"],
        [(b - c) / d, "((b-c)/d)"],
        [(b - (c * d)), "(b-(c*d))"],
        [(b - (c / d)), "(b-(c/d))"],
        [(b / c) - d, "((b/c)-d)"]
    )

    for option in options:
        res = option[0]
        if safe_div(24, res) == a:
            return "a*" + option[1]
        elif 24 * res == a:
            return "a/" + option[1]
        elif 24 + res == a:
            return "a-" + option[1]
        elif 24 - res == a:
            return "a+" + option[1]
        elif res - 24 == a:
            return option[1] + "-a"
        elif res / 24 == a:
            return option[1] + "/a"
        elif res * 24 == a:
            return option[1] + "*a"

    return None
    
def safe_div(num1, num2):
    if num2==0:
        return 99999
    else:
        return num1 / num2
      
_____________________________________________
import itertools

def solve(numbers, goal=24, expr=[]):
    if expr == []:
        expr = [str(n) for n in numbers]
    if len(numbers) == 1:
        if numbers[0] == goal:
            return numbers[0]
        else:
            return False
    if len(numbers) == 2:
        answers, answer_exps = combinetwo(numbers[0], numbers[1])
        for i,answer in enumerate(answers):
            if answer == goal:
                return convert_expr_to_string(expr[0], expr[1], answer_exps[i])
        return False

    pairs = set(itertools.combinations(numbers, 2))
    for pair in pairs:
        possible_values, possible_expr = combinetwo(*pair)
        for counter, value in enumerate(possible_values):
            expression = possible_expr[counter]
            a_index = numbers.index(pair[0])
            b_index = numbers.index(pair[1])
            if a_index == b_index:
                b_index = numbers.index(pair[1], a_index + 1);

            expr_string = convert_expr_to_string(expr[a_index], expr[b_index], expression)
            newlist = numbers[:]
            newexpr = expr[:]
            
            # replace the two numbers with the combined result
            a_index = newlist.index(pair[0])
            newlist.pop(a_index)
            b_index = newlist.index(pair[1])
            newlist.pop(b_index)
            newlist.append(value)

            # order matters
            newexpr.pop(a_index)
            newexpr.pop(b_index)
            newexpr.append(expr_string)
            result = solve(newlist, goal, newexpr)
            if result:
                return remove_redundant_brackets(result)
            else:
                continue

def convert_expr_to_string(a, b, expr):
    temp = [a, b]
    result = '(' + str(temp[expr[0]]) + ')' + str(expr[1]) + '(' + str(temp[expr[2]]) + ')'
    return result

def combinetwo(a, b):
    result = [a + b, a * b]
    expr = [(0, '+', 1), (0, '*', 1)]
    if b > a:
        result.append(b-a)
        expr.append((1, '-', 0))
    else:
        result.append(a-b)
        expr.append((0, '-', 1))
    if b != 0:
        result.append(a / b)
        expr.append((0, '/', 1))
    if a != 0:
        result.append(b / a)
        expr.append((1, '/', 0))
    return result, expr

def remove_redundant_brackets(expr):
    stack = []
    # indices to be deleted
    indices = []
    for i, ch in enumerate(expr):
        if ch == '(':
            stack.append(i)
        if ch == ')':
            last_bracket_index = stack.pop()
            enclosed = expr[last_bracket_index + 1:i]
            if enclosed.isdigit():
                indices.append(i)
                indices.append(last_bracket_index)
    return "".join([char for idx, char in enumerate(expr) if idx not in indices])

def equal_to_24(a,b,c,d):
    num = [a,b,c,d]
    
    r = solve(num, goal=24)
    if r:
        return r
    else:
        return "It's not possible!"
_____________________________________________
import itertools
def equal_to_24(a,b,c,d):
    result = solve([a,b,c,d], expr = [])
    if result == None:
        return "It's not possible!"
    return result
#credit to Lingyi Hu - modified ver of his code

#recursively solves by taking every pair of numbers, doing an operation and 
#placing brackets around, then repeating til only 2 elements of list remain
def solve(numbers, expr=[]):
    if expr == []:
        expr = [str(n) for n in numbers]
    if len(numbers) == 2:
        answers, answer_exps = combinetwo(numbers[0], numbers[1])
        for i,answer in enumerate(answers):
            if answer == 24:
                return convert_expr_to_string(expr[0], expr[1], answer_exps[i])
        return False

    pairs = set(itertools.combinations(numbers, 2))
    for pair in pairs:
        possible_values, possible_expr = combinetwo(*pair)
        for counter, value in enumerate(possible_values):
            expression = possible_expr[counter]
            a_index = numbers.index(pair[0])
            b_index = numbers.index(pair[1])
            if a_index == b_index:
                b_index = numbers.index(pair[1], a_index + 1);

            expr_string = convert_expr_to_string(expr[a_index], expr[b_index], expression)
            newlist = numbers[:]
            newexpr = expr[:]
            
            # replace the two numbers with the combined result
            a_index = newlist.index(pair[0])
            newlist.pop(a_index)
            b_index = newlist.index(pair[1])
            newlist.pop(b_index)
            newlist.append(value)

            # order matters
            newexpr.pop(a_index)
            newexpr.pop(b_index)
            newexpr.append(expr_string)
            result = solve(newlist, newexpr)
            if result:
                return remove_redundant_brackets(result)
            else:
                continue
            
#converts the expression we find to a string (called in every recursion of solve())
def convert_expr_to_string(a, b, expr):
    temp = [a, b]
    result = '(' + str(temp[expr[0]]) + ')' + str(expr[1]) + '(' + str(temp[expr[2]]) + ')'
    return result
# combines operations on any pair of numbers - used to reduce elements in every recursion
# and find final answer in last recursion
    
def combinetwo(a, b):
    result = [a + b, a * b]
    expr = [(0, '+', 1), (0, '*', 1)]
    if b > a:
        result.append(b-a)
        expr.append((1, '-', 0))
    else:
        result.append(a-b)
        expr.append((0, '-', 1))
    if b != 0:
        result.append(a / b)
        expr.append((0, '/', 1))
    if a != 0:
        result.append(b / a)
        expr.append((1, '/', 0))
    return result, expr

#removes redundant brackets
def remove_redundant_brackets(expr):
    stack = []
    # indices to be deleted
    indices = []
    for i, ch in enumerate(expr):
        if ch == '(':
            stack.append(i)
        if ch == ')':
            last_bracket_index = stack.pop()
            enclosed = expr[last_bracket_index + 1:i]
            if enclosed.isdigit():
                indices.append(i)
                indices.append(last_bracket_index)
    return "".join([char for idx, char in enumerate(expr) if idx not in indices])
