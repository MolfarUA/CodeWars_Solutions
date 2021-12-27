module SumOfIntervals (sumOfIntervals) where

import Control.Monad (join)
import Data.Bifunctor (bimap)
import Data.List (sort)

sumOfIntervals :: [(Int, Int)] -> Int
sumOfIntervals = sum . map (uncurry subtract) . scanl1 (join bimap . max . snd) . sort

__________________________
module SumOfIntervals (sumOfIntervals) where

import Data.List

interval (x, y) = [x..y-1]

sumOfIntervals :: [(Int, Int)] -> Int
sumOfIntervals = length . foldl union [] . map interval

___________________________
module SumOfIntervals (sumOfIntervals) where
import Data.List

sumOfIntervals :: [(Int, Int)] -> Int
sumOfIntervals intervals = length $ nub (concat (map (\(x, y) -> [x..y-1]) intervals))
___________________________
module SumOfIntervals (sumOfIntervals) where

import Data.List(nub)

sumOfIntervals :: [(Int, Int)] -> Int
sumOfIntervals = length . nub . concat . map (\(x, y) -> [x..y - 1])
___________________________
module SumOfIntervals (sumOfIntervals) where
import Data.List

sumOfIntervals :: [(Int, Int)] -> Int
sumOfIntervals = length . nub . concatMap createIntervals
  where
    createIntervals x = [fst x .. snd x - 1]
___________________________
module SumOfIntervals (sumOfIntervals) where
import Data.List

sumOfIntervals :: [(Int, Int)] -> Int
sumOfIntervals = length . nub . concat . map(\(x,y) -> [x..y-1])
___________________________
module SumOfIntervals (sumOfIntervals) where

import Data.List

sumOfIntervals :: [(Int, Int)] -> Int
sumOfIntervals = foldl g 0 . reverse . foldl f [] . sort
    where g n (a,b) = n + (b - a)
          f [] x = [x]
          f  ((a1, b1):xs) (a2, b2)
            | b1 >= b2 = (a1, b1):xs
            | b1 >= a2 = (a1, b2):xs
            | otherwise = (a2, b2):(a1, b1):xs
