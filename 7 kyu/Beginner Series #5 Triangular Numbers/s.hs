56d0a591c6c8b466ca00118b


module Codewars.Numbers where

import Control.Arrow ((&&&))

isTriangular :: Int -> Bool
isTriangular = uncurry (==) . (id &&& (^2) . round . sqrt . fromIntegral) . succ . (*8)
__________________________
module Codewars.Numbers where

isTriangular :: Int -> Bool
isTriangular t = root ^ 2 == 1 + 8 * t where
  root = round . sqrt . toEnum $ 1 + 8 * t
__________________________
module Codewars.Numbers where

isTriangular :: Int -> Bool
isTriangular t = (==t) $ head $ dropWhile (<t) $ scanl (+) 1 [2..]
__________________________
module Codewars.Numbers where
import Data.Fixed

isTriangular :: Int -> Bool
isTriangular t = (mod' (sqrt (fromIntegral (8 * t + 1))) 1) == 0
__________________________
module Codewars.Numbers (isTriangular) where

isTriangular :: Int -> Bool
isTriangular t = n*n == n'*n'
  where n  = sqrt (8*realToFrac t+1)
        n' = realToFrac $ ceiling n
__________________________
module Codewars.Numbers where
import Data.List

isTriangular :: Int -> Bool
isTriangular t = elem t (take 65536 $ snd $ mapAccumL (\x y -> (x+y,x+y)) 0 [1..])
__________________________
module Codewars.Numbers (isTriangular) where

isSquare :: Integral n => n -> Bool
isSquare = f . sqrt . fromIntegral
  where
    f :: Double -> Bool
    f n = n == fromInteger (round n)

isTriangular :: Int -> Bool
isTriangular = isSquare . (+1) . (*8)
