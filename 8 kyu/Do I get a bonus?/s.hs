56f6ad906b88de513f000d96


module Bonus where

iHazBonus :: Float->  Bool -> String

iHazBonus salary bonus = '$' : show (salary * if bonus then 10 else 1)
__________________________
module Bonus where

iHazBonus :: Float->  Bool -> String

iHazBonus salary bonus = "$" ++ (show money)
  where
  money
    | bonus == True = salary * 10
    | otherwise = salary
__________________________
module Bonus where

iHazBonus :: Float->  Bool -> String

iHazBonus h a = if a then "$"++(show(h * 10) ) else "$"++(show h)
