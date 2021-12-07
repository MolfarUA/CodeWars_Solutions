test.describe("Basic Tests")
test.assert_equals(split_the_bill({'A': 20, 'B': 15, 'C': 10}), {'A': 5.00, 'B': 0.00, 'C': -5.00})
test.assert_equals(split_the_bill({'A': 40, 'B': 25, 'X': 10}), {'A': 15.00, 'B': 0.00, 'X': -15.00})
test.assert_equals(split_the_bill({'A': 40, 'B': 25, 'C': 10, 'D': 153, 'E': 58}), {'A': -17.20, 'B': -32.20, 'C': -47.20, 'D': 95.80, 'E': 0.80})
test.assert_equals(split_the_bill({'A': 475, 'B': 384, 'C': 223, 'D': 111, 'E': 19}), {'A': 232.6, 'B': 141.6, 'C': -19.4, 'D': -131.4, 'E': -223.4})
test.assert_equals(split_the_bill({'A': 20348, 'B': 493045, 'C': 2948, 'D': 139847, 'E': 48937534, 'F': 1938724, 'G': 4, 'H': 2084}), {'A': -6421468.75, 'B': -5948771.75, 'C': -6438868.75, 'D': -6301969.75, 'E': 42495717.25, 'F': -4503092.75, 'G': -6441812.75, 'H': -6439732.75})

from random import randint,choice

def random_dict():
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    d = {}
    for i in range(randint(1,20)):
        d[''.join([choice(letters) for _ in range(randint(1,20))])] = randint(0,1000000)
    return d
    
test.describe("Random Tests")
for _ in range(100):
    d = random_dict()
    ans = {}
    average = sum(d.values()) / float(len(d))
    for key in d:
        ans[key] = round(d[key] - average,2)
    test.assert_equals(split_the_bill(d),ans)
