5659c6d896bc135c4c00021e


module NextSmaller where 
import Data.List(sort)

nextSmaller :: Integer -> Maybe Integer
nextSmaller n = go (n-1)
          where go c 
                 | c < m || (length $ show c) < (length $ show n) = Nothing 
                 | otherwise = if helper c == m then Just c else go (c-1) 
                    where m = helper n    
                          helper n = read (take 1 zs ++ ys ++ drop 1 zs) :: Integer 
                            where zs = sort $ filter (`elem` "123456789") xs; xs = show n;  ys = filter (=='0') xs
_______________________________
module NextSmaller where 

import Data.Maybe
import Data.List

notPossible (x : xs) = let xs' = dropWhile (== '0') xs in (x : xs') == sort (x : xs')

nextSmaller :: Integer -> Maybe Integer
nextSmaller n 
  | notPossible (show n) = Nothing
  | otherwise = listToMaybe $ filter ((== sort (show n)) . sort . show) [n - 1, n - 2 .. 0]
_______________________________
module NextSmaller where 

import Data.Char (digitToInt)
import Data.List (delete, sortBy)

digits :: Integer -> [Int]
digits = map digitToInt . show

number :: [Int] -> Integer
number = read . concat . map show

mmax :: [Int] -> Maybe Int
mmax [] = Nothing
mmax x = Just (maximum x)

nxSm :: [Int] -> Maybe [Int]
nxSm (_:[]) = Nothing
nxSm [] = Nothing
nxSm (a:b:xs) = case nxSm (b:xs) of
  Just j -> Just (a:j)
  Nothing | a <= b -> Nothing
  Nothing -> (:) <$> f <*> s
    where f = mmax (filter (<a) (b:xs))
          s = (sortBy (flip compare)) <$> ((delete <$> f) <*> Just (a:b:xs))

nextSmaller :: Integer -> Maybe Integer
nextSmaller i = case (nxSm (digits i)) of
  Just (0:_) -> Nothing
  Just j -> Just (number j)
  Nothing -> Nothing
