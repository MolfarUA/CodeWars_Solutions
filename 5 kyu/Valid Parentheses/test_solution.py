import codewars_test as test
from solution import valid_parentheses

def act(parens, expected):
    test.it(f"parens = '{parens}'")(
        lambda: test.assert_equals(valid_parentheses(parens), expected)
    )
    
@test.describe("Fixed Tests")
def fixed():
    act(")",False)
    act("(",False)
    act("",True)
    act("hi)(",False)
    act("hi(hi)",True)
    act("(",False)
    act("hi(hi)(",False)
    act("((())()())",True)
    act("(c(b(a)))(d)",True)
    act("hi(hi))(",False)
    act("())(()",False)

from random import randint

@test.describe("Random tests")
def _random():
    base="abcdefghijklmnopqrstuvwxyz()"
    isSol=lambda string: all([string[:i].count(")")<=string[:i].count("(") for i in range(len(string)+1)]) and string.count("(")==string.count(")")
    for _ in range(40):
        testlen=randint(5,40)
        teststring=["()","()()","(())","()(())()"][randint(0,3)]
        for i in range(testlen):
            pos=randint(0,len(teststring))
            teststring=teststring[:pos]+base[randint(0,len(base)-1)]+teststring[pos:]
        act(teststring,isSol(teststring))
