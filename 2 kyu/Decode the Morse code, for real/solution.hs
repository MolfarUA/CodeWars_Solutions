54acd76f7207c6a2880012bb


module Haskell.Codewars.MorseDecoder where

import Haskell.Codewars.MorseDecoder.Preloaded
import Data.List (group, sort, maximum, minimum, minimumBy, partition)
import Data.Function (on)
import Control.Arrow ((&&&))
import Data.List.Split (splitOn)

trim = reverse . dropWhile (== '0') . reverse . dropWhile (== '0')

lenDisp xs = map (head &&& length) . group . sort . map length . group $ xs

dot'   = (id,                     ('.' :))
dash'  = ((' ' :),                ('-' :))
pause' = (((replicate 3 ' ') ++), ('-' :))

dispersion xs
        | length xs < 3 && mul < 5 = zip3 [min, max] [dot', dash'] [1, 1, 1]
        | length xs < 3 && mul < 6 = zip3 [min, max] [dot', pause'] [1, 1, 1]
        | otherwise = zip3 [min, mid, max] [dot', dash', pause'] [0.9, 1, 0.5]
    where min = fromIntegral . minimum . map fst $ xs
          max = fromIntegral . maximum . map fst $ xs
          mid = min + (max - min) / 7 * 3
          mul = max / min

mass c x (m, s, q) = (s, c * abs (x - m) * q)

findOperator disp (len, count) = (len, fst . minimumBy (compare `on` snd) . map (mass count' len') $ disp)
      where len' = fromIntegral len
            count' = fromIntegral count

stat xs = map (findOperator disp) xs
      where disp = dispersion xs

decodeBitsAdvanced :: String -> String
decodeBitsAdvanced bits = decode' bits'
    where bits' = trim bits
          dict = stat . lenDisp $ bits'
          applyDict ('0', l) xs = let Just (f, _) = lookup l dict in f xs
          applyDict (_, l) xs = let Just (_, f) = lookup l dict in f xs
          decode' = foldr applyDict [] . map (head &&& length) . group

decodeMorse :: String -> String
decodeMorse = unwords . filter (not . null) . map decodeWord . splitOn "   "
    where decodeWord = concat . map morseCodes . words
          morseCodes x = case lookup x morseCode of
            Nothing -> ""
            Just c -> c
_______________________________________________
module Haskell.Codewars.MorseDecoder where
import Haskell.Codewars.MorseDecoder.Preloaded (morseCode)
import Data.Maybe
import Data.List
import Data.List.Split

decodeBitsAdvanced :: String -> String
decodeBitsAdvanced "" = ""
decodeBitsAdvanced bits = concatMap toMorse pulses
  where strip c = dropWhile (==c) . reverse . dropWhile (==c) . reverse
        pulses = map (\s -> (head s, length s)) $ group $ strip '0' bits
        average [] = 1/0; average xs = realToFrac (sum xs) / genericLength xs
        averageOf c = average $ map snd $ filter ((==c).fst) pulses
        det = ceiling $ minimum [averageOf '0', averageOf '1']
        lengths = nub $ map snd pulses
        shorts = filter (<=det) lengths
        threshold = ceiling (4.1*(average shorts))
        longs = filter (<threshold) $ lengths \\ shorts
        toMorse (c,n)
          | n `elem` shorts = if c == '0' then ""  else "."
          | n `elem` longs  = if c == '0' then " " else "-"
          | otherwise = "   "

decodeMorse :: String -> String
decodeMorse "" = ""
decodeMorse morse = (intercalate " " . map (concat . map (fromJust . flip lookup morseCode) . splitOn " ") . splitOn "   ") morse

_______________________________________________
module Haskell.Codewars.MorseDecoder where 
import Haskell.Codewars.MorseDecoder.Preloaded (morseCode)
import Data.List.Split
import Data.List
import Data.Maybe

decodeBitsAdvanced :: String -> String
decodeBitsAdvanced bits = concat $ map recognize bytes
  where
    bytes = group $ strip0 bits
    l = length bytes
    stat = if l < 6
      then 15 * (foldl min 256 $ map length bytes) * l
      else 10 * (sum $ map length bytes)
    getSize xs = g $ length xs
    g size = if size * 18 * l > 5 * stat then 2
      else if size * 9 * l > stat then 1 else 0
    recognize (x:xs) = if x == '0'
      then ["", " ", "   "] !! getSize (x:xs)
      else [".", "-", "-"] !! getSize (x:xs)
    strip0 = dropWhile (== '0') . reverse . dropWhile (== '0') . reverse

decodeMorse :: String -> String
decodeMorse = unwords . filter (not . null) . map (concatMap (\x -> fromJust $ lookup x morseCode) . words) . splitOn "   "
_______________________________________________
module Haskell.Codewars.MorseDecoder where 
import Haskell.Codewars.MorseDecoder.Preloaded (morseCode)
import Data.Maybe
import Data.List

decodeBitsAdvanced :: String -> String
decodeBitsAdvanced bits = concat $ map decodeBits $ gr
    where
        gr = group $ trim '0' bits
        ls = [length x | x <- gr]
        ls0 = [length x | x <- gr, head x == '0']
        ls1 = [length x | x <- gr, head x == '1']
        d = (round $ avg ls) + if length ls < 500 then 0 else 1
        c = d
        w = (round $ avg ls1 * 3) + if length ls1 < 3 then 1
                                    else if length ls < 500 then -1
                                                            else -2
        decodeBits :: String -> String
        decodeBits xs
            | head xs == '1'  = if l <= d then "." else "-"
            | otherwise       = if l <= c then ""
                                else if l <= w then " " else "   "
            where l = length xs

avg :: [Int] -> Double
avg [] = 0
avg xs = fromIntegral (sum xs) / fromIntegral (length xs)

decodeMorse :: String -> String
decodeMorse xs = concat $ decode $ words $ sp $ trim ' ' xs
    where
        decode [] = []
        decode (x:xs) = let s = lookup x morseCode
                            t = if s == Nothing then " " else fromJust s
                        in t : decode xs

trim :: Char -> String -> String
trim c = f . f
    where f = reverse . dropWhile (== c)

sp :: String -> String
sp [] = []
sp (' ':' ':' ':xs) = " _ " ++ sp xs
sp (x:xs) = x : sp xs
