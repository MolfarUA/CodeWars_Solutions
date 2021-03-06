def doTests():
    test.describe("Simple tests")
    test.assert_equals(find_outlier([0, 1, 2]), 1)
    test.assert_equals(find_outlier([1, 2, 3]), 2)
    
    
    test.describe("More complex tests")
    ints1 = [2,6,8,10,3]; # odd at the back
    ints2 = [2,6,8,200,700,1,84,10,4]; # odd in the middle
    ints3 = [17,6,8,10,6,12,24,36]; # odd in the front
    ints4 = [2,1,7,17,19,211,7]; # even in the front
    ints5 = [1,1,1,1,1,44,7,7,7,7,7,7,7,7]; # even in the middle
    ints6 = [3,3,3,3,3,3,3,3,3,3,3,3,3,3,35,5,5,5,5,5,5,5,5,5,5,7,7,7,7,1000]; # even at the end
    ints7 = [2,-6,8,-10,-3]; # odd at the back, negative
    ints8 = [2,6,8,2,-66,34,-35,66,700,1002,-84,10,4]; # odd in the middle, negative
    ints9 = [-123456789,-18,6,-8,-10,6,12,-24,36]; # odd in the front, negative
    ints10 = [-20,1,7,17,19,211,7]; # even in the front, negative
    ints11= [1,1,-1,1,1,-44,7,7,7,7,7,7,7,7]; # even in the middle, negative
    ints12 = [1,0,0]; # odd answer, zeroes
    ints13 = [3,7,-99,81,90211,0,7]; # even in the middle, zero
    
    inputs = [ints1, ints2, ints3, ints4, ints5, ints6, ints7, ints8, ints9, ints10, ints11, ints12, ints13]
    expected = [3, 1, 17, 2, 44, 1000, -3, -35, -123456789, -20, -44, 1, 0]
    
    for i, (ins, e) in enumerate(zip(inputs, expected)):
        #test.it("Test {} - Trying: {}".format(i, ins))
        test.assert_equals(find_outlier(ins), e)
        
    test.describe("Random tests")
    import random
    for _ in range(20):
        test_integers = []
        odds = []
        evens = []
    
        is_odd = random.choice([True, False])
        base = 10000000
        expected = None
        if is_odd:
            odds.append(random.randrange(-base + 1, base + 1, 2))
            for _ in range(random.randint(10, 50)):
                evens.append(random.randrange(-base, base, 2))
            expected = odds[0]
        else:
            evens.append(random.randrange(-base, base, 2))
            for _ in range(random.randint(10, 50)):
                odds.append(random.randrange(-base + 1, base + 1, 2))
            expected = evens[0]
    
        test_integers = odds + evens
        random.shuffle(test_integers)
        test.it("Testing: {}.  Expected: {}".format(test_integers, expected))
        test.assert_equals(find_outlier(test_integers), expected)
doTests()
