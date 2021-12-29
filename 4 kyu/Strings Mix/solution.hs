module Codewars.G964.Mixin where
import Data.Map.Strict (insertWith, empty, Map, unionWith, elems, mapWithKey)
import Data.Char (isLower, ord)
import Data.List (sortBy, intercalate)

counts :: String -> Map Char Int
counts s = foldr (\c m -> if isLower c then insertWith (+) c 1 m else m) empty s

mixThem :: (Char, Char, Int) -> (Char, Char, Int) -> (Char, Char, Int)
mixThem (k1, s1, cnt1) (k2, s2, cnt2)
  | cnt1 > cnt2 = (k1, s1, cnt1)
  | cnt1 < cnt2 = (k2, s2, cnt2)
  | otherwise = (k1, '=', cnt1)

orderMix (k1, s1, cnt1) (k2, s2, cnt2)
  | cnt1 /= cnt2 = if cnt1 > cnt2 then LT else GT
  | s1 /= s2 = compare (ord s1) (ord s2)
  | otherwise = compare (ord k1) (ord k2)

mix :: String -> String -> String
mix s1 s2 = intercalate "/" $ map (\(k, s, cnt) -> [s] ++ ":" ++ (replicate cnt k)) $ filter (\(_, _, cnt) -> cnt > 1) cl
  where
    singleMix s k cnt = (k, s, cnt)
    c = unionWith mixThem (mapWithKey (singleMix '1') $ counts s1) (mapWithKey (singleMix '2') $ counts s2)
    cl = sortBy orderMix $ elems c

__________________________________________________
module Codewars.G964.Mixin where
import Data.List (intercalate, sort)
import Data.Maybe (mapMaybe)
import Control.Arrow

mix :: [Char] -> [Char] -> [Char]
mix s1 s2 = intercalate "/" $ map showCount $ sort $ mapMaybe mkCount ['a' .. 'z']
  where
    showCount (c, (p, l)) = p : ':' : replicate (-c) l
    mkCount l = if c1 > 1 || c2 > 1 then Just ((-(max c1 c2)), (prefix, l)) else Nothing
      where
        (c1, c2) = (($s1) &&& ($s2)) (length . filter (==l))
        prefix = case c1 `compare` c2 of
                     GT -> '1'
                     LT -> '2'
                     EQ -> '='
                     
__________________________________________________
module Codewars.G964.Mixin where

import Data.Char (isAsciiLower)
import Data.List (sort, sortOn, intercalate, group)

mix :: String -> String -> String
mix s1 s2 = intercalate "/" $ sortOn (negate . length)
    $ sortOn head $ filter (/= "") $ zipWith sc (ss s1) (ss s2)
  where ss = group . sort . (['a'..'z'] ++) . filter isAsciiLower
        sc c1 c2
            | l1 < 3 && l2 < 3 = ""
            | l1 == l2  = "=:" ++ tail c1
            | l1 >  l2  = "1:" ++ tail c1
            | otherwise = "2:" ++ tail c2
          where l1 = length c1
                l2 = length c2
                
__________________________________________________
module Codewars.G964.Mixin where

import Data.Char
import Data.List

mix :: String -> String -> String
mix s1 s2 = intercalate "/" 
  $ sortOn (negate . length)
  $ sortOn head 
  $ filter (/= "") 
  $ zipWith sc (ss s1) (ss s2)
  where ss = group . sort . (['a'..'z'] ++) . filter isAsciiLower
        sc c1 c2
            | l1 < 3 && l2 < 3 = ""
            | l1 == l2  = "=:" ++ tail c1
            | l1 >  l2  = "1:" ++ tail c1
            | otherwise = "2:" ++ tail c2
              where l1 = length c1
                    l2 = length c2
