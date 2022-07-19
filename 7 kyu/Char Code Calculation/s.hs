57f75cc397d62fc93d000059


module Kata where

import Data.Char

calc :: String -> Int
calc = (*6) . sum . map sevens

sevens :: Char -> Int
sevens = sum . map (fromEnum . (== '7')) . show . ord
__________________________________
module Kata where

import Data.Char (ord)

calc :: String -> Int
calc x = sum [6 | i <- concatMap (show . ord) x, i == '7']
__________________________________
module Kata where

calc :: String -> Int
calc = sum . map (d . fromEnum)

d 0 = 0
d n | r == 7 = 6 + d q
    | otherwise = d q
    where (q,r) = divMod n 10
__________________________________
module Kata where

calc :: String -> Int
calc = (* 6) . length . filter (== '7') . concatMap (show . fromEnum)
