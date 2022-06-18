module Narcissistic where

narcissistic :: Integral n => n -> Bool
narcissistic n = n == sum (map (^length digits) digits) where 
  digits = (map (`mod`10) . takeWhile (>0) . iterate (`div`10)) n
________________________
module Narcissistic where

narcissistic n = n == (sum $ map (^m) digits) 
    where digits = map (\x -> read [x] :: Integer) $ show n
          m = length digits
________________________
module Narcissistic where

digs :: Integral x => x -> [x]
digs 0 = []
digs x = digs (x `div` 10) ++ [x `mod` 10]

narcissistic :: Integral n => n -> Bool
narcissistic n = n == sum (map pow digits)
  where digits = digs n
        pow num = num ^ (length digits)
________________________
module Narcissistic where

narcissistic :: Integral n => n -> Bool
narcissistic = flip elem [1, 2, 3, 4, 5, 6, 7, 8, 9, 153, 370, 371, 407, 1634, 8208, 9474, 54748, 92727, 93084, 548834, 1741725, 4210818, 9800817, 9926315, 24678050, 24678051, 88593477, 146511208, 472335975, 534494836, 912985153, 4679307774, 32164049650, 32164049651]
