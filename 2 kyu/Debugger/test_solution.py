""" Retro compatibility with old solutions """
if 'attribute_accesses' in Debugger.__dict__:
    Debugger.attribute_acceses = Debugger.attribute_accesses


import random

class Goo(object, metaclass=Meta):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def foo(self, f):
        pass

    def goo(self, z):
        self.x = z
        
b = Goo(1, 2)
f = random.random()
b.foo(f)
x = random.randint(1, 100)
b.goo(x)


calls = Debugger.method_calls

test.assert_equals(len(calls), 3)

test.describe("Test collected method calls")

test.it("Call to init should be collected")
test.assert_equals(calls[0]['args'], (b, 1, 2))

test.it("Call to foo should be collected")
test.assert_equals(calls[1]['args'], (b, f,))

test.it("Call to goo should be collected")
test.assert_equals(calls[2]['args'], (b, x,))

test.describe("Test collected attribute accesses")
accesses = Debugger.attribute_acceses

test.assert_equals(len(accesses), 5)

test.it("Attribute set in init should be collected")
test.assert_equals(accesses[0]['action'], 'set')
test.assert_equals(accesses[0]['attribute'], 'x')
test.assert_equals(accesses[0]['value'], 1)

test.it("Method get should be collected too")
test.assert_equals(accesses[1]['action'], 'set')
test.assert_equals(accesses[1]['attribute'], 'y')

test.it("Attribute get should be collected")
test.assert_equals(accesses[2]['action'], 'get')
test.assert_equals(accesses[2]['attribute'], 'foo')

test.it("Attribute get should be collected")
test.assert_equals(accesses[3]['action'], 'get')
test.assert_equals(accesses[3]['attribute'], 'goo')

test.it("Attribute set in goo should be collected")
test.assert_equals(accesses[4]['action'], 'set')
test.assert_equals(accesses[4]['attribute'], 'x')
test.assert_equals(accesses[4]['value'], x)
