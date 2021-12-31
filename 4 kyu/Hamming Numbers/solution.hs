module Hamming where

hamming  :: Int -> Int
hamming n = h !! (n-1)
    where h = 1 : map (*2) h `f` map (*3) h `f` map (*5) h
            where f xxs@(x:xs) yys@(y:ys)
                    | x==y = x : f xs ys
                    | x<y  = x : f xs yys
                    | x>y  = y : f xxs ys

___________________________________________________
module Hamming where
import Data.List

hamming  :: Int -> Int
hamming n = head $ drop (n - 1) $ sort seq
  where
    seq = [2^i * 3^j * 5^k | i <- [0..m2], j <- [0..m3], k <- [0..m5]]
    ex = head [x | x <- [1..], x^3 * 30 > n]
    m2 = ex * 5
    m3 = ex * 3
    m5 = ex * 2

___________________________________________________
module Hamming where

import Data.Set (singleton, deleteFindMin, insert, fromList, union)

hamming  :: Int -> Int
hamming n = gen (singleton 1) !! (n - 1)
  where
    gen s = y : gen (union s' $ fromList [y * 2, y * 3, y * 5])
      where
        (y, s') = deleteFindMin s

___________________________________________________
module Hamming (hamming) where

hamming :: Int -> Int
hamming n = hammingSequence !! (n - 1)

hammingSequence :: [Int]
hammingSequence = filter isHamming [1 ..]

isHamming :: Int -> Bool
isHamming 1 = True
isHamming n
  | even n = isHamming (div n 2)
  | mod n 3 == 0 = isHamming (div n 3)
  | mod n 5 == 0 = isHamming (div n 5)
  | otherwise = False

___________________________________________________
module Hamming where

mrg :: Ord a => [a] -> [a] -> [a]
mrg (x:xs) (y:ys) = case compare x y of
                EQ -> x : mrg xs ys
                LT -> x : mrg xs (y:ys)
                GT -> y : mrg (x:xs) ys

hamming  :: Int -> Int
hamming n = (1 : hammingList) !! n

hammingList = 1 : mrg twoS (mrg threeS fiveS)
  where
    twoS = map (2*) hammingList
    threeS = map (3*) hammingList
    fiveS = map (5*) hammingList
