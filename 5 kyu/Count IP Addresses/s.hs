module IPsBetween where

import Data.List.Split (splitOn)

type IPv4 = String

ipsBetween :: IPv4 -> IPv4 -> Int
ipsBetween s s' = sum $ zipWith3 (\i x y -> (x-y) * (256^i)) [3,2,1,0] (conv s') (conv s)      
   where conv   = map read . splitOn "."
__________________
module IPsBetween where

import Data.Char(isDigit)

type IPv4 = String

ipsBetween :: IPv4 -> IPv4 -> Int
ipsBetween stra strb = sum $ [ (256 ^ n) * x  | (n, x) <- zip [3,2..0] lista ]
    where lista = zipWith (-) (solve strb) (solve stra) 


solve :: String -> [Int]
solve str = map read listx
    where listx = words $ map (\x -> if isDigit x then x else ' ') str

________________________
module IPsBetween where
import Data.List.Split (splitOn)
import Data.Maybe (fromJust)
import Text.Read (readMaybe)
import Data.Function (on)

type IPv4 = String

toDigits :: IPv4 -> Maybe [Int]
toDigits = traverse readMaybe . splitOn "."

collectDigits :: [Int] -> Int
collectDigits = sum . zipWith (\i digit -> digit * 256^i) [0..] . reverse

parseIp :: IPv4 -> Maybe Int
parseIp = fmap collectDigits . toDigits

ipsBetween :: IPv4 -> IPv4 -> Int
ipsBetween = flip (-) `on` fromJust . parseIp
