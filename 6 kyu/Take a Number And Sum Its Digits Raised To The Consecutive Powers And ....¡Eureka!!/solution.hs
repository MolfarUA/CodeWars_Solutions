module Codewars.G964.Sumdigpow where

import Data.Char(digitToInt)

sumDigPow :: Int -> Int -> [Int]
sumDigPow a b = filter f [a..b]
  where f n = (== n) . sum . zipWith (flip (^)) [1..] . map digitToInt . show $ n
_____________________________________________
module Codewars.G964.Sumdigpow where

sumDigPow :: Int -> Int -> [Int]
sumDigPow a b = filter verify intList 
  where intList = [a..b] 

verify :: Int -> Bool
verify x = applyPowers (toDigit x) == x 

toDigit :: Int -> [Int] 
toDigit 0 = []
toDigit n = toDigit (n `div` 10) ++ [n `mod` 10] 

applyPowers :: [Int] -> Int
applyPowers xs = sum (zipWith (^) xs [1..])
_____________________________________________
module Codewars.G964.Sumdigpow where

sumDigPow :: Int -> Int -> [Int]
sumDigPow a b = filter f [a..b]
  where
    f n = n == sum (zipWith (^) (read . return <$> show n) [1..])
_____________________________________________
module Codewars.G964.Sumdigpow where

sumDigPow :: Int -> Int -> [Int]
sumDigPow a b = filter p [a..b]
  where
  p x = sum (zipWith (^) (map (read . pure) $ show x) [1..]) == x
_____________________________________________
module Codewars.G964.Sumdigpow where
import Control.Applicative
import Data.Char

sumDigPow :: Int -> Int -> [Int]
sumDigPow a b = aux $ [a..b] where
  aux = filter $ (==)
              <*> sum . zipWith (flip (^)) [1..]
               . map digitToInt . show
