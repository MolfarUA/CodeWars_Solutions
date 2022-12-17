58bc16e271b1e4c5d3000151


module LowestBaseSystem (getMinBase) where

import Data.List (find)

getMinBase :: Int -> Int
getMinBase n = maybe (n - 1) fst $ find ((== n) . snd) ns
  where x = fromIntegral n
        maxK = ceiling $ logBase 2 x
        ns = [(b, (b ^ (k + 1) - 1) `div` (b - 1)) | k <- [maxK + 1, maxK..2], let b = truncate (x ** (1 / fromIntegral k)), b >= 2]
______________________________________
module LowestBaseSystem (getMinBase) where

ones :: Int -> Integer -> Integer -> Integer
ones n b m = iterate (\i -> min (m + 1) $ i * b + 1) 0 !! n 

binarySearch :: Integral a => (a -> Bool) -> a -> a -> a
binarySearch f = go
  where
    go l r
      | l == r = r
      | f m = go l m
      | otherwise = go (m + 1) r
      where
        m = l + (r - l) `quot` 2

getMinBase :: Int -> Int
getMinBase 1 = 2
getMinBase x = fromInteger $ head
  [ b
  | n <- reverse [2 .. 31]
  , let b = binarySearch (\i -> ones n i y >= y) 2 y
  , ones n b y == y
  ]
  where
    y = toInteger x
______________________________________
module LowestBaseSystem ( getMinBase ) where

find :: (Integer -> Integer) -> Integer -> Integer -> Integer -> Integer
find f n lo hi | hi - lo == 1 = hi
               | f mi < n     = find f n mi hi
               | otherwise    = find f n lo mi
               where mi = (lo + hi) `div` 2

getMinBase' :: Integer -> Integer
getMinBase' n = minimum [x | k <- [2..m + 1], let x = find (f k) n 1 n, f k x == n]
              where f = \k x -> (x ^ k - 1) `div` (x - 1)
                    m = fromEnum $ logBase 2 $ fromIntegral n

getMinBase :: Int -> Int
getMinBase = fromIntegral . getMinBase' . fromIntegral
______________________________________
module LowestBaseSystem (getMinBase) where

import Data.Foldable (toList)

getMinBase :: Int -> Int
getMinBase v = fromInteger . head $ concatMap (\d -> toList $ binSearch 2 4 (nthDigit d) (toInteger v)) [64,63..2]


nthDigit :: Integer -> Integer -> Integer
nthDigit n b | n == 1    = 1
             | otherwise = 1 + b * nthDigit (n-1) b
             
binSearch :: Integer -> Integer -> (Integer -> Integer) -> Integer -> Maybe Integer
binSearch st fn f v | f fn <= v  = binSearch fn (fn * 2) f v
                    | f st == v = Just st
                    | fn - st <= 1 = Nothing
                    | otherwise = 
                         let
                           md = (st + fn) `div` 2 
                         in
                           if f md > v
                           then binSearch st md f v
                           else binSearch md fn f v
                    
