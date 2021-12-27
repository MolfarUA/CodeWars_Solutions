from solution import initial_state, trigger_state, normal_rule, first_rule, last_rule
import codewars_test as test

states={initial_state, trigger_state}
def catch_states(func):
    def inner(*args):
        state=func(*args)
        states.add(state)
        return state
    return inner

first_rule=catch_states(first_rule)
last_rule=catch_states(last_rule)
normal_rule=catch_states(normal_rule)


def step(squad):
    n=len(squad)
    newsquad=[first_rule(*squad[:2])]
    for i in range(1,n-1):
        newsquad.append(normal_rule(*squad[i-1:i+2]))
    newsquad.append(last_rule(*squad[-2:]))
    return newsquad


def run(size, trigger_time=0):
    squad=[initial_state]*size
    for _ in range(trigger_time):
        squad=step(squad)
        if 'fire' in squad:
            return False
    squad[0]=trigger_state
    while True:    
        squad=step(squad)
        if 'fire' in squad:
            if all(s=='fire' for s in squad):
                return True
            return False

@test.describe("Fixed tests")
def fixed_tests():
    @test.it("Should work for a few robots")
    def test1():
        for i in range(2,7):          
            test.expect(run(i), f"failed for {i} robots")
    @test.it("Should work for any trigger time")
    def test2():
        for t in (0,1,2,3,10):
            test.expect(run(7, t), f"failed for a trigger time of {t}")
    @test.it("Should work for many robots")
    def test3():
        test.expect(run(100), "failed for 100 robots")
        states=set()
        test.expect(run(1000), "failed for 1000 robots")
    @test.it("Should not use more than 50 states")
    def test4():
        test.expect(len(states)<=50, f"{len(states)} states used")
        
from random import randint, shuffle
@test.describe("Random tests")
def test5():
    for _ in range(10):
        test.expect(run(randint(2,100), randint(0,10)))
 
def shuffle_step(squad):
    n=len(squad)
    l=list(range(n))
    shuffle(l)
    newsquad=[None]*n
    for i in l:
        if i==0:
            newsquad[i]=first_rule(*squad[:2])
        elif i==n-1:
            newsquad[i]=last_rule(*squad[-2:])
        else:
            newsquad[i]=normal_rule(*squad[i-1:i+2])
    return newsquad

@test.describe("Crossed tests")
def test_6():
    n=randint(5,10)
    squads=[[initial_state]*randint(10,50) for _ in range(n)] 
    trigger_times=[randint(0,30) for _ in range(n)]
    done=[False]*n
    time=0
    while not all(done):
        for i in range(n):
            if not done[i]:
                if trigger_times[i]==time:
                    squads[i][0]=trigger_state
                squads[i]=shuffle_step(squads[i])
                if 'fire' in squads[i]:
                    if all(s=='fire' for s in squads[i]):
                        if time>=trigger_times[i]:      
                            done[i]=True
                        else:
                            test.fail("fired before trigger")
                    else :
                        return test.fail("robots failed to fire in sync")
        time+=1
    return test.pass_()
