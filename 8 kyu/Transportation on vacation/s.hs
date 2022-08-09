568d0dd208ee69389d000016


module Codewars.G964.Rentalcarcost where

rentalCarCost :: Int -> Int
rentalCarCost d
 | d >= 7    = total - 50
 | d >= 3    = total - 20
 | otherwise = total
 where total = 40 * d
__________________________
module Codewars.G964.Rentalcarcost where

rentalCarCost :: Int -> Int
rentalCarCost d 
  | d >= 7 = d * 40 - 50
  | d >= 3 = d * 40 - 20
  | otherwise = d * 40
__________________________
module Codewars.G964.Rentalcarcost where

rentalCarCost :: Int -> Int
rentalCarCost x = 40 * x - discount
  where
    discount
      | x >= 7    = 50
      | x >= 3    = 20
      | otherwise = 0
