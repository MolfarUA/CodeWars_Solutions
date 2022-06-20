57e8f757085f7c7d6300009a


module Kata (planeSeat) where
import Text.Printf

planeSeat :: String -> String
planeSeat s
  | noSeat = "No Seat!!"
  | otherwise = printf "%s-%s" (verticalDirection seatNumber) (horizontalDirection seatDirection)
  where
    seatNumber = (read :: String -> Int) . init $ s
    seatDirection = last s
    noSeat = seatNumber < 1 || seatNumber > 60 || seatDirection `notElem` "ABCDEFGHK"
    

verticalDirection n
  | n <= 20 = "Front"
  | n <= 40 = "Middle"
  | otherwise = "Back"
  
horizontalDirection c
  | c <= 'C' = "Left"
  | c <= 'F' = "Middle"
  | otherwise = "Right"
_______________________________
module Kata (planeSeat) where

import Data.Char

planeSeat :: String -> String
planeSeat s 
    | n == "No Seat!!" || l == "No Seat!!" = "No Seat!!"
    | otherwise                            = n ++ l
    where (num,letter) = span isDigit s
          n = convNum $ ((read num) :: Int)
          l = convLetter $ head letter
          convNum x
            | x <= 20   = "Front-"
            | x <= 40   = "Middle-"
            | x <= 60   = "Back-"
            | otherwise = "No Seat!!"
          convLetter c
            | c `elem` "ABC"  = "Left"
            | c `elem` "DEF"  = "Middle"
            | c `elem` "GHK"  = "Right"
            | otherwise       = "No Seat!!"
_______________________________
module Kata (planeSeat) where

planeSeat :: String -> String
planeSeat s = case cluster . last $ s of
  Just cluster -> case section (read (init s) :: Int) of
    Just section -> section ++ "-" ++ cluster
    Nothing -> "No Seat!!"
  Nothing -> "No Seat!!"

cluster :: Char -> Maybe [Char]
cluster n
  | n `elem` ['A' .. 'C'] = Just "Left"
  | n `elem` ['D' .. 'F'] = Just "Middle"
  | n `elem` ['G', 'H', 'K'] = Just "Right"
  | otherwise = Nothing

section :: (Ord a, Num a) => a -> Maybe [Char]
section n
  | n <= 20 = Just "Front"
  | n <= 40 = Just "Middle"
  | n <= 60 = Just "Back"
  | otherwise = Nothing
