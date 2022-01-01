module HumanTime where

import Text.Printf

humanReadable :: Int -> String
humanReadable x = printf "%02d:%02d:%02d" h m s
  where (y, s) = x `divMod` 60
        (h, m) = y `divMod` 60
        
_____________________________________
module HumanTime where

import Text.Printf (printf)

humanReadable :: Int -> String
humanReadable x = printf "%02d:%02d:%02d" h m s where
  h = x `div` 3600
  m = x `div` 60 `mod` 60
  s = x `mod` 60
  
_____________________________________
module HumanTime where

import Data.List (intercalate)

humanReadable :: Int -> String
humanReadable n = intercalate ":".map showNum $ [h, m, s]
  where (h, r) = n `divMod` 3600
        (m, s) = r `divMod` 60
        showNum x | x < 10 = "0" ++ show x
        showNum x = show x
        
_____________________________________
module HumanTime where
import Data.List

humanReadable :: Int -> String
humanReadable x = intercalate ":" $ map (addZero.show. (\f -> f x)) [(`div` 3600),(`mod` 60).(`div` 60),(`mod` 60)]
    where addZero n = case n of [n] -> '0':[n]
                                n -> n
                                
_____________________________________
module HumanTime where

humanReadable :: Int -> String
humanReadable x = (pad hours) ++ ":" ++ (pad minutes) ++ ":" ++ (pad seconds)
  where pad n | n < 10    = '0':(show n)
              | otherwise = show n
        hours   = (x `div` 3600)
        minutes = (x - hours * 3600) `div` 60
        seconds = (x - hours * 3600 - minutes * 60)
