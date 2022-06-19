544aed4c4a30184e960010f4


module Divisors where

divisors :: (Show a, Integral a) => a -> Either String [a]
divisors a = case filter ((==0).(rem a)) [2..a`div`2] of
              [] -> Left $ show a ++ " is prime"
              xs -> Right xs
__________________________________
module Divisors where

divisors :: Integer -> Either String [Integer]
divisors a = if null l
           then Left (show a ++ " is prime")
           else Right l
        where l = [x | x <- [2..a`div`2], a`mod`x == 0]
__________________________________
module Divisors where

divisors :: (Show a, Integral a) => a -> Either String [a]
divisors a
  | null divs = Left $ (show a) ++ " is prime"
  | otherwise = Right divs
  where divs = filter ((==0) . mod a) [2..(a-1)]
__________________________________
module Divisors where

divisors :: (Show a, Integral a) => a -> Either String [a]
divisors a = if isPrime then Left primeMsg else Right divs
  where
    divs = [b | b <- [2..(a-1)], a `mod` b == 0]
    isPrime = length divs == 0
    primeMsg = (show a) ++ " is prime"
__________________________________
module Divisors where

divisors :: (Show a, Integral a) => a -> Either String [a]
divisors a = case filter (\d -> a `mod` d == 0) [2..a `div` 2] of
  [] -> Left $ show a ++ " is prime"
  y@(x:xs) -> Right y
