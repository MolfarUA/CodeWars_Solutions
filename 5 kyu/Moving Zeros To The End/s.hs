52597aa56021e91c93000cb0


module MovingZeros (moveZeros) where

import Data.List

moveZeros :: [Int] -> [Int]
moveZeros xs = uncurry (++) $ partition (/=0) xs
_____________________________
module MovingZeros (moveZeros) where

import Data.List

moveZeros :: [Int] -> [Int]
moveZeros = uncurry (++) . partition (/= 0)
_____________________________
module MovingZeros (moveZeros) where

moveZeros :: [Int] -> [Int]
moveZeros = go [] []
  where
    go acc zeroes [] = reverse acc ++ zeroes
    go acc zeroes (0:ns) = go acc (0:zeroes) ns
    go acc zeroes (n:ns) = go (n:acc) zeroes ns
_____________________________
module MovingZeros (moveZeros) where

moveZeros :: [Int] -> [Int]
moveZeros [] = []
moveZeros (x : xs) | x == 0 = moveZeros xs ++ [x]
                   | otherwise = x : moveZeros xs
