547b51dcd587f852e4000ad6


module Parsable where
import Text.Read

parses :: String -> Bool
parses str = (readMaybe str :: Maybe Integer) /= Nothing
____________________________
module Parsable where

import Text.Read (readMaybe)
import Data.Maybe (isJust)

parses :: String -> Bool
parses s = isJust (readMaybe s :: Maybe Int)
____________________________
module Parsable where

import Data.Char

parses :: String -> Bool
parses ('-':xs) = parses' xs
parses xs = parses' xs

parses' :: String -> Bool
parses' [] = False
parses' xs = all isDigit xs
____________________________
module Parsable where

reads' :: ReadS Integer
reads' = reads

parses :: String -> Bool
parses xs = case reads' xs of
  [] -> False
  (n, xs'):_ -> null xs'
