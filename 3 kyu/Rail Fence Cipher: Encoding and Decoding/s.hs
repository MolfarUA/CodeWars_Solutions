58c5577d61aefcf3ff000081


module RailFenceCipher.Kata (encode,decode) where
import Data.List

encode :: [a] -> Int -> [a]
encode str n = map snd . sortOn fst $ zip (cycle ([1..n] ++ [n-1,n-2..2])) str

decode :: [a] -> Int -> [a]
decode str n = map snd . sortOn fst $ zip (encode [1..length str] n) str
_____________________________
module RailFenceCipher.Kata (encode,decode) where

import Data.Ord
import Data.List

upDown n = cycle $ [1 .. n-1] ++ [n, n-1 .. 2]
extr xs ys = map fst $ sortBy (comparing snd) $ zip xs ys

encode :: [a] -> Int -> [a]
encode xs n = extr xs (upDown n)

decode :: [a] -> Int -> [a]
decode xs n = extr xs (encode [1..length xs] n)
_____________________________
module RailFenceCipher.Kata (encode,decode) where

encode :: [a] -> Int -> [a]
encode s m = concat [[s !! (i-1) | i <- [1..n], (i-j)`mod`(2*m-2)==0 || (i-2*m+j)`mod`(2*m-2)==0] | j <- [1..m]]
    where n = length s

decode :: [a] -> Int -> [a]
decode [] m = []
decode s m = decode (take p s ++ drop (p+1) s) m ++ [s!!p]
      where p = lastCharPlace m $ length s

lastCharPlace :: Int -> Int -> Int
lastCharPlace m n | r==0 = 3*k - 1
                  | r==m = n - 1
                  | r>m = (2*k+1)*(2*m-r) - k
                  | otherwise = 2*k*r + r - k - 1
                  where (k, r) = n `divMod` (2*m-2)
_____________________________
module RailFenceCipher.Kata (encode,decode) where

import Data.List (sort)

railPos :: Int -> Int -> [Int]
railPos n i | i == 0 = [0, (n-1)*2..]
            | i == n-1 = [n-1, (n-1)*3..]
            | otherwise = alternate [i, i+(n-1)*2..] [(n-1)*2-i, (n-1)*4-i..]
    where alternate (x:xs) (y:ys) = x : y : alternate xs ys

encode :: [a] -> Int -> [a]
encode s n = map (s !!) (pos (length s) n)

pos :: Int -> Int -> [Int]
pos len n = concat [takeWhile (< len) (railPos n r) | r <- [0..n-1]]

pos' :: Int -> Int -> [Int]
pos' len n = map snd $ sort $ pos len n `zip` [0..]

decode :: [a] -> Int -> [a]
decode s n = map (s !!) (pos' (length s) n)
