module Binaries (code,decode) where

import Numeric (showIntAtBase)
import Data.Char (digitToInt,intToDigit)

code :: String -> String
code = concatMap $ \ c -> let s = showIntAtBase 2 ("01" !!) (digitToInt c) ""
                          in  tail ("0" <* s) ++ '1' : s

decode :: String -> String
decode "" = ""
decode s = let   (l,_:r) = span (== '0') s
                 (b,s') = splitAt (length l + 1) r
           in    binaryToDigit b : decode s'
           where binaryToDigit = intToDigit . foldl ( \ z c -> z + z + fromEnum (c == '1') ) 0
__________________________
module Binaries (code,decode) where
import Numeric
import Data.Char

code :: String -> String
code = concatMap (((++) =<< (++"1") . tail . map (const '0')) . ($"") . showIntAtBase 2 ("01"!!) . digitToInt)

decode :: String -> String
decode "" = ""
decode xs = (intToDigit . fst . head) (readInt 2 (const True) digitToInt as) : decode bs where
  (ts, '1':ds) = span (=='0') xs ; (as, bs) = splitAt (length ts + 1) ds
__________________________
module Binaries where

import           Data.Char                      ( digitToInt
                                                , intToDigit
                                                )
import           Data.List                      ( elemIndices )

code :: String -> String
code = concatMap (encodeDigit . digitToInt)

decode :: String -> String
decode = map (intToDigit . toDec) . splitIntoBits . map digitToInt

splitIntoBits :: [Int] -> [[Int]]
splitIntoBits [] = []
splitIntoBits xs =
    let len = length (takeWhile (== 0) xs) + 1 in take len (drop len xs) : splitIntoBits (drop (2 * len) xs)

encodeDigit :: Int -> String
encodeDigit d =
    let b = replicate (getBits d) '0' ++ "1"
        c = map intToDigit $ toBin d
    in  b ++ c

getBits :: Int -> Int
getBits n = fromIntegral $ floor $ logBase 2 (fromIntegral n)

toBin :: Int -> [Int]
toBin 0 = [0]
toBin x = reverse $ toBin' x
  where
    toBin' 0 = []
    toBin' x | x `mod` 2 == 1 = 1 : toBin' (x `div` 2)
             | otherwise      = 0 : toBin' (x `div` 2)

toDec :: [Int] -> Int
toDec = sum . map (2 ^) . elemIndices 1 . reverse
__________________________
module Binaries (code,decode) where

code :: String -> String
code input = input >>= enc

enc :: Char -> String
enc '0' = "10"
enc '1' = "11"
enc '2' = "0110"
enc '3' = "0111"
enc '4' = "001100"
enc '5' = "001101"
enc '6' = "001110"
enc '7' = "001111"
enc '8' = "00011000"
enc '9' = "00011001"

decode :: String -> String
decode "" = ""
decode ('1' : '0' : t) = '0' : (decode t)
decode ('1' : '1' : t) = '1' : (decode t)
decode ('0' : '1' : '1' : '0': t) = '2' : (decode t)
decode ('0' : '1' : '1' : '1': t) = '3' : (decode t)
decode ('0' : '0' : '1' : '1' : '0': '0' : t) = '4' : (decode t)
decode ('0' : '0' : '1' : '1' : '0': '1' : t) = '5' : (decode t)
decode ('0' : '0' : '1' : '1' : '1': '0' : t) = '6' : (decode t)
decode ('0' : '0' : '1' : '1' : '1': '1' : t) = '7' : (decode t)
decode ('0' : '0' : '0' : '1' : '1' : '0': '0' : '0' : t) = '8' : (decode t)
decode ('0' : '0' : '0' : '1' : '1' : '0': '0' : '1' : t) = '9' : (decode t)
__________________________
module Binaries (code,decode) where

code :: String -> String
code [] = []
code ('0':res) = "10" ++ code res
code ('1':res) = "11" ++ code res
code ('2':res) = "0110" ++ code res
code ('3':res) = "0111" ++ code res
code ('4':res) = "001100" ++ code res
code ('5':res) = "001101" ++ code res
code ('6':res) = "001110" ++ code res
code ('7':res) = "001111" ++ code res
code ('8':res) = "00011000" ++ code res
code ('9':res) = "00011001" ++ code res

decode :: String -> String
decode [] = []
decode ('1':'0':res) = '0' : decode res
decode ('1':'1':res) = '1' : decode res
decode ('0':'1':'1':'0':res) = '2' : decode res
decode ('0':'1':'1':'1':res) = '3' : decode res
decode ('0':'0':'1':'1':'0':'0':res) = '4' : decode res
decode ('0':'0':'1':'1':'0':'1':res) = '5' : decode res
decode ('0':'0':'1':'1':'1':'0':res) = '6' : decode res
decode ('0':'0':'1':'1':'1':'1':res) = '7' : decode res
decode ('0':'0':'0':'1':'1':'0':'0':'0':res) = '8' : decode res
decode ('0':'0':'0':'1':'1':'0':'0':'1':res) = '9' : decode res
