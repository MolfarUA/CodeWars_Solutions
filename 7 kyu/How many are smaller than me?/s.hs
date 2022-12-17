56a1c074f87bc2201200002e


module Codewars.Kata.Smaller where

smaller :: Ord a => [a] -> [Int]
smaller [] = []
smaller (x:xs) = length (filter (<x) xs) : smaller xs
____________________________
module Codewars.Kata.Smaller where

smaller :: Ord a => [a] -> [Int]
smaller [] = []
smaller (x:xs) = foldr (\ v -> if v < x then succ else id) 0 xs : smaller xs
____________________________
module Codewars.Kata.Smaller where

import Data.List ( tails )

smaller :: Ord a => [a] -> [Int]
smaller xs = [ length $ filter (< head x) x | x <- init $ tails xs ]
____________________________
module Codewars.Kata.Smaller where

import Data.List

smaller :: Ord a => [a] -> [Int]
smaller xs = zipWith small xs (tail $ tails xs) where
  small n ns = length $ filter (<n) ns
