56484848ba95170a8000004d


module Codewars.G964.Gps1 where

gps :: Int -> [Double] -> Int
gps s x 
    | length x <= 1 = 0
    | otherwise = floor $ maximum $ zipWith(\a b -> 3600 * (a - b) / fromIntegral s) (tail x) x
_____________________________
module Codewars.G964.Gps1 where

gps :: Int -> [Double] -> Int
gps _ [] = 0
gps _ [_] = 0
gps s xs = floor $ maximum [ (3600 * (b - a)) / (fromIntegral s) | (a, b) <- zip xs (tail xs) ]
_____________________________
module Codewars.G964.Gps1 where

gps :: Int -> [Double] -> Int
gps s x = foldl max 0 $ zipWith (\x1 x2 -> floor $ (x2 - x1) * 3600 / toEnum s) x (tail x)
