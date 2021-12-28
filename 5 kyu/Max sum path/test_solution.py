import codewars_test as test
from solution import max_sum_path
from random import *
from random import randrange as rand

@test.describe('Max Sum Path')
def tests():
    @test.it('Example tests')
    def test_cipher_text():
        test.assert_equals(max_sum_path([2, 3, 7, 10, 12],[1, 5, 7, 8]), 35)
        test.assert_equals(max_sum_path([1,2,3], [3,4,5]), 15)
        test.assert_equals(max_sum_path([1,4,5,8,9,11,19], [2,3,4,11,12]), 61)
        test.assert_equals(max_sum_path([1,2,3], [4,5,6]), 15)
        test.assert_equals(max_sum_path([],[]),0)
        

@test.describe('Random tests')
def random_tests():
    
    def sol(l1, l2):
        i, j = 0, 0
        sum1, sum2 = 0, 0

        while i < len(l1) and j < len(l2):
            if l1[i] < l2[j]:
                sum1 += l1[i]
                i += 1
            elif l1[i] > l2[j]:
                sum2 += l2[j]
                j += 1
            else:
                sum1 =  sum2 = max(sum1, sum2) + l1[i]
                i += 1
                j += 1

        sum1 += sum(l1[i:])
        sum2 += sum(l2[j:])


        return max(sum1, sum2) #, res
    
    
    
    def randGen(nCommon, high, size):
        s = rand(size, size+1+size//10) * 2
        
        upCommon = s//2
        if upCommon>nCommon*100 and not rand(5):
            upCommon = nCommon*100
        common = s - rand(nCommon * bool(rand(10)), upCommon)
        
        i = rand(s-common or 1)
        if high<s: high = s
        lst = sample(range(high), s)
        
        a,b,c = lst[:i], lst[i:common], lst[common:]
        #print(i, common-i, s-common)
        
        return sorted(a+c)[:size], sorted(b+c)[:size]
    
    
    TESTS = [
        ('Small Range',  2,100,10,50),
        ('Medium Range', 10,1000,700,50),
        ('Turbo Large Range', 10,100000,70000,20),
    ]
    
    for title,common,high,size,nTests in TESTS:
        @test.it(title)
        def random_tests():
            for _ in range(nTests):
                a,b = randGen(common,high,size)
                exp = sol(a,b)
                test.assert_equals(max_sum_path(a,b),exp)
                
