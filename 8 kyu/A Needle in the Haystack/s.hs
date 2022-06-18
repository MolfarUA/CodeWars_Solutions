module ANeedleInTheHaystack (findNeedle) where

import Data.Maybe
import Data.List

findNeedle :: [String] -> String
findNeedle = ("found the needle at position " ++) . show . fromJust . elemIndex "needle"
________________________
module ANeedleInTheHaystack (findNeedle) where

findNeedle :: [String] -> String
findNeedle = ("found the needle at position " ++) . show . length . takeWhile (/="needle")
________________________
module ANeedleInTheHaystack (findNeedle) where

findNeedle :: [String] -> String
findNeedle list = "found the needle at position " ++ show (indexOfNeedle list 0)
    where indexOfNeedle list index
              | (head list) == "needle" = index
              | otherwise = indexOfNeedle (tail list) (index + 1)
________________________
module ANeedleInTheHaystack (findNeedle) where

import Data.Maybe
import Data.List
import Text.Printf

findNeedle :: [String] -> String
findNeedle = printf "found the needle at position %d" . fromJust . elemIndex "needle"
________________________
module ANeedleInTheHaystack (findNeedle) where
import Data.List (elemIndex)

findNeedle :: [String] -> String
findNeedle haystack = "found the needle at position " ++ show index
    where Just index = elemIndex "needle" haystack
