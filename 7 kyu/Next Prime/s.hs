58e230e5e24dde0996000070


module Codewars.NextPrime where 

nextPrime :: Integer -> Integer
nextPrime = until isPrime succ . succ where
  isPrime n = all (\x -> n `mod` x > 0) [2..bound n]
  bound = floor . sqrt . fromIntegral
__________________________
module Codewars.NextPrime where 
import Data.List

isPrime :: Integer -> Bool
isPrime n = not $ or $ map (\x -> n `mod` x == 0) [2..mx]
  where mx = round $ sqrt $ fromIntegral n

nextPrime :: Integer -> Integer
nextPrime n = head $ filter isPrime [n+1..]
__________________________
module Codewars.NextPrime where 

nextPrime :: Integer -> Integer
nextPrime n
  | n < 7                                                   = forSmall n
  | otherwise                                               = nextPrime' (n + 1)

forSmall :: Integer -> Integer
forSmall n
  | n < 2                                                    = 2
  | even n                                                   = n + 1
  | otherwise                                                = n + 2

nextPrime' :: Integer  -> Integer
nextPrime' n
  | even n                                                  = nextPrime' (n + 1)
  | n `mod` 3 == 0                                          = nextPrime' (n + 2)
  | otherwise                                               = nextPrime'' n 5

nextPrime'' :: Integer -> Integer -> Integer
nextPrime'' n i
  | n `mod` i == 0 || n `mod` (i + 2) == 0                  = nextPrime' (n + 2)
  | i * i <= n                                              = nextPrime'' n (i + 6)
  | otherwise                                               = n
