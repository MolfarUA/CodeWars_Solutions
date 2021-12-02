test.describe('Basic Tests')
test.it('should handle simple tests')
test.assert_equals(first_non_repeating_letter('a'), 'a')
test.assert_equals(first_non_repeating_letter('stress'), 't')
test.assert_equals(first_non_repeating_letter('moonmen'), 'e')

test.it('should handle empty strings')
test.assert_equals(first_non_repeating_letter(''), '')

test.it('should handle all repeating strings') 
test.assert_equals(first_non_repeating_letter('abba'), '')
test.assert_equals(first_non_repeating_letter('aa'), '')

test.it('should handle odd characters')
test.assert_equals(first_non_repeating_letter('~><#~><'), '#')
test.assert_equals(first_non_repeating_letter('hello world, eh?'), 'w')

test.it('should handle letter cases')
test.assert_equals(first_non_repeating_letter('sTreSS'), 'T')
test.assert_equals(first_non_repeating_letter('Go hang a salami, I\'m a lasagna hog!'), ',')

test.describe('Random Tests')
from random import randint
sol=lambda s: (lambda uniq: ([a for a in s if s.lower().count(a.lower())==1] or [""])[0])(set(s.lower()))
base="abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789;,:."

for _ in range(40):
    s="".join([base[randint(0,len(base)-1)] for q in range(randint(10,60))])
    test.it ("Should work for "+repr(s))
    test.assert_equals(first_non_repeating_letter(s),sol(s),"It should work for random inputs too")
