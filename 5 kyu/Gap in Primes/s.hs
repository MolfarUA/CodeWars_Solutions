561e9c843a2ef5a40c0000a4


module Codewars.G964.GapInPrimes where

import Data.List (find)
import Control.Arrow ((&&&))

gap :: Integer -> Integer -> Integer -> Maybe (Integer, Integer)
gap g m n = find (\(a, b) -> b-a == g) . uncurry zip . (id &&& drop 1) . filter isPrime $ [m..n]
    where isPrime n = all (\d -> n `mod` d  /= 0) [2 .. floor . sqrt . fromIntegral $ n]
__________________________________
module Codewars.G964.GapInPrimes where

import Data.Maybe

gap :: Integer -> Integer -> Integer -> Maybe (Integer, Integer)
gap g m n = listToMaybe . filter (\(x, y) -> y - x == g) $ zip primeListBetweenMN (tail primeListBetweenMN)
  where
    isPrime n = not . any (== 0) . map (\x -> n `rem` x) $ [2 .. floor . sqrt . fromIntegral $ n]
    primeListBetweenMN = filter isPrime [m .. n]
__________________________________
module Codewars.G964.GapInPrimes where

isPrime :: Integer -> Bool
isPrime 2 = True
isPrime n = let factors = filter (\c -> (mod n c) == 0) [2 .. (floor . sqrt . fromIntegral $ n)]
                          in (mod n 2 /= 0) && (length factors) == 0

intermediateGap :: Integer -> [Integer] -> Maybe (Integer,Integer)
intermediateGap _ [] = Nothing
intermediateGap _ [x] = Nothing
intermediateGap n (x:y:xs)
    | (y - x) == n = Just (x,y)
    | otherwise = intermediateGap n (y:xs)

gap :: Integer -> Integer -> Integer -> Maybe (Integer,Integer)
gap g m n = let primesInRange = filter isPrime [m .. n]
                 in intermediateGap g primesInRange
