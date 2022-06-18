59568be9cc15b57637000054

module Become.Immortal where

bitLength :: Integer -> Integer
bitLength n | n <= 0    = 0
            | otherwise = 1 + bitLength (n `div` 2)

elderAge :: Integer -> Integer -> Integer -> Integer -> Integer
elderAge m n l t
  | m < n = elderAge n m l t
  | m <= 0 || n <= 0 || l >= k' = 0
  | otherwise = (s + elderAge (m - k) r (l - k) t
                   + elderAge k (n - r) (l - k) t
                   + elderAge (m - k) (n - r) l t) `mod` t
  where 
    k' = 2 ^ bitLength m
    k = if n > 1 then k' `div` 2 else m
    r = min n k
    s = if k > l then 
          if l >= 0 then 
            (k - l) * (k - l - 1) `div` 2 * r 
          else 
            (k * (k - 1) `div` 2 - l * k) * r
        else 0          
_____________________________
module Become.Immortal where

elderAge :: Integer -> Integer -> Integer -> Integer -> Integer
elderAge m0 n0 l t = mod (f m0 n0 0) t where
  f :: Integer -> Integer -> Integer -> Integer
  f 0 _ _ = 0
  f _ 0 _ = 0
  f a b v
    | a < b = f b a v                                
    | b <= n = b * lineSum n
               + f b (a - n) (n + v)
    | otherwise = n * lineSum n
                + f (a - n) n (v + n)
                + f n (b - n) (v + n)
                + f (a - n) (b - n) v
    where                                  
      n :: Integer
      n = 2 ^ f a where
        f x | x == 1 = 0
            | x > 1 = 1 + f (x `div` 2) 

      lineSum :: Integer -> Integer
      lineSum x | v >= l  = (v-l)*x + seriesSum (x-1)
           | v + x > l - 1 = seriesSum (x+v-l-1)
           | otherwise = 0

      seriesSum :: Integer -> Integer
      seriesSum x = x * (x + 1) `div` 2 
_______________________________________
module Become.Immortal where

import qualified Data.Bits as B

infixl 7 //
(//) = div

infixl 7 %
(%) = mod

elderAge :: Integer -> Integer -> Integer -> Integer -> Integer
elderAge m0 n0 l t = mod (f m0 n0 0) t where
  f :: Integer -> Integer -> Integer -> Integer
  f 0 _ _ = 0
  f _ 0 _ = 0
  f a b v
    | a < b = f b a v                                
    | b <= nth = b * sq nth
               + f b (a - nth) (nth + v)
    | otherwise = nth * sq nth
                + f (a - nth) nth (v + nth)
                + f nth (b - nth) (v + nth)
                + f (a - nth) (b - nth) v
    where                                  
      nth = 2 ^ (floorLog2 a)

      sq :: Integer -> Integer
      sq x | v >= l  = (v-l)*x + ssum (x-1)
           | v + x > l - 1 = ssum (x+v-l-1)
           | otherwise = 0

      ssum :: Integer -> Integer
      ssum x = x * (x + 1) // 2 

      floorLog2 :: Integer -> Integer
      floorLog2 x = f x where
        f x | x == 1 = 0
            | x > 1 = 1 + f (B.rotateR x 1)
_____________________________________________
module Become.Immortal where

import Data.Bits (Bits, shift, xor)

modAdd :: Integral a => a -> a -> a -> a
modAdd m x y = (x + y) `mod` m

modSub :: Integral a => a -> a -> a -> a
modSub m x y = (x - y) `mod` m

modMul :: Integral a => a -> a -> a -> a
modMul m x y = (x * y) `mod` m

modExp :: (Integral a, Integral b) => a -> a -> b -> a
modExp m x e
  | e == 0    = 1
  | e == 1    = x
  | r == 0    = rec
  | otherwise = modMul m rec x
  where
    (q, r) = divMod e 2    
    rec    = modExp m (modMul m x x) q

double :: Integral a => a -> a
double x = x + x
    
powersOf2 :: Integral a => [a]
powersOf2 = 1 : fmap double powersOf2

pow2 :: Integral a => Int -> a
pow2 = (!!) powersOf2

decompose :: Integral a => a -> [(a, Int)]
decompose n = decompose' (reverse $ takeWhile (<= n) powersOf2) 0 n

decompose' :: Integral a => [a] -> a -> a -> [(a, Int)]
decompose' _ _ 0  = []
decompose' [] _ _ = error "got to empty list in decompose' helper function"
decompose' (p2:ps) factor n
  | p2 <= n   = (factor, length ps) : decompose' ps (double $ succ factor) (n - p2)
  | otherwise = decompose' ps (double factor) n

cartProd :: [a] -> [b] -> [(a,b)]
cartProd x y = foldl (++) [] $ fmap (\u -> fmap ((,) u) y) x

elderRect :: (Integral a, Bits a) => a -> (a, Int) -> (a, Int) -> a
elderRect l (r,a) (c,b)
  | a > b        = elderRect l (c,b) (r,a)
  | l >= hiLimit = 0
  | l < loLimit  = pow2 a * ((d `shift` (b+1) + pow2 b - 1 - l - l) `shift` (b-1))
  | otherwise    = pow2 a * (lfactor * (lfactor - 1) `div` 2)
  where
    d       = c `xor` (r `shift` (a-b))
    loLimit = d * pow2 b
    hiLimit = (d + 1) * pow2 b - 1
    lfactor = (d+1) * pow2 b - l

elderAge :: Integer -> Integer -> Integer -> Integer -> Integer
elderAge m n l t = foldl (modAdd t) 0 $ fmap (uncurry $ elderRect l) $ cartProd (decompose m) (decompose n)
____________________________________________
module Become.Immortal where

import Data.Bits
import Math.NumberTheory.Logarithms

highestBitMask 0 = 0
highestBitMask k = 2 ^ integerLog2' k

elderAge :: Integer -> Integer -> Integer -> Integer -> Integer
elderAge row col loss mo = elderAge' 0 row col
  where
    accum base row
      | row == 0 = 0
      | basePlus + row <= loss + 1 = 0 -- totally 0
      | otherwise = sum
      where
        begin = max 0 $ basePlus - loss
        end = basePlus + row - loss -1
        safeMask = row - 1 -- sort (xor safeMask <$> [0..row-1]) == [0..row-1]
        basePlus = base .&. complement safeMask
        sum = ((begin + end) * (end - begin + 1) `div` 2) `mod` mo

    a *: b = (a * b) `mod` mo
    a +: b = (a + b) `mod` mo
    a ~: b = a .&. complement b

    elderAge' base row col
      | col == 0 = 0
      | row < col = elderAge' base col row
      | otherwise =
        baseSum -- highRow * highCol
          +: elderAge' (base `xor` highRow) (row ~: highRow) highCol
          +: elderAge' (base `xor` highCol) highRow (col ~: highCol)
          +: elderAge' (base `xor` highRow `xor` highCol) (row ~: highRow) (col ~: highCol)
      where
        baseSum = highCol *: accum base highRow
        highRow = highestBitMask row
        highCol = highestBitMask col
