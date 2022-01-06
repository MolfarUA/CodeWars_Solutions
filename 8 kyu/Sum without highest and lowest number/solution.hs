module Kata where

sumArray :: Maybe [Int] -> Int
sumArray (Just xs@(_:_:_)) = sum xs - maximum xs - minimum xs
sumArray _ = 0
________________________________________
module Kata where

import Data.List

sumArray :: Maybe [Int] -> Int
sumArray (Nothing) = 0 :: Int 
sumArray (Just []) = 0 :: Int 
sumArray (Just [_]) = 0 :: Int 
sumArray (Just xs) = sum $ tail $ init $ sort xs 
________________________________________
module Kata where

sumArray :: Maybe [Int] -> Int
sumArray Nothing = 0
sumArray (Just []) = 0
sumArray (Just ([_])) = 0
sumArray (Just (_:_:[])) = 0
sumArray (Just xs) = sum xs - minimum xs - maximum xs
________________________________________
module Kata where
import Data.List
sumArray :: Maybe [Int] -> Int
sumArray (Just (x:x1:x2:xs)) = sum $ init $ tail $ sort $ x:x1:x2:xs
sumArray _ = 0
