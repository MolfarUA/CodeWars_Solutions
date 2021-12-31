from math import factorial
from collections import Counter
from functools import lru_cache
from copy import copy

class HashableDict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))

def anagrams(word):
    """
        return the number of anagrams
    """
    @lru_cache()
    def get_count(count_counts):
        if 1 in count_counts and count_counts[1] == sum(count_counts.values()):
            return factorial(count_counts[1])
        count_sum = 0
        for count, count_count in count_counts.items():
            if count_count <= 0: continue
            new_count_counts = copy(count_counts)
            new_count_counts[count] -= 1
            if count > 1:
                new_count_counts[count-1] = new_count_counts.get(count-1, 0) + 1
            count_sum += count_count * get_count(new_count_counts)
        return count_sum

    char_counts = Counter(word)
    count_counts = Counter(char_counts.values())
    # use HashableDict because the return must be hashable to use lru_cache
    return get_count(HashableDict(count_counts))

def listPosition(word):
    """
        Return the anagram list position of the word
    """
    if len(word) <= 1: return 1
    chars = set(word)
    # the number of words whose first char is smaller than that of word
    head_smaller_words = sum([anagrams(word.replace(c, "", 1)) for c in chars if ord(word[0]) > ord(c)])
    return head_smaller_words + listPosition(word[1:])
  
___________________________________________________
from collections import Counter

def listPosition(word):
    l, r, s = len(word), 1, 1
    c = Counter()

    for i in range(l):
        x = word[(l - 1) - i]
        c[x] += 1
        for y in c:
            if (y < x):
                r += s * c[y] // c[x]
        s = s * (i + 1) // c[x]
    return r
  
___________________________________________________
from math import factorial
def listPosition(word):
    """Return the anagram list position of the word"""
    count = 0
    while len(word) > 1:
        first = word[0]
        uniques = set(word)
        possibilities = factorial(len(word))
        for letter in uniques:
            possibilities /= factorial(word.count(letter))
        for letter in uniques:
            if letter < first:
                count += possibilities / len(word) * word.count(letter)
        word = word[1:]
    return count +1

___________________________________________________
from math import factorial
def listPosition(word):
  if not word:
      return 1
  mul = lambda x, y: x * y
  divisor = reduce(mul, (factorial(y) for x, y in set((char, word.count(char)) for char in word)))
  return sorted(word).index(word[0]) * factorial(len(word) - 1) / divisor + listPosition(word[1:])

___________________________________________________
def permute(characters, permutation, dictionary, word):
    if not characters:
        if not permutation in dictionary:
            dictionary[permutation] = len(dictionary) + 1
            return permutation == word
    for i in range(len(characters)):
        nextTry = permute(characters[:i] + characters[i+1:], permutation + characters[i], dictionary, word)
        if nextTry:
            return True
    # will only happen when word cannot be formed from characters 
    return False

factorials = [1]
def fac(n):
    # apply dynamic programming 
    global factorials
    # computed before? 
    if len(factorials) > n:
        return factorials[n]
    # compute it now 
    while len(factorials) <= n:
        x = len(factorials)
        factorial = factorials[x - 1]
        factorials.append(x * factorial)
    return factorials[n]

# computes the number of combinations possible with the 
# given set of characters (characters can be non-distinct) 
def combinations(characters):
    divide_by = 1
    counts = dict()
    for c in characters:
        if c in counts:
            counts[c] += 1
        else:
            counts[c] = 1
    factorial = fac(len(characters))
    for c in counts.keys():
        factorial /= fac(counts[c])
    return int(factorial)

def remove(word, c):
    first_occurrence = word.find(c)
    return word[:first_occurrence] + word[first_occurrence + 1:]
    
# smarter way, only finds an index, without generating permutations 
def solve(word, position):
    if not word:
        return position
    c = word[0]
    earlier = set([x for x in word if x < c])
    for e in earlier:
        try_word = remove(word, e)
        position += combinations(try_word)
    return solve(word[1:], position)

def listPosition(word):
    # return the anagram list position of word 
    '''
    # not efficient enough
    characters = sorted(word)
    dictionary = dict()
    empty_string = ''
    truth = permute(characters, empty_string, dictionary, word)
    return dictionary[word]
    '''
    return solve(word, 1)
  
___________________________________________________
import math
from collections import Counter

def listPosition(word):
    if len(word) == 1:
        return 1
    else:
        return sorted(word).index(word[0]) * calc_word_perm(word) // len(word) + listPosition(word[1:])
        
def calc_word_perm(word):
    denom = 1
    for count in Counter(word).values():
        denom *= math.factorial(count)
    return math.factorial(len(word))//denom
  
___________________________________________________
factorials = [1, 1, 2, 6]
def fatorial(n):
    if n < len(factorials): return factorials[n]
    temp = n * factorial(n-1)
    factorials.insert(n, temp)
    return temp
def listPosition(word):
    n = len(word)
    rank = 0
    for i, char in enumerate(word, start=1):
        count, repetetion = 0, {char: 1}
        for j in word[i:]:
            temp = repetetion.get(j)
            if temp is None: temp = 0
            repetetion.update({j: temp+1})
            count += char > j
        repeating = 1
        for temp in repetetion.values():
            if temp in (0, 1): continue
            repeating *= factorial(temp)
        rank += count * factorial(n-i) // repeating
    return 1+rank
  
___________________________________________________
import math
def listPosition(word):
    """Return the anagram list position of the word"""
    # main logic is this:
    # loop through letters of the word
    # for each letter see if there are letters in the word which appear earlier alphabetically
    # if there are, collect all those earlier letters in a set
    # loop through the set and find the number of combinations of each letter in the set
    # add all those combinations and add + 1 and return the answer
    # refer to https://www.careerbless.com/calculators/rank/index.php,
    # https://stackoverflow.com/questions/5131497/find-the-index-of-a-given-permutation-in-the-sorted-list-of-the-permutations-of
    # also note that for unique characters, no of combinations is n!
    # if a letter is repeated, no of combinations is n!/rep1!rep2!. 
    # for more info, refer to https://math.stackexchange.com/questions/821060/permutations-of-a-string-with-duplicate-characters
    # and https://www.youtube.com/watch?v=1Uy2E2ncazg
    # use the example: SECRET
    
    return helper(word, 1)

def find_combinations(word):
    dictionary, combinations = {}, math.factorial(len(word))
    for letter in word:
        if letter not in dictionary: dictionary[letter] = 1
        else: dictionary[letter] += 1
    for letter in dictionary:
        combinations //= math.factorial(dictionary[letter])
    return combinations

def helper(word, position):
    if not word:
        return position
    first_letter = word[0]
    earlier = set([letter for letter in word if letter < first_letter])
    for letter in earlier:
        index = word.find(letter)
        position += find_combinations(word[:index] + word[index+1:])
    
    # letter has been fixed at that position so remove the letter and move forward
    return helper(word[1:], position)
  
___________________________________________________
import operator
from functools import reduce
from math import factorial
from decimal import *

def perm(word):
    return factorial(len(word)) / reduce(operator.mul, [factorial(word.count(c)) for c in ''.join(set(word))], 1)

def listPosition(word):
    words, pos = perm(word), 0
    for c, i in zip(word, range(len(word))):
        total_words = Decimal(words / (len(word) - i)) * word[i:].count(c)
        pos = (''.join(sorted(word[i:])).index(c)) * total_words / word[i:].count(c) + pos
        words = total_words
    return (pos+1)
  
___________________________________________________
def listPosition(word, rank = 0):
    from math import factorial
    
    if word == '':
        return 1
    
    l = list(set(list(word)))
    l.sort()
    letters = {}
    for x in l:
        letters[x] = word.count(x)
        
    for X in letters:
        if X != word[0]:
            N = len(word) - 1
            temp = letters.copy()
            temp[X] -= 1
            n = factorial(N)
            for x in temp:
                n //= factorial(temp[x])
            rank += n
        else:
            return rank + listPosition(word[1:])
          
___________________________________________________
import math
from collections import defaultdict


def listPosition(word):
    print(word, len(word))
    pos = 1
    letters = len(word)
    ord_lets = sorted([*word])
    letter_count = defaultdict(int)
    for letter in word:
        letter_count[letter] += 1
    for i, letter in enumerate(word):
        dup_den = 1
        pos_value = 1
        for dup in letter_count.values():
            dup_den *= math.factorial(dup)
        letter_count[letter] -= 1
        pos_value = ord_lets.index(letter)
        del ord_lets[pos_value]
        pos += pos_value * math.factorial(letters - (i + 1)) // dup_den
    return pos
