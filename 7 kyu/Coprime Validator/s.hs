module Coprime (coprime) where

import Data.List

coprime :: Word -> Word -> Bool
coprime x y = common == [1]
  where divisors n = filter (\x -> n `mod` x == 0) [1..n]
        common = intersect (divisors x) (divisors y)
___________________________
module Coprime (coprime) where
import Data.List (intersect)

coprime :: Word -> Word -> Bool
coprime w1 w2= maximum (intersect l1 l2) == 1
          where getfactor y = [x | x <- [1..y], y `mod` x == 0]
                l1 = getfactor w1
                l2 = getfactor w2
___________________________
module Coprime (coprime) where

coprime :: Word -> Word -> Bool
coprime m n = (gcd m n) == 1
___________________________
module Coprime (coprime) where

import Data.List (intersect)

coprime :: Word -> Word -> Bool
coprime x y = (==[1]) $ intersect (factorsOf x) (factorsOf y)
  where
    factorsOf n = [x | x <- [1..n], n `mod` x == 0]
