module Perfect (findNextSquare) where

findNextSquare :: Integer -> Integer
findNextSquare x | x == y = z
                 | otherwise = -1
                 where (y:z:_) = dropWhile (< x) $ (^2) <$> [0..]

_______________________________________
module Perfect (findNextSquare) where

findNextSquare :: Integer -> Integer
findNextSquare x = if isSquare x then nextSquare else -1
  where
    nextSquare = (isqrt x + 1) ^ 2

isSquare :: Integer -> Bool
isSquare x = r * r == x
  where
    r = isqrt x

isqrt :: Integer -> Integer
isqrt = floor . sqrt . fromInteger

_______________________________________
module Perfect (findNextSquare) where

findNextSquare :: Integer -> Integer
findNextSquare n | isSqr = s^2
                 | otherwise = -1
  where n' = realToFrac n
        s = floor $ sqrt n' + 1
        isSqr = floor (sqrt n')^2 == n
        
_______________________________________
module Perfect (findNextSquare) where

import Data.Bool

findNextSquare :: Integer -> Integer
findNextSquare =  ($) <$> (bool (-1) <$> head . tail <*>) . (. head) . (==)
              <*> flip dropWhile ((^2) <$> [0..]) . (>)
              
_______________________________________
module Perfect (findNextSquare) where

findNextSquare :: Integer -> Integer
findNextSquare = next . properFraction . sqrt . fromIntegral
  where
    next (i,f) = if f /= 0.0
                    then -1
                    else (i + 1)^2
                    
_______________________________________
module Perfect (findNextSquare) where

findNextSquare :: Integer -> Integer
findNextSquare x
  | isInt (sqrt (fromInteger x)) = (truncate (sqrt (fromInteger x)) + 1) ^ 2
  | otherwise = -1

isInt :: Double -> Bool
isInt = (== 0.0) . snd . properFraction 
