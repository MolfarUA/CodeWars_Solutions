module Kata where

findMissingLetter :: [Char] -> Char
findMissingLetter (x:xs) | head xs == next = findMissingLetter xs
                         | otherwise       = next
                           where next = succ x
________________________
module Kata where

import Data.List
import Data.Char

findMissingLetter :: [Char] -> Char
findMissingLetter cs = head $ [head cs .. last cs] \\ cs 
________________________
module Kata where

findMissingLetter :: [Char] -> Char
findMissingLetter (x:y:xs) = if y == (succ x) then findMissingLetter (y:xs) else succ x
________________________
module Kata where

findMissingLetter :: [Char] -> Char
findMissingLetter (c:cs)
  | (succ c == head cs) = findMissingLetter cs
  | otherwise           = succ c
________________________
module Kata where

findMissingLetter :: [Char] -> Char
findMissingLetter (x:y:xs)
  | succ x == y = findMissingLetter (y:xs)
  | otherwise = succ x
