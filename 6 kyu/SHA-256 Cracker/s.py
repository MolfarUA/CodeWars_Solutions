587f0abdd8730aafd4000035


from hashlib import sha256
from itertools import permutations


def sha256_cracker(hash, chars):
    for p in permutations(chars, len(chars)):
        current = ''.join(p)
        if sha256(current.encode('utf-8')).hexdigest() == hash:
            return current
_________________________
from itertools import permutations
from hashlib import sha256
def sha256_cracker(hash, chars):
  return next(iter(''.join(p) for p in permutations(chars) if sha256(str.encode(''.join(p))).hexdigest() == hash), None)
_________________________
import hashlib
import itertools

def sha256_cracker(hash, chars):
  for p in itertools.permutations(chars):
    if(toSHA256("".join(p)) == hash):
      return "".join(p)
  return None
    
def toSHA256(s):   
  m = hashlib.sha256()  
  m.update(s.encode())
  return m.hexdigest()
_________________________
from hashlib import sha256
from itertools import permutations as p
sha256_cracker=lambda h,c:next((''.join(i) for i in p(c) if sha256(''.join(i).encode()).hexdigest()==h),None)
_________________________
from itertools import permutations
from hashlib import sha256

def sha256_cracker(q, chars):
    
    for el in list(permutations(chars)):
        x = "".join(el)
        if sha256(x.encode('utf-8')).hexdigest() == q:
            return x
_________________________
from hashlib import sha256
from itertools import permutations


def sha256_cracker(hash_, chars):
    return next((word for perm in permutations(chars)
                 if sha256((word := ''.join(perm)).encode('utf-8')).hexdigest() == hash_), None)
_________________________
from hashlib import sha256
from itertools import permutations
from typing import Optional


def sha256_cracker(hash: str, chars: str) -> Optional[str]:
    for w in map(''.join, permutations(chars)):
        if sha256(w.encode()).hexdigest() == hash:
            return w
_________________________
sha256_cracker = lambda h, s: next((''.join(e) for e in __import__('itertools').permutations(s) if __import__('hashlib').sha256(''.join(e).encode()).hexdigest()==h), None)
_________________________
import hashlib
import itertools
def hashit(str):
    result = hashlib.sha256(str.encode())
    return result.hexdigest()
def guess(chars):
    yield from list(itertools.permutations(chars,len(chars)))
def sha256_cracker(hash, chars):
    for x in guess(chars):
        str = ''.join(x)
        if (hashit(str) == hash):
            return str
    return None
_________________________
import hashlib
from itertools import permutations

def sha256_cracker(code, chars):
    x = [''.join(i) for i in permutations(chars)]
    for i in x :
        if hashlib.sha256(str.encode(i)).hexdigest() == code :
            return i
