import codewars_test as test
from solution import translate
import random

@test.describe("Prologue")
def fixed_test_cases():
    @test.it("Simple")
    def example_test_cases():
        test.assert_equals(translate("***lo w***d!", ["hello", "world"]), "hello world!")
        test.assert_equals(translate("c**l, w*ak!", ["hell", "cell", "week", "weak"]), "cell, weak!")
        test.assert_equals(translate("hell*, w***d!", ["hello", "hell", "word", "world"]), "hello, world!")
        test.assert_equals(translate("***", ["mel", "dell"]), "mel")
        test.assert_equals(translate("", ["hell", "weak"]), "")
        test.assert_equals(translate("****. ***,", ["aaa", "bbbb"]), "bbbb. aaa,")
    @test.it("Trickier")
    def New_Edge_test_cases():
        test.assert_equals(translate("*ow ****v* **** ****u oq**y *t***. s*opq. qro***, q*x", ["ooqqu","ptqqq","qqqovq","qpqq","qpx","oqqqy","qropoo","sqopq","qow"]), "qow qqqovq qpqq ooqqu oqqqy ptqqq. sqopq. qropoo, qpx")

@test.describe("100 random tests")
def random_test_cases():
    #Litteral translation of original kata (javascript)
    common  = "abcdefghijklmnopq"
    special = "rstuvwxyz"
    marks   = ",.!?"
    
    def shake(w):
        W = list(w)
        random.shuffle(W)
        return ''.join(W)
    
    def get_vacant_sizes(A):
        R = []
        for i in range(3, 7):
            if i not in A: R.append(i)
        return R
    
    def create_test(i):
        s   = []
        voc = []
    #choose some combinations of common
        begin = random.randint(0, 14)
        sliced_common = common[begin : begin+3]
    #speech words
        special_index = 0
        while len(s)<i:
            word_len     = random.randint(3, 6)
            asterisk_len = random.randint(1, word_len-1)
            word = special[special_index] + "*"*asterisk_len
            special_index += 1
            while len(word) < word_len: word += sliced_common[random.randint(0, 2)]
            s.append(shake(word))
    #full Asterisk Words
        full_asterisk_words_qty = random.randint(0, 2) 
        vacant_sizes = get_vacant_sizes([len(w) for w in s])
        j = 0
        while j<len(vacant_sizes):
            if full_asterisk_words_qty==0: 
                j+=1
                break
            s.append('*'*vacant_sizes[j])
            vacant_sizes = vacant_sizes[:j] + vacant_sizes[j+1:]
            full_asterisk_words_qty -= 1
    #vocabulary
        for w in s:
            #voc.append(w.replace('*', sliced_common[random.randint(0,2)])) # might be optimized ...
            for j in range(len(w)):
                if w[j]=='*': w = w[:j] + sliced_common[random.randint(0,2)] + w[j+1:]
            voc.append(w)
    #extra vocabulary
        extra_vocabulary = random.randint(0, 4)
        for j in range(len(vacant_sizes)):
            if not extra_vocabulary: break
            word = ''
            while len(word) < vacant_sizes[j]+1:
                word += sliced_common[random.randint(0, 2)]
            voc.append(word)
            extra_vocabulary -= 1
    #punctuation
        punctuation_qty = random.randint(0, i)
        for j in range(punctuation_qty):
            s[j] = s[j] + marks[random.randint(0, 3)]
    #final mixing
        random.shuffle(s)
        random.shuffle(voc)
        s = ' '.join(s)
        return s, voc
        
    def check_translate(s, voc):
        match = lambda w1, w2: len(w1)==len(w2) and all(c1=='*' or c1==c2 for c1, c2 in zip(w1, w2))
        get_match = lambda w1, voc: next(w2 for w2 in voc if match(w1, w2))
        alph = '*abcdefghijklmnopqrstuvwxyz'
        w, l = '', len(s)
        for i in range(l):
            if s[i] in alph: w += s[i]
            elif w:
                s = s[:i-len(w)] + get_match(w, voc) + s[i:]
                w=''
        if w: s = s.replace(w, get_match(w, voc))
        return s
    
    @test.it("Random tests")
    def _100_random_tests():
        for i in range(100):
            s, voc = create_test(i%10)
            actual   = translate(s, voc[::])
            expected = check_translate(s, voc[::])
            test.assert_equals(actual, expected)
            
@test.describe("Epilogue")
def epilogue_test_case():
    @test.it("spell to break the curse")
    def example_test_cases():
        test.assert_equals(translate("luk* nintin w*nty s*v*n b*t t**se e*e*is o*f m*ne *ho *id *ot *ant *me t*o *b* k**g o**r *hem *rin* *hem* *ere *nd *ill tt*** *in *ront o*ff *me*.",
                                    ["tto", "themm", "here", "did", "kill", "but", "bbe", "and", "those", "tthem", "mme", "bring", "want", "front", "enemis", "over", "mmee", "off", "iin", "king", "luke", "nintin", "wenty", "seven", "not", "ooff", "mine", "who", "them"]), "luke nintin wenty seven but those enemis off mine who did not want mme tto bbe king over them bring themm here and kill tthem iin front ooff mmee."
                          )
