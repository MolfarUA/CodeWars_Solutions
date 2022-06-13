module SortArray where

import Data.List (sort)

sortArray :: [Int] -> [Int]
sortArray = replaceOdd <$> id <*> sort . filter odd
  where replaceOdd xs [] = xs
        replaceOdd (x:xs) oos@(o:os)
          | even x    = x : replaceOdd xs oos
          | otherwise = o : replaceOdd xs os
_______________________________________________
module SortArray where
import Control.Lens
import Data.List

sortArray :: [Int] -> [Int]
sortArray xs = xs & partsOf (each . filtered odd) %~ sort
_______________________________________________
module SortArray where

import Data.List (sort)

sortArray :: [Int] -> [Int]
sortArray xs = zipInOdds xs (sort $ filter odd xs)


zipInOdds :: [Int] -> [Int] -> [Int]
zipInOdds [] _ = []
zipInOdds xs [] = xs
zipInOdds (x:xs) ys'@(y:ys)
  | odd x = y : zipInOdds xs ys
  | otherwise = x : zipInOdds xs ys'
_______________________________________________
module SortArray where

import Data.List ( sort, unfoldr )

sortArray :: [Int] -> [Int]
sortArray = unfoldr f . ((,) <*> sort . filter odd)
  where
    f ([], _) = Nothing
    f (x:xs, ys) | even x    = Just (x, (xs, ys))
                 | otherwise = Just (head ys, (xs, tail ys))
