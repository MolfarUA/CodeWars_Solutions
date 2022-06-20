55466989aeecab5aac00003e


module Codewars.Kata.Rectangle where

squaresInRect :: Integer -> Integer -> Maybe [Integer]
squaresInRect lng wdth | lng == wdth = Nothing
squaresInRect lng wdth = Just $ sir lng wdth
    where
        sir l w | l == w = [l]
        sir l w
            | l > w = w : sir (l - w) w
            | l < w = l : sir l (w - l)
______________________________
module Codewars.Kata.Rectangle where

squaresInRect :: Integer -> Integer -> Maybe [Integer]
squaresInRect lng wdth
    | lng == wdth = Nothing
    | otherwise   = Just $ squaresInRect' lng wdth
  where
    squaresInRect' x y = case x `compare` y of
        EQ -> [x]
        LT -> x:squaresInRect' x (y - x)
        GT -> y:squaresInRect' (x - y) y
______________________________
module Codewars.Kata.Rectangle where

squaresInRect :: Integer -> Integer -> Maybe [Integer]
squaresInRect lng wdth
  | lng > 0 && wdth > 0 && lng /= wdth = Just $ solution lng wdth
  | otherwise = Nothing

solution lng wdth
  |lng > 0 && wdth > 0 = sq : solution sq (max lng wdth - sq)
  | otherwise = []
  where sq = min lng wdth
