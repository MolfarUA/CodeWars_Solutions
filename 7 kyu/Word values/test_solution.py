import string,random
  
try:
    user_solution = nameValue
except:
    user_solution = name_value

@test.describe("Fixed tests")
def fixed_tests():
    @test.it("")
    def f():
        test.assert_equals(user_solution(["codewars","abc","xyz"]),[88,12,225])
        test.assert_equals(user_solution(["abc abc","abc abc","abc","abc"]),[12,24,18,24])
        test.assert_equals(user_solution(["abc","abc","abc","abc"]),[6,12,18,24])
        test.assert_equals(user_solution(["abcdefghijklmnopqrstuvwxyz","stamford bridge","haskellers"]), [351,282,330])
        test.assert_equals(user_solution(["i love coding","better than pizza","i got this"]),[115,382,321])
        test.assert_equals(user_solution(["mercury","venus","earth mars","jupiter saturn","uranus neptune"]),[103, 162, 309, 768, 945])
        test.assert_equals(user_solution(["a cup","some tea","more coffee","one glass"]),[41, 156, 273, 368])
        test.assert_equals(user_solution(["a","e","i","o","u","the end"]),[1, 10, 27, 60, 105, 336])
        test.assert_equals(user_solution(["coding","better pizza","i got this too"]),[52, 296, 471])

@test.describe("Random tests")
def random_tests():
    def getRandomList():
        L = []
        rand1 = random.randrange(5,15)
        rand2 = random.randrange(4,10)
        for i in range(0,rand2):
            L.append(''.join(random.choice(string.ascii_lowercase) for i in range(rand1)))
        return L
        
    def solutionxyz (myList):   
        L,M = [],[]
        location = string.ascii_lowercase[:26]
        for i in myList:
            count = 0
            i = i.replace(" ", "")
    
            for j in range(0,len(i)):
                try:
                    add = 0 if i[j] == " " else location.index(i[j]) + 1
                    count += add
                except:
                    pass
            M.append(count)
        index = 0
        for i in range(1,len(M) + 1):
            pdt = M[index] * i
            L.append(pdt)
            index += 1
        return L
    
    
    @test.it("")
    def f():
        for i in range (20): 
            checkList = getRandomList()    
            expected = solutionxyz(checkList)
            test.assert_equals(user_solution(checkList), expected)
