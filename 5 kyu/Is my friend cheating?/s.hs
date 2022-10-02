5547cc7dcad755e480000004


module Codewars.Kata.RemovNB where
      
removNb :: Integer-> [(Integer, Integer)]
removNb n = [(a,b) | a <- [1..n], let (b, r) = quotRem (sn -a) (a + 1), r == 0, b <= n, b /= a]
            where sn = sum [1..n]
______________________________
module Codewars.Kata.RemovNB where

import Data.Maybe (mapMaybe)

removNb :: Integer-> [(Integer, Integer)]
removNb n = mapMaybe f [1..n]
    where f x = (\(d, m) -> if m == 0 && d <= n then Just (x, d) else Nothing) ((n * (n+1) `div` 2 - x) `divMod` (x+1))
______________________________
module Codewars.Kata.RemovNB where

removNb :: Integer-> [(Integer, Integer)]
removNb n = [(a,b) | a <- [1..n], let (b,r) = (sn-a) `divMod` (a+1), r == 0, b <= n]
  where sn = n * (n+1) `div` 2
