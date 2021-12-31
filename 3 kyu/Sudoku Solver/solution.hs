module Sudoku where
import Data.Array.IArray

sudoku :: [[Int]] -> [[Int]]
sudoku = toLists . elems . (\(Just a)->a) . solve 0 0 . listArray ((0,0), (8,8)) . concat

solve :: Int -> Int -> Array (Int, Int) Int -> Maybe (Array (Int, Int) Int)
solve 8 9 a = Just a
solve x 9 a = solve (x + 1) 0 a
solve x y a | a ! (x, y) /= 0 = solve x (y + 1) a
solve x y a = trySolve [1..9]
    where
    trySolve [] = Nothing
    trySolve (c:cs) = case verify c of
        Nothing -> trySolve cs
        a'      -> a'
    
    verify c = if (hor c && ver c && sqr c) then solve x (y + 1) (a // [((x, y), c)]) else Nothing
    hor c = not . any ((== c) . (a !)) . filter (\(i,_) -> i == x) $ indices a
    ver c = not . any ((== c) . (a !)) . filter (\(_,j) -> j == y) $ indices a
    sqr c = not . any ((== c) . (a !)) . filter (\(i,j) -> (div i 3 == div x 3) && (div j 3 == div y 3)) $ indices a

toLists [] = []
toLists xs = let (a, b) = splitAt 9 xs in a : toLists b

___________________________________________________
module Sudoku where

import Data.List 


sudoku x = head $ solve x 


type Grid = Matrix Value 
type Matrix a = [Row a]
type Row a = [a]
type Value = Int 

boxsize              :: Int
boxsize               =  3

values                :: [Value]
values                =  [1..9]

empty                 :: Value -> Bool
empty                 =  (== 0)

single                :: [a] -> Bool
single [_]            =  True
single _              =  False


blank :: Grid 
blank = replicate 9 (replicate 9 0)

rows :: Matrix a -> [Row a]
rows = id 

cols :: Matrix a -> [Row a]
cols = transpose 

boxs :: Matrix a -> [Row a]
boxs =  unpack . map cols . pack
     where
    pack   = split . map split                           
    split  = chop boxsize
    unpack = map concat . concat

chop  :: Int -> [a] -> [[a]]
chop n [] =  []
chop n xs =  take n xs : chop n (drop n xs)


valid :: Grid -> Bool 
valid g =  all nodups (rows g) && 
           all nodups (cols g) &&
           all nodups (boxs g)
           where 
           nodups :: Eq a => [a] -> Bool 
           nodups [] = True 
           nodups (x:xs) = (not (elem x xs)) && nodups xs 


type Choices = [Value]

choices :: Grid -> Matrix Choices 
choices g = map (map choice) g
          where 
            choice v = if v == 0 then 
                          [1..9]
                       else 
                         [v]

cp :: [[a]] -> [[a]]
cp [] =  [[]]
cp (xs:xss) =  [y:ys | y <- xs, ys <- cp xss]

collapse :: Matrix [a] -> [Matrix a]
collapse =  cp . map cp



prune                 :: Matrix Choices -> Matrix Choices
prune                 =  pruneBy boxs . pruneBy cols . pruneBy rows
                       where pruneBy f = f . map reduce . f

reduce                :: Row Choices -> Row Choices
reduce xss            =  [xs `minus` singles | xs <- xss]
                          where singles = concat (filter single xss)

minus                 :: Choices -> Choices -> Choices
xs `minus` ys         =  if single xs then xs else xs \\ ys


solve                :: Grid -> [Grid]
solve               =  filter valid . collapse . fix prune . choices

fix                   :: Eq a => (a -> a) -> a -> a
fix f x               =  if x == x' then x else fix f x'
                     where x' = f x

___________________________________________________
module Sudoku where
import Data.List
import Data.List.Split

complete :: [[Int]] -> Bool
complete = all $ all (/=0)

boxes :: [[Int]] -> [[Int]]
boxes x = chunksOf 9 $ concat $ concat $ transpose $ map (chunksOf 3) x

possible :: [[Int]] -> Int -> Int -> [Int]
possible s x y 
  | s!!y!!x /= 0 = []
  | otherwise = [1..9] \\  s!!y `union` (transpose s!!x) `union` (boxes s !! (y `div` 3 + (3 * (x `div` 3))))

updatePossible :: [[Int]] -> [[Int]]
updatePossible s = go 0 0 s
  where
    go x y new_s
      | x == 9 = new_s
      | y == 9 = go (x+1) 0 new_s
      | otherwise = go x (y+1) (substitute new_s x y)
      
substitute :: [[Int]] -> Int -> Int -> [[Int]]
substitute s x y
  | length pos == 1 = s !!= (y, (s!!y !!= (x, (head pos))))
  | otherwise = s
    where pos = possible s x y

-- !!= update list element at index
(!!=) :: [a] -> (Int, a) -> [a]
(!!=) a (b,c) = combine c (splitAt b a)
    where
        combine :: a -> ([a],[a]) -> [a]
        combine _ (_,[]) = []
        combine a (b,_:cs) = b ++ [a] ++ cs

sudoku :: [[Int]] -> [[Int]]
sudoku = until complete updatePossible

___________________________________________________
module Sudoku where
import Data.List
import Data.List.Split

hasEmpty :: [[Int]] -> Bool
hasEmpty s = 0 `elem` (concat s)

boxes :: [[Int]] -> [[Int]]
boxes x = chunksOf 9 $ concat $ concat $ transpose $  map (chunksOf 3) x

possible :: [[Int]] -> Int -> Int -> [Int]
possible s x y 
  | (s !! y) !! x /= 0 = []
  | otherwise = [1..9] \\  ((s !! y) `union` (transpose s !! x) `union` (boxes s !! (y `div` 3 + (3 * (x `div` 3)))))

updatePossible :: [[Int]] -> [[Int]]
updatePossible s = go 0 0 s
  where
    go x y new_s
      | x == 9 = new_s
      | y == 9 = go (x+1) 0 new_s
      | otherwise = go x (y+1) (substitute new_s x y)
      
substitute :: [[Int]] -> Int -> Int -> [[Int]]
substitute s x y
  | length pos == 1 = s !!= (y, ((s !! y) !!= (x, (head pos))))
  | otherwise = s
    where pos = possible s x y

(!!=) :: [a] -> (Int, a) -> [a]
(!!=) a (b,c) = combine c (splitAt b a)
    where
        combine :: a -> ([a],[a]) -> [a]
        combine _ (_,[]) = []
        combine a (b,_:cs) = b ++ [a] ++ cs

sudoku :: [[Int]] -> [[Int]]
sudoku s
  | hasEmpty s = sudoku $ updatePossible s
  | otherwise = s
  
___________________________________________________
module Sudoku where
import Data.List

sudoku :: [[Int]] -> [[Int]]
sudoku s = res 0 0 s
  where horizontals l = l
        verticals l = transpose l
        smallBoxes l nl | null l = reverse nl
                        | null (head l) = smallBoxes (drop 3 l) nl
                        | otherwise = smallBoxes (map (drop 3) (take 3 l) ++ drop 3 l) (concatMap (take 3) (take 3 l):nl)
        isNotZero l = all (notElem 0) l
        getBox x y = 3*div y 3+div x 3
        changeNum x y l = tail $ sort $ nub $ mconcat $ (verticals l!!x):(horizontals l!!y):((smallBoxes l [])!!getBox x y):[]
        addNum l = head $ [1..9] \\ l
        newL x y l n = take y l ++ [take x (l!!y)++ [n] ++ drop (x+1) (l!!y)] ++ drop (y+1) l
        res x y l
          | y == 9 && isNotZero l = l
          | y == 9 && not (isNotZero l) = res 0 0 l
          | x == 9 = res 0 (y+1) l
          | l!!y!!x /= 0 = res (x+1) y l
          | l!!y!!x == 0 &&
            length (changeNum x y l) /= 8 = res (x+1) y l
          | l!!y!!x == 0 &&
            length (changeNum x y l) == 8 = res 0 0 (newL x y l (addNum (changeNum x y l)))
