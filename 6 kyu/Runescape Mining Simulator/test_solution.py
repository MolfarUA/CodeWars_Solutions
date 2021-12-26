from solution import Miner
import codewars_test as test
from preloaded import EXPERIENCE, ROCKS

from copy import deepcopy
from random import choice, randint, shuffle

EXPERIENCE = {1: 0, 
              2: 83, 
              3: 174, 
              4: 276, 
              5: 388, 
              6: 512, 
              7: 650, 
              8: 801, 
              9: 969, 
              10: 1154, 
              11: 1358, 
              12: 1584, 
              13: 1833, 
              14: 2107, 15: 2411, 16: 2746, 17: 3115, 18: 3523, 19: 3973, 20: 4470, 21: 5018, 22: 5624, 23: 6291, 24: 7028, 25: 7842, 26: 8740, 27: 9730, 28: 10824, 29: 12031, 30: 13363, 31: 14833, 32: 16456, 33: 18247, 34: 20224, 35: 22406, 36: 24815, 37: 27473, 38: 30408, 39: 33648, 40: 37224}

ROCKS = {
    'Clay': (1, 5),
    'Copper': (1, 17.5),
    'Tin': (1, 17.5),
    'Iron': (15, 35),
    'Silver': (20, 40),
    'Coal': (30, 50),
    'Gold': (40, 65)
}

class _Miner:
    def __init__(self, xp=0):
        self.xp = xp
        self.level = next((lvl-1 for lvl, exp in EXPERIENCE.items() if exp > self.xp), 40)

    def mine(self, rock):
        if ROCKS[rock][0] > self.level:
            return f"You need a mining level of {ROCKS[rock][0]} to mine {rock}."
        else:
            self.xp += ROCKS[rock][1]
            if self.level < 40 and self.xp >= EXPERIENCE[self.level+1]:
                self.level += 1
                return f"Congratulations, you just advanced a Mining level! Your mining level is now {self.level}."
            else:
                return "You swing your pick at the rock."
            
@test.describe("Final tests")
def tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        m = Miner()
        for i in range(1, 6):
            if i <= 4:
                test.assert_equals(m.mine('Tin'), "You swing your pick at the rock.")
            else:
                test.assert_equals(m.mine('Tin'), 
                                   "Congratulations, you just advanced a Mining level! Your mining level is now 2.")
        test.assert_equals(m.mine('Gold'), 'You need a mining level of 40 to mine Gold.')
        for _ in range(4):
            m.mine('Copper')
        test.assert_equals(m.mine('Copper'), "Congratulations, you just advanced a Mining level! Your mining level is now 3.")
        for _ in range(5):
            m.mine('Copper')
        test.assert_equals(m.mine('Copper'), "Congratulations, you just advanced a Mining level! Your mining level is now 4.")
        test.assert_equals(m.mine('Copper'), "You swing your pick at the rock.")
        test.assert_equals(m.mine('Iron'), 'You need a mining level of 15 to mine Iron.')
        
        m = Miner()
        for i in range(1, 131):
            levels = [17, 35, 56, 78, 103, 130]
            res = m.mine('Clay')
            if i in levels:
                test.assert_equals(res, 
                                   f"Congratulations, you just advanced a Mining level! Your mining level is now {levels.index(i) + 2}.")
        
        m = Miner(3973)
        test.assert_equals(m.mine('Silver'), "You need a mining level of 20 to mine Silver.")
        
        m = Miner(4470)
        test.assert_equals(m.mine('Silver'), "You swing your pick at the rock.")
        
        m = Miner(5017)
        test.assert_equals(m.mine('Silver'), "Congratulations, you just advanced a Mining level! Your mining level is now 21.")
        test.assert_equals(m.mine('Coal'), "You need a mining level of 30 to mine Coal.")
    
    @test.it("Random Tests")
    def random_tests():
        tests = list(range(20))
        shuffle(tests)
        for i in tests:
            xp = randint(0, 50000) if i % 10 else 0
            user, ref = Miner(xp), _Miner(xp)
            for _ in range(50):
                ore = choice(list(ROCKS))
                test.assert_equals(user.mine(ore), ref.mine(ore))
