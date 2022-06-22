5842df8ccbd22792a4000245


module Kata where

import Data.List (intercalate)

expandedForm :: Int -> String
expandedForm = intercalate " + " . map(\(n, c) ->  c : replicate n '0' ) . reverse . filter ((/='0') . snd) . zip [0..] . reverse . show
_________________________\
module Kata where
import Data.List

expandedForm :: Int -> String
expandedForm n = intercalate " + " [d : take ((length str) - pos) (repeat '0') | (d, pos) <- zip (str) [1..], d /= '0'] 
  where str = show n
_________________________
module Kata where
import Data.List (intercalate, tails)

expandedForm :: Int -> String
expandedForm = intercalate " + " . expand . show where 
  expand = filter (/="") . map zeroTail . init . tails
  zeroTail ('0':_) = ""
  zeroTail ( x:xs) = x : map (\_ -> '0') xs
