@test.describe("Sample tests")
def sample():
    test.assert_equals(count_patterns_from('A',10), 0)
    test.assert_equals(count_patterns_from('A',0),  0)
    test.assert_equals(count_patterns_from('E',14), 0)
    test.assert_equals(count_patterns_from('B',1),  1)
    test.assert_equals(count_patterns_from('C',2),  5)
    test.assert_equals(count_patterns_from('E',2),  8)
    test.assert_equals(count_patterns_from('E',4),  256)



@test.describe("More tests")
def more():
    
    @test.it("Small outputs")
    def t():
        test.assert_equals(count_patterns_from('D',3),  37)
        test.assert_equals(count_patterns_from('E',4),  256)


    @test.it("Large output")
    def t():
        test.assert_equals(count_patterns_from('E',8),  23280)



@test.it("Random tests")
def rndTests():
    
    from random import randrange as rand
    
    
    EQUIV_PTS = {same: src for src,seq in (('A','CGI'), ('B','DFH')) for same in seq}
    
    ALL       = set('ABCDEFGHI')
    LINKED_TO = {'A': ('BC','DG','EI','F', 'H'),
                 'B': ('A', 'C', 'D', 'EH','F', 'G', 'I'),
                 'C': ('BA','D', 'EG','FI','H'),
                 'D': ('A', 'B', 'C', 'EF','G', 'H', 'I'),
                 'E': tuple('ABCDFGHI'),
                 'F': ('A', 'B', 'C', 'ED','G', 'H', 'I'),
                 'G': ('DA','B', 'EC','F', 'HI'),
                 'H': ('A', 'EB','C', 'D', 'F', 'G', 'I'),
                 'I': ('EA','B', 'FC','D', 'HG')
                }
    
    
    def DFS(c, depth, root, seens, patterns):
        if depth > len(ALL): return                
        
        patterns[root][depth] += 1
        
        seens.add(c)
        toExplore = ''.join( next((n for n in seq if n not in seens), '') for seq in LINKED_TO[c] )
        for nextC in toExplore:
            DFS(nextC, depth+1, root, seens, patterns)
        seens.discard(c)
        
    
    PATTERNS = {}
    for c in "ABE":
        PATTERNS[c] = [0]*10
        DFS(c, 1, c, set(), PATTERNS)
    
    
    def refCounts(start, length):
        if not (0 < length < 10) or start not in ALL: return 0    
        
        actualStart = EQUIV_PTS.get(start, start)
        return PATTERNS[actualStart][length]
        
    
    """ Random tests """
    for c in ALL:
        for _2 in range(4):
            
            n = rand(11)
            if n==10: n = rand(10,25)
            test.assert_equals(count_patterns_from(c,n), refCounts(c,n))
            
