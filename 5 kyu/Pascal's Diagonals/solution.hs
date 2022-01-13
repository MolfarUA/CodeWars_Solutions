module PascalsDiagonals (generateDiagonal) where

generateDiagonal :: Int -> Int -> [Int]
generateDiagonal n l = take l $ scanl (\c i -> c * (n + i) `div` i) 1 [1..]
_______________________________
module PascalsDiagonals (generateDiagonal) where

walk :: Int -> Int -> Int -> Int -> [Int]
walk n l last pos 
  | l <= 0 = []
  | otherwise = (last : next) 
    where
      next = walk n (pred l) (last * (n + pos) `div` pos) (succ pos)

generateDiagonal :: Int -> Int -> [Int]
generateDiagonal n l = walk n l 1 1
_______________________________
module PascalsDiagonals (generateDiagonal) where

generateDiagonal :: Int -> Int -> [Int]
generateDiagonal n l = take l $ pascal !! n

pascal :: [[Int]]
pascal = scanl1 (+) `iterate` repeat 1
