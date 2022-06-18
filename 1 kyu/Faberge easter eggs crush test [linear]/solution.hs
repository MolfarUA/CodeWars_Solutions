5976c5a5cd933a7bbd000029

{-# LANGUAGE BangPatterns, MagicHash, UnboxedTuples, ForeignFunctionInterface, UnliftedFFITypes #-}

module Faberge (height) where

import GHC.Exts
import GHC.Integer
import System.IO.Unsafe
import System.Process
import System.Posix.DynamicLinker

type HeightFun = Int# -> Int# -> Int#
foreign import ccall "dynamic"
  mkFun :: FunPtr HeightFun -> HeightFun

height'' :: HeightFun
height'' = unsafePerformIO $ do
  writeFile "/tmp/mod_word.c" "#include <stdio.h>\n\
\ \n\
\ const long mo = 998244353;\n\
\ \n\
\ long modinv(long a, long b) {\n\
\   long or = a, os = 1, ot = 0, r = b, s = 0, t = 1;\n\
\   long q, nr, ns, nt;\n\
\   while (r != 0) {\n\
\     q = or / r;\n\
\     nr = or - q * r;\n\
\     ns = os - q * s;\n\
\     nt = ot - q * t;\n\
\     or = r; os = s; ot = t;\n\
\     r = nr; s = ns; t = nt;\n\
\   }\n\
\   return os < 0 ? os + b : os;\n\
\ }\n\
\ \n\
\ long moddiv(long a, long b) {\n\
\   return (a * modinv(b, mo)) % mo;\n\
\ }\n\
\ \n\
\ long height(long n, long m) {\n\
\   long i = 1, num = m, dom = 1, acc = 0;\n\
\   m = m % mo;\n\
\   while (i <= n) {\n\
\     acc = (acc * i + num) % mo;\n\
\     num = (num * (m - i)) % mo;\n\
\     i   = (i + 1)         % mo;\n\
\     dom = (dom * i      ) % mo;\n\
\   }\n\
\   return moddiv((acc * i) % mo, dom);\n\
\ }"
  callCommand "gcc -c -fPIC /tmp/mod_word.c -o /tmp/mod_word.o"
  callCommand "gcc -shared -o/tmp/libmod_word.so /tmp/mod_word.o"
  lib <- dlopen "/tmp/libmod_word.so" [RTLD_LAZY]
  mkFun <$> dlsym lib "height"

-- the original solution
-- this is plenty fast if compiled (< 2 times the C above), but CW insists on interpreting it or some such
-- that makes it 2-3 seconds to slow

-- the 998244353# below isn't a constant because GHC refuses to allow 
-- binding unlifted values to top-level names for some reason.
mo = 998244353

modinv :: Int#  -> Int# -> Int#
modinv a b = makePos (go a 1# 0# b 0# 1#)
  where makePos a | isTrue# (0# <=# a) = a
                  | otherwise         = makePos (a +# b)
        go _ !os _ 0# _ _ = os
        go !or !os !ot !r !s !t = go r s t
                                     (or -# q *# r)
                                     (os -# q *# s)
                                     (ot -# q *# t)
          where q = or `quotInt#` r

moddiv :: Int# -> Int# -> Int#
a `moddiv` b = (a *# modinv b 998244353#) `remInt#` 998244353#

height' :: Int# -> Int# -> Int#
height' !n !m = go 1# m 1# 0# `remInt#` 998244353#
  where go !i !num !dom !acc | isTrue# (i ># n) =
          ((acc *# i) `remInt#` 998244353#) `moddiv` dom
                             | otherwise        =
          go ((i +# 1#) `remInt#` 998244353#)
             ((num *# (m -# i)) `remInt#` 998244353#)
             ((dom *# (i +# 1#)) `remInt#` 998244353#)
             ((acc *# i +# num) `remInt#` 998244353#)

height :: Integer -> Integer -> Integer
height n m = smallInteger (height'' (integerToInt n) (integerToInt (m `mod` mo)))
__________________________________________________
module Faberge (height) where

import Data.List
import GHC.Integer.GMP.Internals (recipModInteger)

mo = 998244353

madd a b
    | s >= mo = s - mo
    | otherwise = s
    where s = a + b

mmul a b = a * b `mod` mo

msum = foldl' madd 0

factInvs = scanl' mmul 1 $ (`recipModInteger` mo) <$> [1 ..]

height n m = msum (take (n' + 1) $ zipWith mmul falling factInvs) - 1
    where
        falling = scanl' mmul 1 [m, m - 1 ..]
        n' = fromInteger n
__________________________________________________
module Faberge where

mo = 998244353

height :: Integer -> Integer -> Integer
height n m
  | n * m == 0       = 0
  | otherwise        = sub 0 1 flipFactorials 0
  where
    cut = 998244353
    flipFactorials = scanr1 (\x y -> x * y `mod` cut) [2..n] ++ [1]
    inverseBaseFact = invert $ head flipFactorials
    invert num = ((((num^349 `mod` cut)^281 `mod` cut)^29 `mod` cut)^13 `mod` cut)^27 `mod` cut
    sub height fSum fFacts k
      | k == n - 1 = (newFSum * inverseBaseFact * head fFacts + height) `mod` cut
      | otherwise  = sub ((newFSum * inverseBaseFact * head fFacts + height) `mod` cut) newFSum (tail fFacts)  (k + 1)
      where
        newFSum = (m - k) * fSum `mod` cut
__________________________________________________
module Faberge where

import Data.Vector (Vector, generate, (!))
import GHC.Integer.GMP.Internals

height :: Integer -> Integer -> Integer
height n m = let m' = m `rem` mo in sum (scanl (\b k -> b * (m' - k) * (invs ! fromIntegral k) `rem` mo) m' [1 .. n - 1]) `rem` mo

mo :: Integer
mo = 998244353

invs :: Vector Integer
invs = generate 80000 (\i -> recipModInteger (fromIntegral i + 1) mo)

__________________________________________________
module Faberge where

mo :: Integral a => a
mo = 998244353

modinv :: Integral a => a -> a -> a
modinv _ 0 = error "not invertible"
modinv _ 1 = 1
modinv m a = let y = modinv a (m `mod` a) in (m * (a-y) + 1) `div` a

-- n = # eggs, m = # throws
height :: Integer -> Integer -> Integer
height n m
  | n <= 0    = 0
  | m <= 0    = 0
  | n > m     = height m m
  | otherwise = (rowSum n 0 m (pred m) 2) `mod` mo

-- partial sums m'th row of Pascal's triangle, skipping the initial 1
rowSum :: Integral a => a -> a -> a -> a -> a -> a
rowSum remain accum cur numer denom
  | remain == 0 = accum
  | otherwise   = rowSum (pred remain) (accum + cur) (cur * numer * modinv mo denom `mod` mo) (pred numer) (succ denom)
