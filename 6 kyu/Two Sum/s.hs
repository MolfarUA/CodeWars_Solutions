module TwoSum (twoSum) where

twoSum :: [Int] -> Int -> (Int,Int)
twoSum xxs n = head [(fst x,fst y) | x <- xs, y <- xs, snd x + snd y == n, fst x < fst y]
  where xs = zip [0..] xxs
________________________________
module TwoSum (twoSum) where

twoSum :: [Int] -> Int -> (Int,Int)
twoSum ns t = head [
  (x, y) |
   x <- [0..length ns - 1],
   y <- [0..length ns - 1],
   x < y,
   (ns !! x) + (ns !! y) == t]
________________________________
module TwoSum (twoSum) where
import Data.List

twoSum :: [Int] -> Int -> (Int,Int)
twoSum xs n = head [(i1,i2) | i1 <- [0..(length xs)-1], i2<-[i1+1..(length xs)-1], xs!!i1+xs!!i2==n ]
________________________________
module TwoSum (twoSum) where

import Control.Monad.State (State,evalState,get,put)
import Data.Map (Map,empty,member,insert,(!))
import Data.Foldable (foldlM)

twoSum :: [Int] -> Int -> (Int,Int)
twoSum xs n = evalState (foldlM go undefined $ zip [0..] xs) empty where
  go :: (Int,Int) -> (Int,Int) -> State (Map Int Int) (Int,Int)
  go z (i,x) = do
    state <- get
    if member (n-x) state then do
      return ( i, state ! (n-x) )
    else do
      put $ insert x i state
      return z
________________________________
module TwoSum (twoSum) where

import Data.List

justToInt :: Maybe Int -> Int
justToInt (Just x) = x

twoSum :: [Int] -> Int -> (Int,Int)
twoSum [] _ = (0, 0)
twoSum xs x
  | elem y end = (0, (justToInt(elemIndex y end)) + 1)
  | otherwise = ((fst elseVal) + 1, (snd elseVal) + 1)
  where y = x - (head xs)
        end = tail xs
        elseVal = twoSum end x
