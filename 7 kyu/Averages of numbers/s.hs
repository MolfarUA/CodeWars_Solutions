module Kata where

averages :: Maybe [Double] -> [Double]
averages = maybe [] (\xs -> zipWith (\a b -> (a+b)/2) xs (tail xs))
____________________________
module Kata where

averages :: Maybe [Double] -> [Double]
averages Nothing          = []
averages (Just [])        = []
averages (Just [_])       = []
averages (Just (x:y:xs))  = (x + y) / 2 : averages (Just $ y:xs)
____________________________
module Kata where

averages :: Maybe [Double] -> [Double]
averages = maybe [] $ zipWith (\a b -> (a + b) / 2) <*> tail
____________________________
module Kata where

averages :: Maybe [Double] -> [Double]
averages Nothing   = []
averages (Just xs) = zipWith avg xs (tail xs)
  where
    avg a b = (a + b) / 2
____________________________
module Kata where

averages :: Maybe [Double] -> [Double]
averages = maybe [] (\xs -> zipWith (((/ 2) .) . (+)) xs (tail xs))
