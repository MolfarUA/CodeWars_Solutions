module Codewars.Kata.Bus where

number :: [(Int, Int)] -> Int
number = sum . map (uncurry (-))
_____________________________________
module Codewars.Kata.Bus where

number :: [(Int, Int)] -> Int
number xs = sum $ map (\(x,y) -> x-y) xs
_____________________________________
module Codewars.Kata.Bus where

number :: [(Int, Int)] -> Int
number xs = sum [ fst x - snd x | x <- xs]
_____________________________________
module Codewars.Kata.Bus where

number :: [(Int, Int)] -> Int
number [] = 0
number xs = foldl (\acc (x, y) -> (acc + x  - y)) 0 xs
_____________________________________
module Codewars.Kata.Bus where

number :: [(Int, Int)] -> Int
number []                  = 0
number ((on, off) : stops) = on - off + number stops
_____________________________________
module Codewars.Kata.Bus where

number :: [(Int, Int)] -> Int
number xs = (sum $ map fst xs) - (sum $ map snd xs)
