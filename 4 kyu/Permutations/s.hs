5254ca2719453dcc0b00027d


module Codewars.Kata.Permutations (permutations) where
import Data.List (delete, nub)

permutations :: String -> [String]
permutations "" = [""]
permutations xs = [x : y | x <- nub xs, y <- permutations $ delete x xs]
______________________________
module Codewars.Kata.Permutations (permutations) where

import Data.List (nub, delete)

permutations :: String -> [String]
permutations "" = [[]]
permutations xs = nub $ [y| x <- xs, y <- map (x:) . permutations $ delete x xs]
______________________________
module Codewars.Kata.Permutations (permutations) where

import Data.List hiding (permutations)

permutations :: String -> [String]
permutations = map head . group . sort . foldr (\x -> concatMap (rotations . (x :))) [[]]

rotations :: [a] -> [[a]]
rotations xs = take (length xs) (iterate (\(y : ys) -> ys ++ [y]) xs)
