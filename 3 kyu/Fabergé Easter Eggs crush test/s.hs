54cb771c9b30e8b5250011d4


module Faberge where

heigth n m | n > m = heigth m m
           | otherwise = f 0 1 1
           where f a b c | c > n = a
                         | otherwise = f (a + d) d (c + 1)
                         where d = b * (m - c + 1) `div` c
_________________________
module Faberge where
heigth :: Integer -> Integer -> Integer 
-- inefficient solution
-- heigth n m | n == 0 || m == 0 = 0
--            | otherwise = 1 + (heigth n (m-1)) + (heigth (n-1) (m-1))

-- I will explain this in the kata comments :)
heigth n m | n == 0 || m == 0 = 0
           | n > m = heigth m m
           | otherwise = (sum $ scanl (\s x -> s * (m-x+1) `div` x ) 1 [1..n]) - 1
_________________________
module Faberge where

heigth :: Integer -> Integer -> Integer 
heigth n m = step(1, 1, 0) - 1
  where 
    step (curr, t, sum)
      | t == n+2 = sum
      | otherwise = step ((curr*(m+1-t)) `div` t, t+1, sum+curr)
_________________________
module Faberge where heigth n m = sum (scanl (\s x -> s * (m-x+1) `div` x ) 1 [1..n]) - 1
_________________________
module Faberge where

heigth :: Integer -> Integer -> Integer 
heigth n m = chooseSum m (min n m) where
  chooseSum :: Integer -> Integer -> Integer
  chooseSum n k = snd (chooseSumPrev n k) 
  chooseSumPrev :: Integer -> Integer -> (Integer, Integer)
  chooseSumPrev _ 0 = (1, 0)
  chooseSumPrev n k =
    let (prev, cumulative) = chooseSumPrev n (k - 1)
        curr = prev * (n - k + 1) `div` k 
        currCumulative = curr + cumulative in 
        (curr, currCumulative)
