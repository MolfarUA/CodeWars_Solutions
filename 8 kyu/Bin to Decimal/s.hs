57a5c31ce298a7e6b7000334


module BinToDecimal where
import Numeric (readInt)
import Data.Char (digitToInt)

binToDec :: String -> Int
binToDec = fst. head . readInt 2 (`elem` "01") digitToInt
_________________________
module BinToDecimal where

import Data.Char

binToDec :: String -> Int
binToDec s = foldl (\acc c -> 2 * acc + digitToInt c) 0 s
_________________________
module BinToDecimal where
import Data.List

binToDec :: String -> Int
binToDec s = sum $ zipWith (\x y -> read [x] * 2 ^ y) (reverse s) [0..]
