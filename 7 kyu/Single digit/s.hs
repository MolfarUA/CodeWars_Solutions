module SingleDigit (singleDigit) where

import Data.Bits (popCount)

singleDigit :: Integer -> Int
singleDigit = fromIntegral . until (< 10) (fromIntegral . popCount)
__________________________
module SingleDigit (singleDigit) where

toBin :: Integer -> [Int]
toBin 0 = []
toBin n = toBin (n `div` 2) ++ [fromIntegral (n `mod` 2)]

singleDigit :: Integer -> Int
singleDigit n 
  |n < 10 = fromIntegral(n)
  |s < 10 = s
  |otherwise = singleDigit $ fromIntegral(s)
  where s = sum . toBin $ n
__________________________
module SingleDigit
  ( singleDigit )
where
import Data.Bits
  ( popCount )
import Data.Char
  ( digitToInt )
import Numeric
  ( showIntAtBase )

singleDigit :: Integer -> Int
singleDigit integer =
  if integer < 10
    then fromEnum integer
    else
      singleDigit .
      toEnum .
      sum .
      map digitToInt $
      showIntAtBase 2 ( "01" !! ) integer ""
__________________________
module SingleDigit (singleDigit) where

toBinary :: Integer -> [Integer]
toBinary 0 = [0]
toBinary n = toBinary (quot n  2) ++ [rem n 2]

testNum :: Integer -> Int
testNum num = if num < 10 then (fromIntegral num) else singleDigit num

singleDigit :: Integer -> Int
singleDigit num 
  | num < 10 = fromIntegral num
  | otherwise = testNum (foldr (+) 0 (toBinary num))
__________________________
module SingleDigit (singleDigit) where
import Data.Bits  
singleDigit :: Integer -> Int
singleDigit = fromInteger.count

count :: Integer -> Integer
count n = if abs n < 10 then n else count $ toInteger $ popCount n
__________________________
module SingleDigit (singleDigit) where

import Data.Bits (popCount)

singleDigit :: Integer -> Int
singleDigit n
  | length (show n) == 1 = fromIntegral n
  | otherwise            = singleDigit (fromIntegral $ popCount n)
__________________________
module SingleDigit (singleDigit) where

singleDigit :: Integer -> Int
singleDigit x
  | x >= 10 = singleDigit $ breakDown x
  | otherwise = fromIntegral x

breakDown :: Integer -> Integer 
breakDown 0 = 0
breakDown x  = remainder + breakDown quotient
  where (quotient, remainder) = divMod x 2
