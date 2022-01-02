module UniqueInOrder (uniqueInOrder) where

import Data.List

uniqueInOrder :: Eq a => [a] -> [a]
uniqueInOrder = map head . group
_____________________________________________
module UniqueInOrder (uniqueInOrder) where
import Data.List

uniqueInOrder :: Eq a => [a] -> [a]
uniqueInOrder = concatMap nub.group
_____________________________________________
module UniqueInOrder (uniqueInOrder) where

uniqueInOrder :: Eq a => [a] -> [a]
uniqueInOrder [] = []
uniqueInOrder (s:[]) = [s]
uniqueInOrder (a:b:xs) = 
  if a == b then 
    uniqueInOrder (a:xs) 
  else 
    a : uniqueInOrder (b:xs)
_____________________________________________
module UniqueInOrder (uniqueInOrder) where

uniqueInOrder :: Eq a => [a] -> [a]
uniqueInOrder b = foldl (\x y->if (null x) || (y /= (last x)) then x++[y] else x) [] b
_____________________________________________
module UniqueInOrder (uniqueInOrder) where
import Data.List

uniqueInOrder :: Eq a => [a] -> [a]
uniqueInOrder = concat . map nub . group

-- how to solve this
-- one: group things using group
-- two: use a function to get one element from each of the created arrays
-- three: concat the results

