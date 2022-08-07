55e785dfcb59864f200000d9


module Codewars.G964.Countmult where

countSpecMult :: Int -> Integer -> Integer
countSpecMult n m =  div m . product . take n $ sieve [2..] where sieve (p:xs) = p : sieve [x | x <- xs, rem x p > 0]
_________________________________
module Codewars.G964.Countmult where

primes :: [Integer]
primes = sieve [2..]
  where 
    sieve (x:xs) = x:sieve(filter(not . multipleOf x) xs)
    sieve _ = []
    multipleOf x y = (y `mod` x == 0)

countSpecMult :: Int -> Integer -> Integer
countSpecMult n maxval = maxval `div` (product z)
  where z = take n primes
_________________________________
module Codewars.G964.Countmult where

countSpecMult :: Int -> Integer -> Integer
countSpecMult n maxval = div maxval (f (n-1) 2 2)

f :: Int -> Integer -> Integer -> Integer
f 0 _ prod = prod
f n p prod = f (n-1) x (prod*x) where x = nextPrime p


factors :: Integer -> [Integer]
factors x = [n | n <- [3, 5 ..  s ], mod x n == 0]
            where s = ceiling (sqrt (fromIntegral x) ) 

isPrime :: Integer -> Bool
isPrime x
  | x <2 = False
  | x==2 = True
  | mod x 2 == 0 = False
  | x>=2 = factors x == [] 

nextPrime :: Integer -> Integer
nextPrime n = head $ filter(isPrime) [n+1..]
