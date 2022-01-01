module Codewars.Kata.YourOrderPlease where

import Data.List (sortOn, find)
import Data.Char (isDigit)

yourOrderPlease :: String -> String
yourOrderPlease = unwords . sortOn (find isDigit) . words

_____________________________________________
module Codewars.Kata.YourOrderPlease where
import Data.List 
import Data.Char
import Data.Ord

yourOrderPlease :: String -> String
yourOrderPlease = unwords . sortBy (comparing (head . filter isDigit)) . words

_____________________________________________
module Codewars.Kata.YourOrderPlease where
import Data.Char ( isNumber )
import Data.List ( find, sortBy )
import Data.Ord  ( comparing )

yourOrderPlease :: String -> String
yourOrderPlease = unwords . sortBy (comparing $ find isNumber) . words

_____________________________________________
module Codewars.Kata.YourOrderPlease where
import Data.List (sortOn)
import Data.Char (isNumber)

yourOrderPlease :: String -> String
yourOrderPlease = unwords . sortOn(filter isNumber). words
  
_____________________________________________
module Codewars.Kata.YourOrderPlease where

import Data.List
import Data.Ord
import Data.Char

yourOrderPlease :: String -> String
yourOrderPlease [] = []
yourOrderPlease s = unwords $ sortBy (comparing $ filter isDigit) $ words s
