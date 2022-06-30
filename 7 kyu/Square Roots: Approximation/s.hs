58475cce273e5560f40000fa


module ApproxRoot where

--no rounding, just compares ~0.01 accuracy

approxRoot :: Int -> Double
approxRoot n
  | base^2 == n' = base
  | otherwise = base + (n' - base^2) / (base * 2 + 1)
  where
    n' = fromIntegral n
    base = head $ filter (\x -> x^2 <= n' && n' < (x+1)^2) [0..]
____________________________
module ApproxRoot where

--no rounding, just compares ~0.01 accuracy

approxRoot :: Int -> Double
approxRoot n 
  | base ^ 2 == dn = base
  | otherwise     = base + (dn - base ^ 2) / (above ^ 2 - base ^ 2)
  where base  = fromIntegral $ floor $ sqrt dn
        above = succ base
        dn    = fromIntegral n
____________________________
{-# LANGUAGE TupleSections #-}

module ApproxRoot where

approxRoot :: Int -> Double
approxRoot x
  | greaterRoot == lowerRoot = fromIntegral greaterRoot
  | otherwise = (+ fromIntegral differenceLower / fromIntegral difference) . fromIntegral $ lowerRoot
  where
    (lowerRoot, greaterRoot) = sqrtRange x
    greaterSquare = greaterRoot * greaterRoot
    lowerSquare = lowerRoot * lowerRoot
    difference = greaterSquare - lowerSquare
    differenceLower = x - lowerSquare

sqrtRange :: Int -> (Int, Int)
sqrtRange x
  | perfect * perfect == x = (perfect, perfect)
  | otherwise = (floor root, ceiling root)
  where
    root = sqrt . fromIntegral $ x :: Double
    perfect = round root :: Int
