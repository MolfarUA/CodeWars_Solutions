module Codewars.Kata.XO where

import Data.Char (toLower)
import Data.List (filter)

xo :: String -> Bool
xo str = count 'x' str == count 'o' str
  where count char = length . filter ((==) char . toLower)
__________________________________
module Codewars.Kata.XO where

-- | Returns true if the number of
-- Xs is equal to the number of Os
-- (case-insensitive)
check :: String -> Int -> Int -> Bool
check [] 0 0 = True
check [] a b = a == b
check (a:rest) x o 
  | a == 'x' || a == 'X' = check rest (x + 1) o
  | a == 'o' || a == 'O' = check rest x (o + 1)
  | otherwise            = check rest x o
    


xo :: String -> Bool
xo str = check str 0 0
__________________________________
module Codewars.Kata.XO where


import Data.Char (toLower)
import Data.Map (toList, fromListWith)

-- | Returns true if the number of
-- Xs is equal to the number of Os
-- (case-insensitive)
xo :: String -> Bool
xo str 
    | length s == 0 = True
    | length s > 1 = head s == last s
    | otherwise = False
    where s = ( map snd ) ( ( toList . fromListWith (+) ) [(toLower c,1) | c <- str, c `elem` "xoXO"] )
__________________________________
module Codewars.Kata.XO where

import Data.Char

-- | Returns true if the number of
-- Xs is equal to the number of Os
-- (case-insensitive)
xo :: String -> Bool
xo str = length (filter (== 'o') . map toLower $ str) == length (filter (== 'x') . map toLower $ str)
