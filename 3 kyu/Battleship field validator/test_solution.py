try: validate_battlefield = validateBattlefield        # retro compatibility with previous solutions
except NameError: pass



# reference solution

# function that look for given ship in field. Count them and returns true if numbers of objects is equal to max.
def rfindShip(rfield, rship):
    r_s = rship['schema'];
    for rrow in rfield:
        r_r = '0' + ''.join(map(str, rrow)) + '0';
        ri = 0;
        while ri < 12:
            rpC = r_r.find('0' + r_s + '0', ri);
            if rpC == -1:
                break;
            rship['count'] += 1;
            rrow[rpC : rpC + len(r_s)] = [2] * len(r_s);
            ri = rpC + len(r_s) + 1;

    for rx in range(0, 10):
        rcol = '0';
        for ry in range(0, 10):
            rcol += str(rfield[ry][rx]);
        rcol += '0';
        ri = 0;
        while ri < 12:
            rpC = rcol.find('0' + r_s + '0', ri);
            if rpC == -1:
                break;
            rship['count'] += 1;
            for ry in range(rpC, rpC + len(r_s)):
                rfield[ry][rx] = 2;
            ri = rpC + len(r_s) + 1;

    return rship['max'] == rship['count']

# verify if some is collided
def rverifyCollisions(rfield):
    for rx in range(0, 9):
        for ry in range(0, 9):
            if rfield[rx][ry] > 0 and rfield[rx+1][ry+1] > 0:
                return False;
        for ry in range(1, 10):
            if rfield[rx][ry] > 0 and rfield[rx+1][ry-1] > 0:
                return False;

    return True;

def refvalidate_battlefield(rfield):
    # ships objects
    roBattleship = {'count': 0, 'max': 1, 'schema': '1111'}
    roCruiser = {'count': 0, 'max': 2, 'schema': '111'}
    roDestroyer = {'count': 0, 'max': 3, 'schema': '11'}
    roSubmarine = {'count': 0, 'max': 4, 'schema': '1'}
    # to avoid too long ships, we look at NoNo object
    roNoNo = {'count': 0, 'max': 0, 'schema': '11111'}
    
    return rfindShip(rfield, roNoNo) \
        and rfindShip(rfield, roBattleship) \
        and rfindShip(rfield, roCruiser) \
        and rfindShip(rfield, roDestroyer) \
        and rfindShip(rfield, roSubmarine) \
        and rverifyCollisions(rfield)


# generate random test cases
from random import randint

def buildCase():
    if randint(0, 1): # allValid
        bboats = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        touchEdge = False
        touchCorner = False
    else:
        if randint(0, 1): # correctNumberOfBoats:
            bboats = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        else:
            bboats = [randint(1, 4) for numberOfBoats in range(randint(0, 12))]
        if not randint(0, 1): # correctBoatSizes:
            bboats = [randint(1, 6) for bbsize in bboats]
        touchEdge = bool(randint(0, 1))
        touchCorner = bool(randint(0, 1))
    testFieldDict = {(r, c): 0 for c in range(10) for r in range(10)}
    bblocked = set()
    for bbsize in bboats:
        infiniteLoop = 0
        while True:
            infiniteLoop += 1
            if infiniteLoop == 10:
                break
            bbdirection = randint(0, 1)
            if bbdirection:
                bbdr, bbdc = 0, 1
            else:
                bbdr, bbdc = 1, 0
            bbstartr, bbstartc = randint(0, 9), randint(0, 9)
            bbendr = bbstartr + (bbsize - 1) * bbdr
            bbendc = bbstartc + (bbsize - 1) * bbdc
            if not(0 <= bbendr < 10 and 0 <= bbendc < 10):
                continue
            if any((bbstartr + bbstep * bbdr, bbstartc + bbstep * bbdc) in bblocked for bbstep in range(bbsize)):
                continue
            for bbstep in range(bbsize):
                bbr = bbstartr + bbstep * bbdr
                bbc = bbstartc + bbstep * bbdc
                testFieldDict[bbr, bbc] = 1
                bblocked.add((bbr, bbc))
                if not touchEdge:
                    bblocked.add((bbr - 1, bbc))
                    bblocked.add((bbr + 1, bbc))
                    bblocked.add((bbr, bbc - 1))
                    bblocked.add((bbr, bbc + 1))
            if not touchCorner:
                if bbdirection:
                    bblocked.add((bbstartr - 1, bbstartc - 1))
                    bblocked.add((bbstartr + 1, bbstartc - 1))
                    bblocked.add((bbendr - 1, bbendc + 1))
                    bblocked.add((bbendr + 1, bbendc + 1))
                else:
                    bblocked.add((bbstartr - 1, bbstartc - 1))
                    bblocked.add((bbstartr - 1, bbstartc + 1))
                    bblocked.add((bbendr + 1, bbendc - 1))
                    bblocked.add((bbendr + 1, bbendc + 1))
            break
        if infiniteLoop == 10:
            return None
    testfield = [[testFieldDict[r, c] for c in range(10)] for r in range(10)]
    return testfield


def tests():
    # display and compare actual and expected results
    from copy import deepcopy
    def judge(testfield, expected = None):
        for testrow in testfield:
            print(testrow)
        actual = validate_battlefield(deepcopy(testfield))
        if expected == None:
            expected = refvalidate_battlefield(testfield)
        test.assert_equals(actual, expected)
    
    
    # fixed tests
    #test.it("Fixed Tests")
    test.it("Must return true for valid field")
    testfield = [[1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                 [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
                 [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    judge(testfield, True)
    
    test.it("Must return false if unwanted ships are present")
    testfield = [[1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                 [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
                 [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    judge(testfield, False)
    
    test.it("Must return false if number of ships of some type is incorrect")
    testfield = [[1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                 [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
                 [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    judge(testfield, False)
    
    test.it("Must return false if some of ships is missing")
    testfield = [[0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                 [0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 1, 0, 1, 1, 1, 0, 1, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    judge(testfield, False)
    
    test.it("Must return false if ships are in contact")
    testfield = [[1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                 [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
                 [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                 [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    judge(testfield, False)
    
    test.it("Must return false if some of ships has incorrect shape (non-straight)")
    testfield = [[1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                 [1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [1, 1, 0, 0, 1, 1, 1, 0, 1, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    judge(testfield, False)
             
    test.it("Must return false if the number and length of ships is not ok")
    testfield = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
                 [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
                 [1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    judge(testfield, False)


    # random tests
    test.describe("Random Tests")
    for n in range(1, 101):
        test.it("Random #{}".format(n))
        testfield = buildCase()
        while not testfield:
            testfield = buildCase()
        judge(testfield)
    
tests()
