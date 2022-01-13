module PasswordMaker where

import Data.Char(toLower)

translate :: Char -> Char
translate x
 | toLower x == 'i' = '1'
 | toLower x == 'o' = '0'
 | toLower x == 's' = '5'
 | otherwise = x

makePassword :: String -> String
makePassword = map (translate . head) . words
__________________________________
module PasswordMaker where

makePassword :: String -> String
makePassword = map (translate . head) . words where
  translate c
    | c `elem` "iI" = '1'
    | c `elem` "oO" = '0'
    | c `elem` "sS" = '5'
    | otherwise = c
__________________________________
module PasswordMaker where

makePassword :: String -> String
makePassword = map (digit . head) . words
  where digit c | c `elem` "iI" = '1'
                | c `elem` "oO" = '0'
                | c `elem` "sS" = '5'
                | otherwise     =  c
__________________________________
module PasswordMaker where

makePassword :: String -> String
makePassword = map repl . map head . words

repl 'i' = '1'
repl 'I' = '1'
repl 'o' = '0'
repl 'O' = '0'
repl 's' = '5'
repl 'S' = '5'
repl x = x
