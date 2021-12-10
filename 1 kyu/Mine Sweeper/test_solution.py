failed = [False]


def makeAssertion(gamemap, mCount, expected, isRnd=False, stuff=None):

    if isRnd: rnd_m,i = stuff
    
    try:
        actual = solve_mine(gamemap,mCount)
        
        if isRnd and expected == "?" and actual == rnd_m[0]:
            print ("<font face='sans-serif' color='#cc0000'><b>Test #"+str(i+1)+": Your solution succeeded where the original didn't.</b></font>\nMight be that yours is smarter... Or you made a wrong (but successful) guess somewhere ?")
            print("Please post a comment in the discourse about that, providing the information below:\n ")
        
        if actual != expected: 
            failed[0] = True
            game.printTrace()
            print(" \nYour answer:\n{}\n\nExpected:\n{}".format(actual, expected))
        test.assert_equals(actual, expected)
    except BoomException as e:
        failed[0] = True
        raise e

@test.describe("Sample Tests")
def doTests():    

    gamemap = """
? ? ? ? ? ?
? ? ? ? ? ?
? ? ? 0 ? ?
? ? ? ? ? ?
? ? ? ? ? ?
0 0 0 ? ? ?
""".strip()
    result = """
1 x 1 1 x 1
2 2 2 1 2 2
2 x 2 0 1 x
2 x 2 1 2 2
1 1 1 1 x 1
0 0 0 1 1 1
""".strip()
    game.read(gamemap, result)
    makeAssertion(gamemap, game.count, result)
    
    gamemap = """
0 ? ?
0 ? ?
""".strip()
    result = """
0 1 x
0 1 1
""".strip()
    game.read(gamemap, result)
    makeAssertion(gamemap, game.count, "?")
    
    gamemap = """
0 ? ?
0 ? ?
""".strip()
    result = """
0 2 x
0 2 x
""".strip()
    game.read(gamemap, result)
    makeAssertion(gamemap, game.count, result)
    
    gamemap = """
? ? ? ? 0 0 0
? ? ? ? 0 ? ?
? ? ? 0 0 ? ?
? ? ? 0 0 ? ?
0 ? ? ? 0 0 0
0 ? ? ? 0 0 0
0 ? ? ? 0 ? ?
0 0 0 0 0 ? ?
0 0 0 0 0 ? ?
""".strip()
    result = """
1 x x 1 0 0 0
2 3 3 1 0 1 1
1 x 1 0 0 1 x
1 1 1 0 0 1 1
0 1 1 1 0 0 0
0 1 x 1 0 0 0
0 1 1 1 0 1 1
0 0 0 0 0 1 x
0 0 0 0 0 1 1
""".strip()
    game.read(gamemap, result)
    makeAssertion(gamemap, game.count, result)
    
    gamemap = """
? ? 0 ? ? ? 0 0 ? ? ? 0 0 0 0 ? ? ? 0
? ? 0 ? ? ? 0 0 ? ? ? 0 0 0 0 ? ? ? ?
? ? 0 ? ? ? ? ? ? ? ? 0 0 0 0 ? ? ? ?
0 ? ? ? ? ? ? ? ? ? ? 0 0 0 0 0 ? ? ?
0 ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 0 0
0 ? ? ? 0 0 0 ? ? ? 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 ? ? ? ? ? ? ? 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 ? ? ? ? 0 0 0 0 0
0 0 ? ? ? 0 ? ? ? 0 ? ? ? ? 0 0 0 0 0
0 0 ? ? ? ? ? ? ? 0 0 0 0 0 0 ? ? ? 0
0 0 ? ? ? ? ? ? ? ? ? 0 0 0 0 ? ? ? 0
0 0 0 0 ? ? ? ? ? ? ? 0 0 0 0 ? ? ? 0
0 0 0 0 0 ? ? ? ? ? ? 0 0 0 0 0 ? ? ?
0 0 ? ? ? ? ? ? 0 0 0 0 0 0 0 0 ? ? ?
0 0 ? ? ? ? ? ? ? 0 0 0 0 0 0 0 ? ? ?
0 0 ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 ? ?
0 0 0 0 0 0 ? ? ? ? 0 0 0 ? ? ? 0 ? ?
0 0 0 ? ? ? ? ? ? ? 0 0 0 ? ? ? ? ? ?
0 0 0 ? ? ? ? ? 0 0 0 ? ? ? ? ? ? ? ?
0 0 0 ? ? ? ? ? 0 0 0 ? ? ? 0 ? ? ? ?
0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
""".strip()
    result = """
1 1 0 1 1 1 0 0 1 1 1 0 0 0 0 1 1 1 0
x 1 0 1 x 1 0 0 2 x 2 0 0 0 0 1 x 2 1
1 1 0 2 3 3 1 1 3 x 2 0 0 0 0 1 2 x 1
0 1 1 2 x x 1 2 x 3 1 0 0 0 0 0 1 1 1
0 1 x 2 2 2 1 3 x 3 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 2 x 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 1 2 2 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 x x 1 0 0 0 0 0
0 0 1 1 1 0 1 1 1 0 1 2 2 1 0 0 0 0 0
0 0 1 x 2 1 3 x 2 0 0 0 0 0 0 1 1 1 0
0 0 1 1 2 x 3 x 3 1 1 0 0 0 0 1 x 1 0
0 0 0 0 1 2 3 2 2 x 1 0 0 0 0 1 1 1 0
0 0 0 0 0 1 x 1 1 1 1 0 0 0 0 0 1 1 1
0 0 1 1 2 2 2 1 0 0 0 0 0 0 0 0 1 x 1
0 0 1 x 2 x 2 1 1 0 0 0 0 0 0 0 1 1 1
0 0 1 1 2 1 3 x 3 1 0 0 0 0 0 0 0 1 1
0 0 0 0 0 0 2 x x 1 0 0 0 1 1 1 0 1 x
0 0 0 1 1 1 1 2 2 1 0 0 0 1 x 1 1 2 2
0 0 0 1 x 3 2 1 0 0 0 1 1 2 1 1 1 x 2
0 0 0 1 2 x x 1 0 0 0 1 x 1 0 1 2 3 x
0 0 0 0 1 2 2 1 1 1 1 1 1 1 0 1 x 3 2
0 0 0 0 1 1 1 1 2 x 1 1 1 1 0 2 3 x 2
0 0 0 0 1 x 1 1 x 2 1 1 x 1 0 1 x 3 x
""".strip()
    game.read(gamemap, result)
    makeAssertion(gamemap, game.count, "?")
    
    gamemap = """
0 0 0 0 0 0 0 0 ? ? ? ? ? 0 ? ? ? 0 ? ? ?
0 0 0 0 0 0 0 0 ? ? ? ? ? 0 ? ? ? ? ? ? ?
0 0 0 0 0 0 0 0 0 0 ? ? ? 0 ? ? ? ? ? ? ?
0 0 0 0 0 ? ? ? 0 0 ? ? ? 0 ? ? ? ? ? ? 0
? ? 0 0 0 ? ? ? 0 ? ? ? ? 0 0 ? ? ? ? ? ?
? ? 0 0 0 ? ? ? 0 ? ? ? 0 0 0 ? ? ? ? ? ?
? ? ? 0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 ? ? ?
? ? ? 0 0 0 0 0 0 0 ? ? ? ? 0 0 ? ? ? 0 0
? ? ? 0 0 0 0 0 0 0 ? ? ? ? 0 0 ? ? ? 0 0
""".strip()
    result = """
0 0 0 0 0 0 0 0 1 x x 2 1 0 1 x 1 0 1 2 x
0 0 0 0 0 0 0 0 1 2 3 x 1 0 2 2 2 1 2 x 2
0 0 0 0 0 0 0 0 0 0 2 2 2 0 1 x 1 1 x 2 1
0 0 0 0 0 1 1 1 0 0 1 x 1 0 1 2 2 2 1 1 0
1 1 0 0 0 1 x 1 0 1 2 2 1 0 0 1 x 1 1 1 1
x 1 0 0 0 1 1 1 0 1 x 1 0 0 0 1 1 1 1 x 1
2 2 1 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 1 1 1
1 x 1 0 0 0 0 0 0 0 1 2 2 1 0 0 1 1 1 0 0
1 1 1 0 0 0 0 0 0 0 1 x x 1 0 0 1 x 1 0 0
""".strip()
    game.read(gamemap, result)
    makeAssertion(gamemap, game.count, "?")
    
    
    
    
@test.it("More basic Tests")
def moreTests():
    gamemap = """
? ? ? ? ? 0 ? ? ? 0 0 0
? ? ? ? ? 0 ? ? ? 0 0 0
? ? ? ? ? 0 0 0 0 0 0 0
0 0 0 0 ? ? ? 0 0 ? ? ?
0 0 0 0 ? ? ? 0 0 ? ? ?
""".strip()
    result = """
1 1 2 1 1 0 1 x 1 0 0 0
1 x 2 x 1 0 1 1 1 0 0 0
1 1 2 1 1 0 0 0 0 0 0 0
0 0 0 0 1 1 1 0 0 1 2 2
0 0 0 0 1 x 1 0 0 1 x x
""".strip()
    game.read(gamemap, result)
    makeAssertion(gamemap, game.count, result)
    
    gamemap = """
0 0 0 0 0 0 0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 0 0 ? ? ? ? ? ? 0
0 0 0 0 0 0 0 0 0 0 0 0 ? ? ? 0 ? ? ? 0 0 0 0 ? ? ? ? ? ? 0
? ? ? 0 0 0 0 ? ? ? 0 0 0 0 ? ? ? ? ? 0 0 0 0 ? ? ? ? ? ? 0
? ? ? ? ? ? 0 ? ? ? ? ? 0 0 ? ? ? ? ? 0 0 0 0 ? ? ? 0 0 0 0
? ? ? ? ? ? 0 ? ? ? ? ? 0 0 ? ? ? ? 0 0 0 0 0 ? ? ? 0 0 ? ?
0 ? ? ? ? ? 0 0 0 ? ? ? 0 ? ? ? ? ? 0 0 0 0 0 ? ? ? 0 0 ? ?
0 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? 0 0 0 ? ? ? ? ? ? ?
0 0 0 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? 0 ? ? ? 0 0 ? ? ? 0
0 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? 0 ? ? ? 0 0 ? ? ? 0
? ? ? ? 0 ? ? ? ? 0 0 0 ? ? ? ? ? ? ? 0 0 ? ? ? 0 0 ? ? ? 0
? ? ? ? 0 ? ? ? ? ? 0 0 ? ? ? ? ? ? ? 0 0 0 ? ? ? 0 0 0 0 0
? ? ? ? ? ? ? ? ? ? 0 0 ? ? ? ? ? ? ? 0 0 0 ? ? ? ? 0 0 0 0
? ? ? ? ? ? ? ? ? ? 0 0 0 0 ? ? ? ? ? 0 0 0 ? ? ? ? 0 0 0 0
? ? ? ? ? ? ? 0 0 ? ? ? 0 0 ? ? ? 0 0 0 0 0 ? ? ? ? 0 0 0 0
? ? ? ? 0 0 0 0 0 ? ? ? 0 0 ? ? ? 0 0 0 0 0 ? ? ? 0 0 0 0 0
""".strip()
    result = """
0 0 0 0 0 0 0 0 0 0 0 0 1 x 1 0 0 0 0 0 0 0 0 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 1 1 1 0 0 0 0 2 x 2 1 x 1 0
1 1 1 0 0 0 0 1 1 1 0 0 0 0 1 1 2 x 1 0 0 0 0 2 x 2 1 1 1 0
1 x 1 1 1 1 0 1 x 2 1 1 0 0 1 x 2 1 1 0 0 0 0 1 1 1 0 0 0 0
1 2 2 3 x 2 0 1 1 2 x 1 0 0 1 2 2 1 0 0 0 0 0 1 1 1 0 0 1 1
0 1 x 3 x 2 0 0 0 1 1 1 0 1 2 3 x 1 0 0 0 0 0 1 x 1 0 0 1 x
0 1 1 3 3 3 2 1 1 1 1 2 1 2 x x 2 2 1 1 0 0 0 1 1 1 1 1 2 1
0 0 0 1 x x 2 x 1 1 x 2 x 2 3 3 3 2 x 1 0 1 1 1 0 0 2 x 2 0
0 1 1 2 2 2 3 2 2 1 1 2 1 1 1 x 2 x 2 1 0 1 x 1 0 0 2 x 2 0
1 2 x 1 0 1 2 x 1 0 0 0 1 1 2 2 3 2 1 0 0 1 1 1 0 0 1 1 1 0
1 x 2 1 0 1 x 3 2 1 0 0 1 x 1 1 x 2 1 0 0 0 1 1 1 0 0 0 0 0
1 1 2 1 2 2 2 2 x 1 0 0 1 1 1 1 2 x 1 0 0 0 1 x 2 1 0 0 0 0
1 1 2 x 2 x 1 1 1 1 0 0 0 0 1 1 2 1 1 0 0 0 1 2 x 1 0 0 0 0
1 x 3 2 2 1 1 0 0 1 1 1 0 0 1 x 1 0 0 0 0 0 1 2 2 1 0 0 0 0
1 2 x 1 0 0 0 0 0 1 x 1 0 0 1 1 1 0 0 0 0 0 1 x 1 0 0 0 0 0
""".strip()
    game.read(gamemap, result)
    makeAssertion(gamemap, game.count, result)
    
    gamemap = """
? ? ? ? 0 0 0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 ? ? ? ? ? ?
? ? ? ? 0 0 0 0 0 0 0 0 ? ? ? 0 0 0 ? ? ? ? ? ? ? ? ?
? ? ? ? 0 0 ? ? ? 0 0 0 0 0 0 0 0 0 ? ? ? ? ? ? 0 0 0
0 ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 0 ? ? ? ? ? ? 0 0 0
0 ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 0 0 ? ? ? ? ? 0 0 0
""".strip()
    result = """
1 2 x 1 0 0 0 0 0 0 0 0 1 x 1 0 0 0 0 0 0 1 1 1 1 x 1
1 x 2 1 0 0 0 0 0 0 0 0 1 1 1 0 0 0 1 1 1 1 x 1 1 1 1
1 2 2 1 0 0 1 1 1 0 0 0 0 0 0 0 0 0 1 x 2 2 1 1 0 0 0
0 1 x 2 1 2 2 x 2 1 0 0 0 0 0 0 0 0 1 3 x 3 1 1 0 0 0
0 1 1 2 x 2 x 3 x 1 0 0 0 0 0 0 0 0 0 2 x 3 x 1 0 0 0
""".strip()
    game.read(gamemap, result)
    makeAssertion(gamemap, game.count, "?")
    
    gamemap = """
0 0 0 ? ? ? ? ? 0 0 0 0 0 0 ? ? ? 0 0 0 ? ? ? ? ? ?
0 0 0 ? ? ? ? ? 0 0 0 ? ? ? ? ? ? 0 0 ? ? ? ? ? ? ?
0 ? ? ? ? ? ? ? ? ? ? ? ? ? 0 0 0 0 0 ? ? ? ? ? ? ?
0 ? ? ? ? ? ? ? ? ? ? ? ? ? 0 0 0 0 0 ? ? ? 0 0 0 0
0 ? ? ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 ? ? ? ? 0 0 0
0 0 ? ? ? ? 0 0 0 ? ? ? 0 0 0 ? ? ? ? ? ? ? ? 0 0 0
0 0 ? ? ? ? 0 0 0 ? ? ? 0 0 0 ? ? ? ? ? ? ? ? 0 0 0
? ? ? ? ? ? 0 0 0 ? ? ? ? ? ? ? ? ? ? ? ? 0 0 0 0 0
? ? ? ? ? ? 0 0 0 0 0 0 ? ? ? ? ? 0 0 ? ? ? 0 0 0 0
? ? ? ? ? ? 0 0 0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 0 0 0
0 ? ? ? 0 0 0 0 0 0 0 0 0 ? ? ? ? ? ? ? ? ? 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 ? ? ? ? ? ? ? ? ? ? ? 0 0
0 0 0 0 0 ? ? ? 0 0 0 0 0 ? ? ? ? ? ? ? 0 ? ? ? ? ?
0 0 0 0 0 ? ? ? 0 ? ? ? 0 0 0 0 ? ? ? ? ? ? ? ? ? ?
0 ? ? ? ? ? ? ? 0 ? ? ? 0 0 0 0 ? ? ? ? ? 0 0 0 ? ?
0 ? ? ? ? ? 0 0 ? ? ? ? 0 0 0 ? ? ? ? ? ? 0 0 0 ? ?
0 ? ? ? ? ? 0 0 ? ? ? 0 0 0 0 ? ? ? ? ? ? 0 0 0 ? ?
""".strip()
    result = """
0 0 0 1 2 3 x 1 0 0 0 0 0 0 1 x 1 0 0 0 1 1 1 1 1 1
0 0 0 1 x x 2 1 0 0 0 1 1 1 1 1 1 0 0 1 2 x 1 1 x 1
0 1 2 3 4 3 3 1 1 1 1 2 x 1 0 0 0 0 0 2 x 3 1 1 1 1
0 1 x x 2 x 2 x 1 1 x 2 1 1 0 0 0 0 0 2 x 2 0 0 0 0
0 1 2 2 2 1 2 1 1 1 1 1 0 0 0 0 0 0 0 1 2 2 1 0 0 0
0 0 1 2 2 1 0 0 0 1 1 1 0 0 0 1 1 1 1 1 2 x 1 0 0 0
0 0 1 x x 1 0 0 0 1 x 1 0 0 0 1 x 1 1 x 2 1 1 0 0 0
1 1 2 3 3 2 0 0 0 1 1 1 1 1 2 2 2 1 1 1 1 0 0 0 0 0
1 x 2 2 x 1 0 0 0 0 0 0 1 x 2 x 1 0 0 1 1 1 0 0 0 0
1 2 x 2 1 1 0 0 0 0 0 0 1 1 2 2 2 1 1 3 x 2 0 0 0 0
0 1 1 1 0 0 0 0 0 0 0 0 0 1 1 2 x 1 1 x x 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 1 x 2 1 2 2 3 2 2 1 1 0 0
0 0 0 0 0 1 1 1 0 0 0 0 0 1 1 1 1 2 x 1 0 1 x 1 1 1
0 0 0 0 0 1 x 1 0 1 1 1 0 0 0 0 1 x 3 2 1 1 1 1 1 x
0 1 1 2 1 2 1 1 0 1 x 1 0 0 0 0 1 1 2 x 1 0 0 0 1 1
0 2 x 3 x 1 0 0 1 2 2 1 0 0 0 1 1 1 2 2 2 0 0 0 1 1
0 2 x 3 1 1 0 0 1 x 1 0 0 0 0 1 x 1 1 x 1 0 0 0 1 x
""".strip()
    game.read(gamemap, result)
    makeAssertion(gamemap, game.count, result)
    
    gamemap = """
0 0 0 ? ? ? ? ? ? 0 0 0 0 0 ? ? ? 0 0 ? ? ? ? ? ? ? ?
? ? 0 ? ? ? ? ? ? 0 0 0 0 0 ? ? ? ? ? ? ? ? ? ? ? ? ?
? ? ? ? 0 0 0 0 0 0 ? ? ? 0 ? ? ? ? ? ? 0 ? ? ? ? ? ?
? ? ? ? 0 0 0 0 0 0 ? ? ? 0 0 0 0 ? ? ? 0 ? ? ? ? ? ?
0 ? ? ? 0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 0 0 ? ? ? ? ? ?
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ? ? ? ? 0
""".strip()
    result = """
0 0 0 1 x 1 1 x 1 0 0 0 0 0 1 1 1 0 0 1 x 3 x 3 1 2 1
1 1 0 1 1 1 1 1 1 0 0 0 0 0 1 x 1 1 1 2 1 3 x 3 x 2 x
x 2 1 1 0 0 0 0 0 0 1 1 1 0 1 1 1 1 x 1 0 2 2 3 1 3 2
1 2 x 1 0 0 0 0 0 0 1 x 1 0 0 0 0 1 1 1 0 1 x 2 1 2 x
0 1 1 1 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 1 2 3 x 2 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 x 2 1 0
""".strip()
    game.read(gamemap, result)
    makeAssertion(gamemap, game.count, result)
    
    
    
    gamemap = """
? ? ? 0 ? ? ? 0 ? ? ? ? ? 0 0 0 ? ? ? 0 0 0 0 0 0 ? ? ? 0 0
? ? ? 0 ? ? ? ? ? ? ? ? ? 0 0 0 ? ? ? ? ? 0 0 0 0 ? ? ? 0 0
0 0 0 ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0 ? ? ? 0 0 0 0 ? ? ? ? 0
? ? ? ? ? ? ? ? ? ? ? ? ? ? ? 0 0 0 ? ? ? 0 0 0 0 0 ? ? ? 0
? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? 0 0 0 ? ? ? 0 0 0 0 ? ? ? 0
? ? ? 0 0 0 ? ? ? 0 0 0 ? ? ? ? 0 0 0 ? ? ? 0 0 0 0 ? ? ? 0
? ? 0 0 0 0 ? ? ? 0 0 0 ? ? ? ? 0 0 0 ? ? ? 0 0 0 ? ? ? 0 0
0 0 0 0 0 0 ? ? ? 0 0 0 ? ? ? 0 ? ? ? 0 0 0 ? ? ? ? ? ? 0 0
0 0 0 0 ? ? ? ? ? 0 0 0 ? ? ? 0 ? ? ? ? ? ? ? ? ? ? ? ? 0 0
0 0 0 0 ? ? ? 0 0 0 0 0 ? ? ? 0 ? ? ? ? ? ? ? ? ? 0 0 0 ? ?
0 0 0 0 ? ? ? 0 0 0 0 ? ? ? 0 0 ? ? ? ? ? ? ? ? 0 ? ? ? ? ?
0 ? ? ? 0 0 0 0 0 0 0 ? ? ? 0 0 ? ? ? ? ? ? ? ? 0 ? ? ? ? ?
0 ? ? ? ? ? ? ? 0 0 0 ? ? ? 0 0 0 ? ? ? 0 ? ? ? ? ? ? ? 0 0
0 ? ? ? ? ? ? ? ? ? 0 ? ? ? ? 0 0 ? ? ? ? 0 ? ? ? 0 0 0 0 0
? ? 0 ? ? ? ? ? ? ? 0 ? ? ? ? 0 0 0 ? ? ? 0 ? ? ? ? 0 0 0 0
? ? 0 0 0 0 ? ? ? ? 0 ? ? ? ? 0 0 0 ? ? ? 0 0 ? ? ? 0 0 0 0
? ? 0 0 0 0 ? ? ? 0 0 0 0 ? ? ? 0 0 0 0 0 0 0 ? ? ? ? 0 0 0
0 0 0 0 0 0 ? ? ? 0 0 0 0 ? ? ? 0 0 0 ? ? ? 0 ? ? ? ? 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 ? ? ? 0 0 0 ? ? ? 0 ? ? ? ? 0 0 0
? ? ? ? 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ? ? ? 0 ? ? ? 0 ? ? ?
? ? ? ? ? ? ? 0 ? ? ? 0 0 ? ? ? ? ? 0 ? ? ? ? ? ? ? 0 ? ? ?
? ? ? ? ? ? ? 0 ? ? ? ? 0 ? ? ? ? ? 0 0 0 0 ? ? ? 0 0 ? ? ?
0 0 ? ? ? ? ? 0 ? ? ? ? ? ? ? ? ? ? ? 0 0 0 ? ? ? 0 0 0 0 0
0 0 ? ? ? ? ? 0 0 ? ? ? ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 0 0
0 0 0 0 ? ? ? 0 0 0 0 ? ? ? ? ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 ? ? ? ? ? ? ? 0 0 ? ? ? ? ? ? ? ? 0 0 0 0
0 0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 0 ? ? ? ? ? ? ? ? ? ? ? ? ?
0 0 0 0 0 ? ? ? ? ? ? ? 0 0 0 0 0 ? ? ? ? ? ? ? ? ? ? ? ? ?
0 0 0 0 0 ? ? ? ? ? ? 0 0 0 0 0 0 ? ? ? ? ? ? ? ? ? ? ? ? ?
""".strip()
    result = """
1 x 1 0 1 1 1 0 1 x 2 x 1 0 0 0 1 x 1 0 0 0 0 0 0 1 1 1 0 0
1 1 1 0 1 x 2 2 3 2 2 1 1 0 0 0 1 1 2 1 1 0 0 0 0 1 x 1 0 0
0 0 0 1 2 2 2 x x 2 1 1 0 0 0 0 0 0 1 x 1 0 0 0 0 1 2 2 1 0
1 1 1 1 x 1 1 2 2 2 x 1 1 1 1 0 0 0 1 1 1 0 0 0 0 0 2 x 2 0
2 x 1 1 1 1 1 1 1 1 1 1 1 x 2 1 0 0 0 1 1 1 0 0 0 0 2 x 2 0
x 2 1 0 0 0 1 x 1 0 0 0 2 3 x 1 0 0 0 1 x 1 0 0 0 0 1 1 1 0
1 1 0 0 0 0 2 2 2 0 0 0 1 x 2 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0
0 0 0 0 0 0 1 x 1 0 0 0 2 2 2 0 1 1 1 0 0 0 1 1 1 1 x 1 0 0
0 0 0 0 1 1 2 1 1 0 0 0 1 x 1 0 1 x 1 1 1 2 2 x 1 1 1 1 0 0
0 0 0 0 1 x 1 0 0 0 0 0 1 1 1 0 2 2 2 2 x 3 x 2 1 0 0 0 1 1
0 0 0 0 1 1 1 0 0 0 0 1 1 1 0 0 1 x 1 2 x 4 2 2 0 1 1 1 1 x
0 1 1 1 0 0 0 0 0 0 0 1 x 1 0 0 1 2 2 2 1 2 x 1 0 1 x 1 1 1
0 1 x 2 1 2 1 1 0 0 0 1 1 1 0 0 0 1 x 1 0 1 2 2 1 1 1 1 0 0
0 1 1 2 x 2 x 3 2 1 0 1 2 2 1 0 0 1 2 2 1 0 1 x 1 0 0 0 0 0
1 1 0 1 1 2 2 x x 1 0 1 x x 1 0 0 0 1 x 1 0 1 2 2 1 0 0 0 0
x 1 0 0 0 0 2 3 3 1 0 1 2 2 1 0 0 0 1 1 1 0 0 2 x 2 0 0 0 0
1 1 0 0 0 0 1 x 1 0 0 0 0 1 1 1 0 0 0 0 0 0 0 2 x 3 1 0 0 0
0 0 0 0 0 0 1 1 1 0 0 0 0 1 x 1 0 0 0 1 1 1 0 1 2 x 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0 2 x 2 0 1 2 2 1 0 0 0
1 2 2 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 x 2 0 1 x 1 0 1 1 1
1 x x 1 1 1 1 0 1 1 1 0 0 1 1 2 1 1 0 1 1 1 1 2 2 1 0 1 x 1
1 2 3 2 2 x 1 0 1 x 2 1 0 1 x 3 x 2 0 0 0 0 1 x 1 0 0 1 1 1
0 0 1 x 3 2 2 0 1 2 x 1 1 2 2 3 x 3 1 0 0 0 1 1 1 0 0 0 0 0
0 0 1 1 2 x 1 0 0 1 1 2 2 x 2 2 2 x 2 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 0 0 0 0 1 x 4 x 1 1 1 2 x 1 1 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 1 2 2 x 2 1 0 0 1 1 1 1 x 2 1 1 0 0 0 0
0 0 0 0 0 1 1 2 1 2 x 1 1 1 1 0 0 1 2 2 1 1 1 2 x 2 1 1 1 1
0 0 0 0 0 1 x 4 x 4 2 1 0 0 0 0 0 2 x x 2 2 2 2 3 x 2 1 x 1
0 0 0 0 0 1 2 x x x 1 0 0 0 0 0 0 2 x 3 2 x x 1 2 x 2 1 1 1
""".strip()
    game.read(gamemap, result)
    makeAssertion(gamemap, game.count, result)
    
    gamemap = """
0 0 0 0 0 0 0 ? ? ?
? ? ? ? ? ? 0 ? ? ?
? ? ? ? ? ? 0 ? ? ?
? ? ? ? ? ? 0 ? ? ?
0 0 ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? ?
0 0 ? ? ? ? ? ? ? ?
0 0 0 0 ? ? ? ? ? ?
0 0 0 0 ? ? ? ? ? ?
0 0 0 ? ? ? ? 0 0 0
0 0 0 ? ? ? ? 0 0 0
0 0 0 ? ? ? ? 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
? ? 0 ? ? ? 0 0 0 0
? ? 0 ? ? ? 0 0 0 0
? ? ? ? ? ? ? ? ? 0
? ? ? ? ? ? ? ? ? ?
? ? ? ? ? ? ? ? ? ?
0 0 ? ? ? 0 0 ? ? ?
0 0 ? ? ? ? ? ? ? ?
0 0 ? ? ? ? ? ? ? ?
0 0 0 0 0 ? ? ? ? ?
""".strip()
    result = """
0 0 0 0 0 0 0 1 1 1
1 1 1 1 1 1 0 2 x 2
1 x 2 2 x 1 0 2 x 2
1 1 2 x 2 1 0 1 1 1
0 0 2 2 2 1 1 1 0 0
0 0 1 x 1 1 x 2 1 1
0 0 1 1 2 2 2 3 x 2
0 0 0 0 1 x 1 2 x 2
0 0 0 0 1 1 1 1 1 1
0 0 0 1 2 2 1 0 0 0
0 0 0 1 x x 1 0 0 0
0 0 0 1 2 2 1 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
1 1 0 1 1 1 0 0 0 0
x 1 0 1 x 1 0 0 0 0
2 3 1 3 2 2 1 1 1 0
x 2 x 2 x 1 1 x 2 1
1 2 1 2 1 1 1 2 x 1
0 0 1 1 1 0 0 1 1 1
0 0 1 x 1 1 1 2 2 2
0 0 1 1 1 1 x 2 x x
0 0 0 0 0 1 1 2 2 2
""".strip()
    game.read(gamemap, result)
    makeAssertion(gamemap, game.count, result)
    
    gamemap = """
? ? 0 0 0 0 0 0 0 0 0 0 0 0 ? ? ? 0
? ? 0 0 ? ? ? 0 0 0 ? ? ? 0 ? ? ? 0
? ? 0 0 ? ? ? 0 0 0 ? ? ? 0 ? ? ? 0
0 ? ? ? ? ? ? 0 0 0 ? ? ? 0 0 0 0 0
0 ? ? ? 0 0 0 0 0 ? ? ? ? 0 0 0 0 0
0 ? ? ? 0 0 0 0 0 ? ? ? ? ? ? ? ? ?
0 0 0 ? ? ? 0 0 0 ? ? ? ? ? ? ? ? ?
0 ? ? ? ? ? ? 0 ? ? ? 0 ? ? ? ? ? ?
0 ? ? ? ? ? ? 0 ? ? ? ? ? 0 ? ? ? ?
0 ? ? ? ? ? ? ? ? ? ? ? ? 0 ? ? ? 0
0 ? ? ? 0 ? ? ? 0 0 ? ? ? 0 0 0 0 0
0 ? ? ? 0 ? ? ? 0 0 ? ? ? 0 0 0 0 0
0 ? ? ? ? ? ? 0 0 0 ? ? ? 0 0 0 0 0
? ? ? ? ? ? ? 0 0 0 ? ? ? ? ? 0 0 0
? ? ? ? ? ? ? 0 ? ? ? ? ? ? ? 0 0 0
? ? ? ? ? ? 0 0 ? ? ? ? ? ? ? 0 ? ?
0 ? ? ? 0 0 0 0 ? ? ? ? ? ? 0 0 ? ?
0 ? ? ? 0 0 0 0 0 ? ? ? 0 0 0 0 ? ?
? ? ? ? ? 0 0 0 0 ? ? ? 0 0 0 0 0 0
? ? ? ? ? ? ? 0 0 ? ? ? 0 0 0 0 0 0
? ? ? ? ? ? ? 0 0 0 ? ? ? 0 ? ? ? 0
? ? ? ? ? ? ? 0 0 0 ? ? ? 0 ? ? ? 0
""".strip()
    result = """
1 1 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0
x 1 0 0 1 1 1 0 0 0 1 1 1 0 1 x 1 0
1 1 0 0 1 x 1 0 0 0 2 x 2 0 1 1 1 0
0 1 1 1 1 1 1 0 0 0 2 x 2 0 0 0 0 0
0 1 x 1 0 0 0 0 0 1 2 2 1 0 0 0 0 0
0 1 1 1 0 0 0 0 0 1 x 1 1 1 1 1 2 2
0 0 0 1 1 1 0 0 0 1 1 1 1 x 1 1 x x
0 1 1 2 x 2 1 0 1 1 1 0 1 1 2 2 4 x
0 1 x 2 2 x 1 0 1 x 2 1 1 0 1 x 2 1
0 2 2 2 1 2 2 1 1 1 3 x 2 0 1 1 1 0
0 1 x 1 0 1 x 1 0 0 2 x 2 0 0 0 0 0
0 1 1 1 0 1 1 1 0 0 2 2 2 0 0 0 0 0
0 1 1 1 1 1 1 0 0 0 1 x 1 0 0 0 0 0
1 2 x 2 2 x 1 0 0 0 1 2 3 2 1 0 0 0
x 2 1 2 x 2 1 0 1 1 1 2 x x 1 0 0 0
1 2 1 2 1 1 0 0 1 x 1 2 x 3 1 0 1 1
0 1 x 1 0 0 0 0 1 1 1 1 1 1 0 0 1 x
0 1 1 1 0 0 0 0 0 1 1 1 0 0 0 0 1 1
1 1 1 1 1 0 0 0 0 1 x 1 0 0 0 0 0 0
x 3 2 x 2 1 1 0 0 1 1 1 0 0 0 0 0 0
x 3 x 3 3 x 1 0 0 0 1 1 1 0 1 1 1 0
1 2 1 2 x 2 1 0 0 0 1 x 1 0 1 x 1 0
""".strip()
    game.read(gamemap, result)
    makeAssertion(gamemap, game.count, result)
    
    gamemap = """
0 0 0 0 ? ? ? ? ? ?
0 0 0 ? ? ? ? ? ? ?
0 ? ? ? ? ? ? ? ? ?
? ? ? ? ? ? ? ? ? 0
? ? ? ? 0 0 0 0 0 0
? ? ? 0 0 0 0 0 0 0
""".strip()
    result = """
0 0 0 0 1 1 1 1 1 1
0 0 0 1 2 x 2 2 x 1
0 1 1 2 x 2 2 x 2 1
1 2 x 2 1 1 1 1 1 0
1 x 2 1 0 0 0 0 0 0
1 1 1 0 0 0 0 0 0 0
""".strip()
    game.read(gamemap, result)
    makeAssertion(gamemap, game.count, result)
    
    gamemap = """
? ? ? 0 0 ? ? ? ? ? ? 0 0 ? ? ? ?
? ? ? 0 0 ? ? ? ? ? ? 0 0 ? ? ? ?
0 0 0 0 0 ? ? ? ? 0 0 0 0 0 ? ? ?
0 0 0 0 0 0 ? ? ? 0 0 0 0 0 ? ? ?
0 0 0 0 0 0 0 0 0 0 0 0 0 0 ? ? ?
? ? ? 0 0 0 0 0 0 0 0 0 0 ? ? ? ?
? ? ? 0 0 0 0 0 0 0 0 0 0 ? ? ? ?
""".strip()
    result = """
1 x 1 0 0 2 x 2 1 x 1 0 0 1 x x 1
1 1 1 0 0 2 x 3 2 1 1 0 0 1 3 4 3
0 0 0 0 0 1 2 x 1 0 0 0 0 0 1 x x
0 0 0 0 0 0 1 1 1 0 0 0 0 0 1 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1
1 1 1 0 0 0 0 0 0 0 0 0 0 1 2 x 1
1 x 1 0 0 0 0 0 0 0 0 0 0 1 x 2 1
""".strip()
    game.read(gamemap, result)
    makeAssertion(gamemap, game.count, result)
    
    gamemap = """
0 ? ? ? ? ? 0 0 0 ? ? ? ? ? ? ? ? 0 0 0
0 ? ? ? ? ? 0 0 0 ? ? ? ? ? ? ? ? 0 0 0
0 ? ? ? ? ? 0 0 0 ? ? ? ? ? ? ? 0 0 ? ?
0 0 0 ? ? ? 0 0 0 0 ? ? ? ? ? ? 0 0 ? ?
0 0 0 ? ? ? 0 0 0 0 0 0 0 0 0 0 0 ? ? ?
0 ? ? ? ? ? 0 0 0 0 0 0 0 0 0 0 0 ? ? ?
0 ? ? ? 0 ? ? ? 0 0 0 0 0 ? ? ? 0 ? ? ?
0 ? ? ? 0 ? ? ? ? ? ? 0 0 ? ? ? ? ? 0 0
0 ? ? ? 0 ? ? ? ? ? ? 0 0 ? ? ? ? ? 0 0
0 ? ? ? 0 0 0 ? ? ? ? 0 0 0 0 ? ? ? 0 0
0 ? ? ? 0 0 0 0 0 0 0 0 0 0 0 ? ? ? ? 0
0 ? ? ? 0 0 0 0 0 ? ? ? 0 0 0 ? ? ? ? 0
0 ? ? ? 0 0 0 0 0 ? ? ? ? ? 0 ? ? ? ? 0
? ? ? ? 0 0 0 0 0 ? ? ? ? ? 0 ? ? ? ? 0
? ? 0 0 0 0 0 0 0 0 0 ? ? ? 0 ? ? ? ? ?
? ? ? ? 0 0 0 0 0 0 0 0 0 0 0 ? ? ? ? ?
? ? ? ? 0 0 ? ? ? ? ? 0 ? ? ? 0 0 ? ? ?
? ? ? ? ? ? ? ? ? ? ? 0 ? ? ? 0 0 0 0 0
? ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ? 0 0 0 0
0 ? ? ? ? ? ? ? ? 0 0 0 ? ? ? ? 0 0 0 0
0 0 0 0 ? ? ? ? ? 0 0 0 ? ? ? ? 0 0 0 0
0 0 0 0 ? ? ? 0 0 0 0 0 ? ? ? ? 0 0 0 0
0 0 0 0 0 0 0 ? ? ? ? 0 ? ? ? ? 0 0 0 0
? ? ? ? ? 0 0 ? ? ? ? ? ? ? ? ? ? ? ? 0
? ? ? ? ? 0 0 ? ? ? ? ? ? 0 ? ? ? ? ? ?
? ? ? ? ? 0 0 0 0 0 ? ? ? ? ? ? ? ? ? ?
? ? ? ? ? ? 0 0 0 0 0 ? ? ? 0 0 0 ? ? ?
? ? ? ? ? ? 0 0 0 0 0 ? ? ? 0 0 0 ? ? ?
? ? ? ? ? ? 0 0 0 0 0 0 0 0 0 0 0 ? ? ?
""".strip()
    result = """
0 1 1 2 1 1 0 0 0 1 1 2 2 2 2 x 1 0 0 0
0 1 x 2 x 1 0 0 0 1 x 3 x x 3 2 1 0 0 0
0 1 1 2 1 1 0 0 0 1 2 x 3 3 x 1 0 0 1 1
0 0 0 1 1 1 0 0 0 0 1 1 1 1 1 1 0 0 1 x
0 0 0 1 x 1 0 0 0 0 0 0 0 0 0 0 0 1 2 2
0 1 1 2 1 1 0 0 0 0 0 0 0 0 0 0 0 1 x 1
0 1 x 1 0 1 1 1 0 0 0 0 0 1 1 1 0 1 1 1
0 1 1 1 0 1 x 2 2 2 1 0 0 1 x 2 1 1 0 0
0 1 1 1 0 1 1 2 x x 1 0 0 1 1 2 x 1 0 0
0 1 x 1 0 0 0 1 2 2 1 0 0 0 0 2 2 2 0 0
0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 1 x 2 1 0
0 1 1 1 0 0 0 0 0 1 1 1 0 0 0 1 2 x 1 0
0 1 x 1 0 0 0 0 0 1 x 2 1 1 0 1 3 3 2 0
1 2 1 1 0 0 0 0 0 1 1 2 x 1 0 2 x x 1 0
x 1 0 0 0 0 0 0 0 0 0 1 1 1 0 2 x 4 3 2
1 2 1 1 0 0 0 0 0 0 0 0 0 0 0 1 1 2 x x
1 2 x 1 0 0 1 2 3 2 1 0 1 1 1 0 0 1 2 2
1 x 3 3 1 1 1 x x x 1 0 2 x 2 0 0 0 0 0
1 2 x 2 x 1 2 3 4 2 1 0 2 x 3 1 0 0 0 0
0 1 1 2 2 2 2 x 1 0 0 0 1 2 x 1 0 0 0 0
0 0 0 0 1 x 2 1 1 0 0 0 1 2 2 1 0 0 0 0
0 0 0 0 1 1 1 0 0 0 0 0 1 x 2 1 0 0 0 0
0 0 0 0 0 0 0 1 2 2 1 0 1 2 x 1 0 0 0 0
1 1 1 1 1 0 0 1 x x 2 1 1 1 2 2 2 1 1 0
x 2 3 x 2 0 0 1 2 2 2 x 1 0 1 x 2 x 2 1
2 x 3 x 2 0 0 0 0 0 1 2 2 1 1 1 2 1 2 x
2 3 3 3 2 1 0 0 0 0 0 1 x 1 0 0 0 1 2 2
x 2 x 2 x 1 0 0 0 0 0 1 1 1 0 0 0 1 x 1
1 2 1 2 1 1 0 0 0 0 0 0 0 0 0 0 0 1 1 1
""".strip()
    game.read(gamemap, result)
    makeAssertion(gamemap, game.count, result)
    
    
    
    gamemap = """
0 0 0 0 0 0 0 0 0 0 0 0 ? ? ? 0 ? ? ? ? ? 0 0 ? ? ?
0 0 ? ? ? ? ? ? ? 0 0 0 ? ? ? 0 ? ? ? ? ? 0 0 ? ? ?
0 0 ? ? ? ? ? ? ? 0 0 0 ? ? ? ? 0 ? ? ? ? ? 0 ? ? ?
0 0 ? ? ? ? ? ? ? 0 0 0 0 ? ? ? 0 ? ? ? ? ? 0 0 0 0
""".strip()
    result = """
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 1 x 2 1 1 0 0 1 1 1
0 0 1 2 2 1 1 1 1 0 0 0 1 x 1 0 1 2 3 x 1 0 0 1 x 1
0 0 1 x x 1 1 x 1 0 0 0 1 2 2 1 0 1 x 3 2 1 0 1 1 1
0 0 1 2 2 1 1 1 1 0 0 0 0 1 x 1 0 1 1 2 x 1 0 0 0 0
""".strip()
    game.read(gamemap, result)
    makeAssertion(gamemap, game.count, result)
    
    
    
    gamemap = "?"
    result = "0"
    game.read(gamemap, result)
    makeAssertion(gamemap, game.count, result)
    
    gamemap = "?"
    result = "x"
    game.read(gamemap, result)
    makeAssertion(gamemap, game.count, result)
    
    gamemap = "? ? ?\n? ? ?\n? ? ?"
    result = "x x x\nx 8 x\nx x x"
    game.read(gamemap, result)
    makeAssertion(gamemap, game.count, "?")
    
    gamemap = """
0 0 0 0
0 0 0 0
? ? 0 0
? ? ? ?
? ? ? ?
? ? ? ?
? ? 0 0
0 0 0 0
0 0 0 0
0 0 0 0""".strip()
    result = """
0 0 0 0
0 0 0 0
1 1 0 0
x 2 1 1
x 3 1 x
x 2 1 1
1 1 0 0
0 0 0 0
0 0 0 0
0 0 0 0""".strip()
    game.read(gamemap, result)
    makeAssertion(gamemap, game.count, result)
    
    gamemap = """
0 0 0 0 0 0 0 0 0 0 0
0 0 0 ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? 0 0 0
0 0 0 0 0 0 0 0 0 0 0
""".strip()
    result = """
0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 2 3 3 2 1 0 0
0 0 1 3 x x x x 1 0 0
0 0 2 x x x x 5 2 0 0
0 0 3 x x x x x 2 0 0
0 0 3 x x x x x 2 0 0
0 0 2 x x x x 3 1 0 0
0 0 1 2 3 3 2 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0
""".strip()
    game.read(gamemap, result)
    makeAssertion(gamemap, game.count, result)
    
    gamemap = """
0 0 0 0 0 0 0 0 0 0 0
0 0 0 ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? 0 0 0
0 0 0 0 0 0 0 0 0 0 0
""".strip()
    result = """
0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 2 3 3 2 1 0 0
0 0 1 3 x x x x 1 0 0
0 0 2 x x 6 x 5 2 0 0
0 0 3 x 4 4 x x 2 0 0
0 0 3 x 5 5 x x 2 0 0
0 0 2 x x x x 3 1 0 0
0 0 1 2 3 3 2 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0
""".strip()
    game.read(gamemap, result)
    makeAssertion(gamemap, game.count, result)
    
    
    
    
    

import re
from random import randint
from itertools import combinations
from functools import reduce


TEST_FAILS_ALEA = False
IS_DUMB         = TEST_FAILS_ALEA

if TEST_FAILS_ALEA: print("WARNING!!!! : Random tests are desactivated !!!")


class InternalSweeper(object):

    IS_DEBUG = False
    around   = [ (dx,dy) for dx in range(-1,2) for dy in range(-1,2) if (dx,dy) != (0,0) ]
    
    def __init__(self, mapStr, nMines):
        lines = mapStr.split('\n')
        mapDct, unknowns, posToWorkOn = {}, set(), set()
        for x,line in enumerate(lines):
            for y,c in enumerate(line.split(' ')):
                mapDct[(x,y)] = c
                if c == '?': unknowns.add((x,y))
                else:        posToWorkOn.add((x,y))
    
        self.map         = mapDct
        self.unknowns    = unknowns
        self.posToWorkOn = posToWorkOn
        self.flagged     = set()
        self.nMines      = nMines
        self.lX          = len(lines)
        self.lY          = len(lines[0].split(' '))
        
    
    
    def __str__(self):                return '\n'.join(' '.join( self.map[(x,y)] for y in range(self.lY)) for x in range(self.lX) )
    
    def getValAt(self,pos):           return int(self.map[pos])
    
    def getneighbors(self, pos):      return { (pos[0]+dx,pos[1]+dy) for dx,dy in self.around }
    
    def printDebug(self):             print(" \n------------\n{}\nRemaining mines: {}".format(self, self.nMines-len(self.flagged))) if self.IS_DEBUG else None
    
    def lookaroundThisPos(self, pos):
        neighbors = self.getneighbors(pos)
        return {'?': neighbors & self.unknowns,
                'x': neighbors & self.flagged}
        
    
    """ MAIN FUNCTION """
    def solve(self):
        
        self.printDebug()
        while True:
            while True:
                archivePosToWorkOn = self.posToWorkOn.copy()            # Archive to check against modifications
                
                self.openAndFlag_OnTheFly();       self.printDebug()    # Open and flag in the map while simple matches can be found
                self.complexSearch_OpenAndFlag();  self.printDebug()    # Use more complex algorithm to find mines or unknown positions that are surely openable
                
                if archivePosToWorkOn == self.posToWorkOn: break        # Repeat these two "simple" steps until its not possible to go further in the resolution
            
            self.complexSearch_CombineApproach()                        # Use witted combinatory approach to go further (if possible)
            
            if archivePosToWorkOn == self.posToWorkOn:
                break; self.printDebug()                                # Repeat these to "simple" steps until its not possible to go further in the resolution
        
        
        if len(self.flagged) == self.nMines:                            # If no more mines remaining but some unknown cases still there
            self.openThosePos(self.unknowns.copy())
            
        elif len(self.flagged) + len(self.unknowns) == self.nMines:     # If all the remaining "?" are mines, flag them
            self.flagThosePos(self.unknowns.copy())
        
        self.printDebug()
        
        return '?' if self.unknowns else str(self)
        
    
    def openAndFlag_OnTheFly(self):
        while True:
            openables, workDonePos = set(), set()
            for pos in self.posToWorkOn:                                    # Run through all the positions that might neighbors to open
                openables, workDonePos = [ baseSet|newPart for baseSet,newPart in zip((openables, workDonePos), self.openablePosaround_FlagOnTheFly(pos)) ]
            
            self.openThosePos(openables)                                    # After the exit of the loop, modification of self.posToWorkOn is possible, so:
            self.posToWorkOn -= workDonePos                                 # remove the pos with full number of mines from the working set (to fasten the executions)
            if not openables and not workDonePos: break     
    
    
    def openablePosaround_FlagOnTheFly(self, pos):
        around = self.lookaroundThisPos(pos)
        
        if self.getValAt(pos) == len(around['?']) + len(around['x']):       # If all the unknomn cases can be flagged (or if they are already!)...
            self.flagThosePos(around['?'])                                  # flag them (if not already done)
            return (set(), {pos})                                           # return the current position to remove it from self.posToWorkOn ("We're done with you..." / This behaviour will identify the "done" positions generated by the "witted approach")
            
        return (around['?'], {pos}) if self.getValAt(pos) == len(around['x']) else (set(), set())  
        
        
    def openThosePos(self, posToOpen):
        for pos in posToOpen:
            self.map[pos] = str(open(*pos))                                 # Open squares and update the map
            if self.map[pos] != '0': self.posToWorkOn.add(pos)              # Update slef.posToWorkOn if needed
        self.unknowns -= posToOpen                                          # Remove opened squares from the unknown positions
    
    
    def flagThosePos(self, posToFlag):
        for pos in posToFlag: self.map[pos] = 'x'                           # Flag mines
        self.unknowns -= posToFlag                                          # Remove flagged squares from the unknown positions
        self.flagged  |= posToFlag                                          # update the set of flagged positions
    
    
    def complexSearch_OpenAndFlag(self):
        markables, openables = set(), set()
        for pos in self.posToWorkOn:
            newMark, newOpen = self.intelligencia_OpenAndFlag(pos)
            markables |= newMark
            openables |= newOpen
            
        self.flagThosePos(markables)
        self.openThosePos(openables)
        
                
    def intelligencia_OpenAndFlag(self, pos):
        around       = self.lookaroundThisPos(pos)                          # Cases around the current position
        rMines        = [self.getValAt(pos)-len(around['x']), 0]            # Prepare an array with the number of remaining mines to find for the current position and the neighbor that will be worked on later
        neighToWorkOn = self.getneighbors(pos) & self.posToWorkOn           # Search for neighbors (only usefull ones, meaning: self.getValAt(posneighbor) is a number and this neighbor still miss some mines)
            
        markables, openables = set(), set()                                 # markables: position that will be flagged / openables: positions that will be open... of course... / fullUnion: stroe all the squares
        knownParts = []                                                     # knownParts: list of the intersections of the '?' cases of all the neighbors of the current pos and the current neighbor
        
        for pos2 in neighToWorkOn:
            around2  = self.lookaroundThisPos(pos2)                                         # Cases around the neighbor that is worked on right now
            rMines[1] = self.getValAt(pos2) - len(around2['x'])                             # Update the number of mines still to find for the current neighbor
            onlys     = [ around['?'] - around2['?'], around2['?'] - around['?'] ]          # Define the '?' that are owned only by the current "pos", and only by the current neighbor ("pos2")
            mInter    = max( n-len(only) for n,only in zip(rMines, onlys) )                 # Define the minimum (yes "minimum", even if "max" is used!) number of mines that have to be in the '?' that are commun to "pos" and it's current neighbor pos2"
            
            if mInter <= 0 or 1 not in rMines: continue                                     # If these conditions are met, there is nothing "extrapolable" at the current position, so continue the iteration
            
            currentIntersect = around['?'] & around2['?']
            if currentIntersect: knownParts.append(currentIntersect)                        # Store (if it exists) the current intersection of '?' cases for further checks

            for i in range(2):                                                              # Work on the two current LOCATIONS (pos, pos2)
                if len(onlys[i]) == rMines[i]-mInter:  markables |= onlys[i]                # The number of '?' cases that are only around the treated LOCATION matches the number mines of this LOCATION that are out of the interesction "pos & pos2". So, those cases will be flagged
                elif mInter == rMines[i]:              openables |= onlys[i]                # If the number of mines surely present in the intersection "pos & pos2" matches the number of mines still to found arorund the treated LOCATION, all the cases out of the intersection for the current LOCATION can be opened
            
        # Final check on the different intersections parts:
        fullIntersection = {posInter for posSet in knownParts for posInter in posSet}       # Union of all the intersections for the current position and its differente neighbors
        if len(knownParts) == rMines[0] and sum( len(s) for s in knownParts) == len(fullIntersection): 
            openables |= around['?'] - fullIntersection                                     # If some '?' cases are still unchecked while we can be sure that all the remaining mines are elsewhere (even without knowing their exact location), the leftovers can be opened
        
        return markables, openables
        
        
        
    def complexSearch_CombineApproach(self):
        rMines = self.nMines - len(self.flagged)                                            # number of remaining mines to find
        matchPos = []
        
        if rMines != 0:
            
            borderUnknowns = { pos2 for pos in self.posToWorkOn for pos2 in self.lookaroundThisPos(pos)['?'] }      # '?' that are joined to the current posToWorkOn...
            borderUnknowns |= { pos2 for pos in borderUnknowns for pos2 in self.lookaroundThisPos(pos)['?'] }       # ...then add the "next layer" of "?", ot be able to make more guesses on the remaining farther squares
            
            for n in range(rMines if not (self.unknowns-borderUnknowns) else 1, min(rMines, len(borderUnknowns)-1)+1):
                for posMines in combinations(borderUnknowns, n):
                    setPosMines = set(posMines)
                    for pos in self.posToWorkOn:
                        around = self.lookaroundThisPos(pos)
                        if self.getValAt(pos) != len(around['x']) + len(around ['?'] & setPosMines): break
                    else:
                        matchPos.append(setPosMines)                                                                # if the for loop execute until its end, the current position is valid. Archive it.
            
            untouched = borderUnknowns - {flagPos for s in matchPos for flagPos in s}                               # search for '?' that are never marked in any of the valid combinations
        
            if len(matchPos) == 1:  self.flagThosePos(matchPos[0])                                                  # Flag the found mines if only 1 match
            self.openThosePos(untouched)                                                                            # open the untouched '?' (free of mines!!)
            

def _my_solve_(mapStr, n):  return InternalSweeper(mapStr, n).solve()


    
    
    
@test.describe("Efficiency tests")
def effic():
    
    gamemap = """
0 1 ? ? ? ? ?
0 2 ? ? ? ? ?
0 2 ? ? ? ? ?
0 2 ? ? ? ? ?
0 1 ? ? ? ? ?
""".strip()
    result = """
0 1 1 1 1 x 1
0 2 x 2 1 1 1
0 2 x 2 1 1 1
0 2 2 2 1 x 1
0 1 x 1 1 1 1
""".strip()
    game.read(gamemap, result)
    
    import time
    
    funcs, t = [_my_solve_, solve_mine], []
    ratio = 10
    for i,f in enumerate(funcs):
        start = time.perf_counter()
        f(gamemap, game.count)
        t.append(time.perf_counter()-start)
    
    @test.it("Precheck...")
    def precheck():
        succeedStr = "You're fast enough to have a chance to pass the next one without timing out."
        if t[1] >= t[0]*ratio:
            print("This is the next test, where your function has to be clever so it won't time out:\n{}41 mines.".format("""
0 1 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ?
0 2 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ?
0 2 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ?
0 2 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ?
0 1 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ?
"""))
        test.assert_equals(["DAMN!", succeedStr][t[1] < t[0]*ratio], succeedStr, "Your implementation is waaaaay too slow on this one. This is because you didn't think about the right approach... ;) Your function took {}s to execute, but it should run in less than {}s to be able to handle the next test without timing out (see upper the next grid)".format(round(t[1], 5), round(t[0]*ratio, 5)))
    
    
    gamemap = """
0 1 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ?
0 2 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ?
0 2 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ?
0 2 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ?
0 1 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ?
""".strip()
    result = """
0 1 1 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1
0 2 x 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 2 x 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 2 2 2 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1 1 x 1
0 1 x 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
""".strip()
    game.read(gamemap, result)
    
    @test.it("Big test: if you fail on this one, you still have some optimizations to do...")
    def bigTest():
        makeAssertion(gamemap, game.count, "?")
    
    
    
    


def rand_map():
    width = randint(4, 30)
    height = randint(4, 30)
    mines = (width*height)//10
    map = [[0 for j in range(width)] for i in range(height)]
    for m in range(mines):
        r = randint(0, height-1)
        c = randint(0, width-1)
        while map[r][c] == 'x':
            r = randint(0, height-1)
            c = randint(0, width-1)
        map[r][c] = 'x'
        for (i, j) in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            if (0 <= r+i < height) and (0 <= c+j < width) and (map[r+i][c+j] != 'x'):
                map[r+i][c+j] += 1
    map = "\n".join([" ".join([str(v) for v in l]) for l in map])
    #print (map)
    return (map, mines)
    
        
    
@test.describe("Random Tests")
def rand_tests():
    
    reg = re.compile('[1-8x]')
    for i in range(1 if TEST_FAILS_ALEA else 100):
        
        if not TEST_FAILS_ALEA:
            rnd_m = rand_map()
            m_txt = reg.sub('?', rnd_m[0])
        
        else:
            rnd_m = [""" 
0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 2 3 3 2 1 0 0
0 0 1 3 x x x x 1 0 0
0 0 2 x x 6 x 5 2 0 0
0 0 3 x 4 4 x x 2 0 0
0 0 3 x 5 5 x x 2 0 0
0 0 2 x x x x 3 1 0 0
0 0 1 2 3 3 2 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0
""".strip(), 17]
            m_txt = """
0 0 0 0 0 0 0 0 0 0 0
0 0 0 ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? 0 0 0
0 0 0 0 0 0 0 0 0 0 0
""".strip()
            
        
        
        @test.it("Test "+str(i+1))
        def ttt():
            game.read(m_txt, rnd_m[0])
            m_num = game.count
                
            try:
                my_ans = _my_solve_(m_txt, m_num)
                
            except:
                print("<font face='sans-serif' color='#00cc00'><b>Test #"+str(i+1)+" Exception occured in author's answer!!</b></font>")
                print("Please post a comment in the discourse about that, providing the informations below:\n ")
                print("Number of mines: {}\nOriginal random map:\n{}\n ".format(m_num, rnd_m[0]))
                print("Game map:\n{}".format(m_txt))
                raise Exception("Bad News!!")
            
            makeAssertion(m_txt, m_num, my_ans, isRnd=True, stuff=(rnd_m,i))
    
    
if not failed[0]:
    @test.describe("Congratulations! You have passed all the tests!")
    def congrats():
        print ("<font color='#00aa00' size=2><b>I'm waiting for your <font color='#dddd00'>feedback, rank and vote.<font color='#00aa00'>many thanks! ;-)</b></font>")
    
