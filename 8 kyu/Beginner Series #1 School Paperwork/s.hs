55f9b48403f6b87a7c0000bd


module Codewars.Kata.Paperwork where

import Data.Function (on)

paperwork :: Int -> Int -> Int
paperwork = (*) `on` max 0
__________________________
module Codewars.Kata.Paperwork where

paperwork :: Int -> Int -> Int
paperwork classmates pages
  | pages      < 0 = 0
  | classmates < 0 = 0
  | otherwise  = classmates * pages
__________________________
module Codewars.Kata.Paperwork where

paperwork :: Int -> Int -> Int
paperwork = \a b -> if a < 0 || b <0 then 0 else a *b
__________________________
module Codewars.Kata.Paperwork where

paperwork :: Int -> Int -> Int
paperwork n m 
  | n < 0 || m < 0 = 0
  | True = n*m
__________________________
module Codewars.Kata.Paperwork where

paperwork :: Int -> Int -> Int
paperwork n m = if n < 0 || m < 0 then 0 else m * n
