59c5d0b0a25c8c99ca000237


{-# LANGUAGE TupleSections #-}
module IsThatALine (line) where
import Data.Maybe
import Data.List
import Control.Monad
import Control.Applicative

f<?>xs = if null xs then[]else((,0)<$>findIndices f(head xs))++(((+1)<$>)<$>f<?>tail xs)

line :: [[Char]] -> Bool
line g=isJust$msum$mfilter(null.((/=' ')<?>g\\))<$>r[]<$>(=='X')<?>g where
  (x,y)!xs=(g!!y!!x)`elem`xs
  r p c@(x,y)=guard(length s==1)>>let (n:_)=s in (guard(n!"X")>>return(n:c:p))<|>r(c:p)n
    where s=[q|q@(a,b)<-[(x+1,y),(x-1,y),(x,y+1),(x,y-1)],a`elem`[0..(length$head g)-1]&&b`elem`[0..length g-1],q`notElem`p,q!(if a/=x then"-+X"else"|+X"),null p||(c!"+")/=((a==x)==(x==fst(head p)))]
_______________________________________
module IsThatALine (line) where

import qualified Data.Map as M (Map,fromList,toList,delete,empty)

line :: [[Char]] -> Bool
line grid = foldl (||) (False).map (\(x,y) -> isLine (x,y) (check0 (x,y)) (M.delete (x,y) path)) $ ends
  where path = M.fromList.filter ((/=' ').snd) $ [((j,i), grid !! i !! j) | i<-[0..length grid - 1], j<-[0..length (head  grid) - 1]]
        ends = map fst.filter ((=='X').snd).M.toList $ path
        check0 (x,y) = \((x',y'),d') -> case d' of
          '-' -> y' == y && abs (x'-x) == 1
          '|' -> x' == x && abs (y'-y) == 1
          _ -> abs (x'-x) + abs (y'-y) == 1
        isLine _ _ path | path == M.empty = True
        isLine (x,y) d path = if length neighbours == 1 then isLine (x',y') d'' (M.delete (x',y') path) else False
          where neighbours = filter d.M.toList $ path
                [((x',y'),d')] = neighbours
                d'' = case d' of
                  'X' -> \((a,b),_) -> abs (a-x') + abs (b-y') == 1
                  '-' -> \((a,b),_) -> b == y' && abs (a-x') == 1
                  '|' -> \((a,b),_) -> a == x' && abs (b-y') == 1
                  '+' -> \((a,b),_) -> if abs (x-x') == 1 then a == x' && abs (b-y') == 1 else b == y' && abs (a-x') == 1
_______________________________________
{-# LANGUAGE TupleSections #-}

module IsThatALine (line) where
import Data.Array

line :: [[Char]] -> Bool
line xs = case pts of [start, end] -> walk asArray end start (0, 0) || walk asArray start end (0, 0)
  where (rows, cols) = (length xs - 1, length (head xs) - 1)
        asArray = array ((0, 0), (rows, cols)) [((i, j), xs !! i !! j) | i <- [0..rows], j <- [0..cols]]
        pts = (\(r, row) -> fmap ((r,) . fst) $ filter ((== 'X') . snd) $ zip [0..] row) =<< zip [0..] xs
        
        walk :: Array (Int, Int) Char -> (Int, Int) -> (Int, Int) -> (Int, Int) -> Bool
        walk arr target (i, j) (di, dj) | (i, j) == target  = foldr ((&&) . (== ' ')) True newArr
                                        | i < 0 || i > rows ||
                                          j < 0 || j > cols = False
                                        | otherwise         = case segs of [(i', j')] -> go (i', j')
                                                                           _          -> False
                           where c      = arr ! (i, j)
                                 isInBounds (r, c) = r >= 0 && c >= 0 && r <= rows && c <= cols
                                 nexts  = filter isInBounds $ 
                                          case c of
                                            ' ' -> []
                                            'X' -> [(i', j) | i' <- [i+1, i-1], isInBounds (i', j), newArr ! (i', j) `elem` "|+X"]
                                                   ++ [(i, j') | j' <- [j+1, j-1], isInBounds (i, j'), newArr ! (i, j') `elem` "-+X"]
                                            '+' -> [(i+dj, j+di), (i-dj, j-di)]
                                            '-' -> [(i, j+1), (i, j-1)]
                                            '|' -> [(i+1, j), (i-1, j)]
                                 segs  = filter ((/= ' ') . (newArr !)) nexts
                                 newArr = arr // [((i, j), ' ')]
                                 go (i', j') = walk newArr target (i', j') (i'-i, j'-j)
