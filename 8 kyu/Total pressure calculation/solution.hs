module DoubletonNumber (doubleton) where
import Data.List

doubleton :: Int -> Int
doubleton n = (head.dropWhile (not.isDoubleton)) [n+1..]

isDoubleton n = 2==(length.nub.show) n 

############
module DoubletonNumber (doubleton) where

import Data.List
import Data.Maybe

doubleton :: Int -> Int
doubleton = fromJust . find isDoubleton . tail . iterate succ
  where isDoubleton = (== 2) . length . nub . show
  
#############
{-# Language ViewPatterns #-}

module DoubletonNumber (doubleton) where

import Data.Set (fromList)

doubleton :: Int -> Int
doubleton (succ -> n) | isDoubleton n = n
                      | otherwise = doubleton n
                      where isDoubleton = (== 2) . length . fromList . show
                      
##############
module DoubletonNumber ( doubleton ) where
import Data.List
  ( nub )

doubleton :: Int -> Int
doubleton inputNumber = nextDoubletonNumber
  where
  
  nextDoubletonNumber :: Int
  nextDoubletonNumber = head
    $ dropWhile
      ( not
      . isDoubleton )
      [ succ inputNumber .. ]
    where
    
    isDoubleton :: Int -> Bool
    isDoubleton number = ( == 2 )
      . length
      . nub
      $ show number
      
#######################
module DoubletonNumber (doubleton) where

import Data.List (nub)

doubleton :: Int -> Int
doubleton n = head . dropWhile (<= n) . filter isDoubleton $ [0 ..]

isDoubleton :: Int -> Bool
isDoubleton = (==) 2 . length . nub . show

#########################
module DoubletonNumber (doubleton) where

import Data.List

doubleton :: Int -> Int
doubleton = findD . (+1)

findD x 
  | (==) 2 (length $ nub $ show x) = x
  | otherwise = findD (x + 1)
