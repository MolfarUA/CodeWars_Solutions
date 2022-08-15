57eadb7ecd143f4c9c0000a3


module Initials where

import Data.Char
import Data.List

getInitials :: String -> String
getInitials = intersperse '.' . map (toUpper . head) . words
_________________________
module Initials where

import Data.List (head, intersperse, words)
import Data.Char (toUpper)

getInitials :: String -> String
getInitials = intersperse '.' . map (toUpper . head) . words
_________________________
module Initials where
import Data.Char

getInitials :: String -> String
getInitials str = (head s) : '.' : (tail s) 
  where s = map (toUpper . head) (words str)
