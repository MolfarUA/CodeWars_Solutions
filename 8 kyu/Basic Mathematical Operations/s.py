def basic_op(operator, value1, value2):
    if operator=='+':
        return value1+value2
    if operator=='-':
        return value1-value2
    if operator=='/':
        return value1/value2
    if operator=='*':
        return value1*value2
________________________________
def basic_op(operator, value1, value2):
    return eval("{}{}{}".format(value1, operator, value2))
________________________________
def basic_op(operator, value1, value2):
    return eval(str(value1) + operator + str(value2))
________________________________
def basic_op(operator, value1, value2):
    if operator == "+":
        return value1 + value2
    elif operator == "-":
        return value1 - value2
    elif operator == "*":
        return value1 * value2
    elif operator == "/":
        return value1 / value2
    else:
        print ("Unrecognized Operator. Abort.")
________________________________
def basic_op(o, a, b):
    return {'+':a+b,'-':a-b,'*':a*b,'/':a/b}.get(o)
________________________________
def basic_op(operator, value1, value2):
    return eval(f'{value1}{operator}{value2}')
________________________________
def basic_op(operator, value1, value2):
    ops = {'+': lambda a, b: a + b, 
           '-': lambda a, b: a - b,
           '*': lambda a, b: a * b,
           '/': lambda a, b: a / b}
    return ops[operator](value1, value2)
________________________________
def basic_op(operator, value1, value2):
    if operator == '+':
        return value1 + value2
    if operator == '-':
        return value1 - value2
    if operator == '*':
        return value1 * value2
    if operator == '/':
        return value1 / value2
________________________________
def basic_op(op, v1, v2):
    return v1+v2 if op == "+" else v1-v2 if op == "-" else  v1*v2 if op == "*" else  v1/v2
________________________________
def basic_op(operator, value1, value2):
    if operator == "+" :
        return value1 + value2
    elif operator == "-" :
        return value1 - value2
    elif operator == "*" :
        return value1 * value2
    elif operator == "/" :
        return value1/value2
    else:
        print("invalid")
________________________________
import operator
def basic_op(sign, value1, value2):
    op = {
        '+' : operator.add,
        '-' : operator.sub,
        '*' : operator.mul,
        '/' : operator.truediv
        }
    return (op[sign](value1, value2))
________________________________
def basic_op(operator, value1, value2):
    m_symbols = {'+': 'add', '-': 'sub', '*': 'mul', '/': 'truediv', '//': 'floordiv', '%': 'mod', '**': 'pow'}
    method = '__%s__' % m_symbols[operator]
    return getattr(value1, method)(value2)
________________________________
from operator import add, sub, mul, truediv
basic_op = lambda op, v1, v2 : {'+' : add, '-' : sub, '*' : mul, '/' : truediv}[op](v1, v2)
________________________________
from operator import add, sub, mul, truediv
ops = {'+' : add, '-' : sub, '*' : mul, '/' : truediv}
basic_op = lambda op, v1, v2 : ops[op](v1, v2)
________________________________
def basic_op(oper, v1, v2):
    n = {
        '+': v1 + v2,
        '-': v1 - v2,
        '/': v1 / v2,
        '*': v1 * v2
    }
    return n[oper]
________________________________
def basic_op(operator, v1, v2):
    answer = { '+': v1+v2 , '-' : v1-v2 , '*' : v1*v2 , '/' : v1/v2 }
    return answer[operator]
