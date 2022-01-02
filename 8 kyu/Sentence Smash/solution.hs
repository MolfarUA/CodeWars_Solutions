module Codewars.Kata.Smash where

smash :: [String] -> String
smash = unwords

_____________________________________
module Codewars.Kata.Smash where

import Data.List

smash :: [String] -> String
smash s = intercalate " " s

_____________________________________
module Codewars.Kata.Smash where

smash :: [String] -> String
smash [] = ""
smash [a] = a
smash (x:xs) = x ++ " " ++ smash xs
