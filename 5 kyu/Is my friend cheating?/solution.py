import unittest

def removNb (n):
    seen = set()
    result = []
    total = sum (range (1, n+1))
    for item in range (1, n+1):
        searched = (total - item) / (item + 1)
        if searched in seen:
            result.append ((int(searched), item))
            result.append ((item, int(searched)))
        else:
            seen.add(item)
    return sorted (result, key=lambda minFirst: minFirst[0])

test = unittest.TestCase()

test.assertEquals(removNb(100), [])
test.assertEquals(removNb(26), [(15, 21), (21, 15)])
