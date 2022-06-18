module Codewars.G964.FindEven where

import Control.Applicative ((<$>), (<*>))
import Data.List (elemIndex)
import Data.Maybe (fromMaybe)

findEvenIndex :: [Int] -> Int
findEvenIndex = fromMaybe (-1) . elemIndex True .
  (zipWith (==) <$> scanl1 (+) <*> scanr1 (+))
________________________
module Codewars.G964.FindEven where

test arr idx = (sum $ take idx arr) == (sum $ drop (idx + 1) arr)

findEvenIndex :: [Int] -> Int
findEvenIndex arr = 
  case filter (test arr) [0..(length arr - 1)] of
    [] -> -1
    xs -> head xs
________________________
module Codewars.G964.FindEven where

findEvenIndex :: [Int] -> Int
findEvenIndex (a:rr) = go 0 a 0 (sum rr) rr
    where go ix p l r ar
              | l == r = ix
              | null ar = -1
              | (a:as) <- ar = go (ix+1) a (p+l) (r-a) as
________________________
module Codewars.G964.FindEven where
import Data.List (findIndex)

findEvenIndex :: [Int] -> Int
findEvenIndex arr = maybe (-1) id $ findIndex (\(a,b,_) -> a == b) $ pairs
  where pairs = scanr (\x (a,b,c) -> (a + c, b - x, x)) (0, sum arr, 0) arr
________________________
module Codewars.G964.FindEven where

findEvenIndex :: [Int] -> Int
findEvenIndex arr = if null is then -1 else head is
  where is = [ i | i <- [0..length arr], sum (drop (i + 1) arr) == sum (take i arr) ]
