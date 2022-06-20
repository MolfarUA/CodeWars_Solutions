58cb43f4256836ed95000f97


module Codewars.Kata.Cuboids where

findDifference :: (Int, Int, Int) -> (Int, Int, Int) -> Int
findDifference (x1, y1, z1) (x2, y2, z2) = abs(x1 * y1 * z1 - x2 * y2 * z2)
________________________
module Codewars.Kata.Cuboids where

findDifference :: (Int, Int, Int) -> (Int, Int, Int) -> Int
findDifference a b = abs ( cuboidVolume a - cuboidVolume b )

cuboidVolume :: (Int, Int, Int) -> Int
cuboidVolume (x, y, z) = x*y*z
________________________
module Codewars.Kata.Cuboids where
import Data.Function (on)

findDifference :: (Int, Int, Int) -> (Int, Int, Int) -> Int
findDifference = (abs .) . subtract `on` getVolume

getVolume (a, b, c) = a * b * c
