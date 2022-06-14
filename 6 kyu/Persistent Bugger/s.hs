module Codewars.G.Persistence where

import Data.Char (digitToInt)

persistence :: Int -> Int
persistence n = if n < 10 then 0 else 1 + persistence (product $ map digitToInt $ show n)
________________________________________
module Codewars.G.Persistence where
import Data.Char

persistence :: Int -> Int
persistence n
  | (n<10) = 0
  | otherwise = 1 + persistence (product $ map digitToInt $ show n)
________________________________________
module Codewars.G.Persistence where

persistence :: Int -> Int
persistence n
  | n < 10    = 0
  | otherwise = 1 + persistence (digitProduct n)

digitProduct :: Int -> Int
digitProduct n
  | n < 10    = n
  | otherwise = r * digitProduct q
  where
    (q, r) = n `divMod` 10
________________________________________
module Codewars.G.Persistence where

import Data.List
import Data.Tuple

persistence :: Int -> Int
persistence = length . takeWhile (>9) . iterate (product . revDigits) 
    
revDigits = unfoldr (\x -> if x == 0 then Nothing else Just $ swap (x `divMod` 10))
________________________________________
module Codewars.G.Persistence where

import Data.Char (digitToInt)

persistence :: Int -> Int
persistence = length . takeWhile (> 9) . iterate (product . digits)

digits :: Int -> [Int]
digits = map digitToInt . show
