module Counter (ones) where

import Data.List.Split (wordsBy)

ones :: [Int] -> [Int]
ones = fmap length . wordsBy (== 0)
_____________________________________________
module Counter (ones) where

import Data.List

ones :: [Int] -> [Int]
ones = map length . filter ((==1) . head) . group
_____________________________________________
module Counter (ones) where
import Data.List

ones :: [Int] -> [Int]
ones = map length . filter (1 `elem`) . group
_____________________________________________
module Counter (ones) where

ones :: [Int] -> [Int]
ones [] = []
ones (x:xs)
    | x == 1 = (length . takeWhile (==1) $ (x:xs)) : (ones . dropWhile (==1) $ (x:xs))
    | otherwise = ones . dropWhile (/= 1) $ (x:xs)
_____________________________________________
module Counter (ones) where

import Data.List (group)

ones :: [Int] -> [Int]
ones = map length . filter ((== 1) . head) . group
_____________________________________________
module Counter (ones) where

ones :: [Int] -> [Int]
ones l 
  | l == []     = []
  | head l == 1 = (fromIntegral $ length $ takeWhile (== 1) l) : (ones $ dropWhile (==1) l)
  | otherwise   = ones $ tail l
