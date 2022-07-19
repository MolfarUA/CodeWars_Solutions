5573f28798d3a46a4900007a


{-# LANGUAGE TupleSections #-}
module Kata.GetToTheChoppa where

import           Data.Foldable                  ( asum
                                                , foldl'
                                                )
import           Data.List                      ( intercalate )
import qualified Data.Map                      as Map
import           Data.Map.Lazy                  ( Map
                                                , alter, insert
                                                )
import           Data.Maybe                     ( fromMaybe )
import qualified Data.Sequence                 as Seq
import           Data.Sequence                  ( Seq(..)
                                                , (|>)
                                                )
import           Data.Vector                    ( (!)
                                                , Vector
                                                , fromList
                                                )
import qualified Data.Vector                   as V

type Pos = (Int, Int)
data Node = Passable | NotPassable deriving (Eq, Show)
type Grid = [[Node]]
type Grid' = Vector (Vector Node)
type Path = [Pos]

getNode :: Pos -> Grid' -> Node
getNode (x, y) grid = grid ! y ! x

neighboringNodes :: Pos -> Grid' -> [Pos]
neighboringNodes (x0, y0) g =
    [ p | p <- [(x0 + 1, y0), (x0 - 1, y0), (x0, y0 + 1), (x0, y0 - 1)], fst p >= 0, fst p < width, snd p >= 0, snd p < height, getNode p g == Passable ]
  where
    height = V.length g
    width  = V.length (g ! 0)

shortestPath :: Grid -> Pos -> Pos -> Path
shortestPath []              _ _ = []
shortestPath [[Passable   ]] _ _ = [(0, 0)]
shortestPath [[NotPassable]] _ _ = []
shortestPath g               s e = go Map.empty (Seq.singleton (0, s))
  where
    go :: Map Pos (Int, Pos) -> Seq (Int, Pos) -> Path
    go mp Empty              = rollup e [] (snd <$> mp)
    go mp se@((cost, p) :<| ps) = go
        (foldl' (\mp' q -> insert q (cost + 1, p) mp') mp ns)
        (foldl' (|>) ps ((cost + 1, ) <$> ns))
        where ns = [ no | no <- neighboringNodes p g', maybe True ((> cost + 1) . fst) (Map.lookup no mp) ]
    rollup :: Pos -> Path -> Map Pos Pos -> Path
    rollup p path mp | p == s = p : path
                     | otherwise = rollup (fromMaybe (error "rollup") (Map.lookup p mp)) (p : path) mp
    g' = fromList (fromList <$> g)
__________________________________
module Kata.GetToTheChoppa where

import Data.Array.IArray
import Data.Array.MArray
import Data.Array.ST
import Data.List
import Control.Monad
import Control.Monad.ST

type Pos = (Int, Int)
data Node = Passable | NotPassable deriving (Show, Eq)
-- A grid is a list of list of nodes, which are Passable / NotPassable
type Grid = [[Node]]
type Path = [Pos]

type AGrid = Array Int (Array Int Node)
type IGrid = Array Int (Array Int Int)
type SIGrid s = Array Int (STUArray  s Int Int)

toAGrid :: Grid -> AGrid
toAGrid grid =  listArray (0, h) $ map (listArray (0, w)) grid
    where l = length grid
          h = l - 1
          w = if l == 0
                  then -1
                  else length (head grid) - 1

shortestPath :: Grid -> Pos -> Pos -> Path
shortestPath grid = scan $ toAGrid grid

scan :: AGrid -> Pos -> Pos -> Path
scan a start end
    | uncurry (-) (bounds a) > 0 = []
    | end == start = pure start
    | otherwise =
        let a' = runST $ do
                a'' <- listArray (0, h) <$>
                    mapM (const $ newArray (0, w) 0) [0 .. h] ::
                        ST s (SIGrid s)
                bfs a a'' [start] 1
                mapM freeze a''
        in backtrack a' end []
    where (h, w) = (snd $ bounds a, snd $ bounds $ a ! 0)
          bfs :: AGrid -> SIGrid s -> [Pos] -> Int -> ST s ()
          bfs _ _ [] _ = return ()
          bfs ia ma p acc = do
              mapM_ (\(x, y) -> writeArray (ma ! y) x acc) p
              ch <- filterM
                  (\(x, y) -> do
                      visited <- readArray (ma ! y) x
                      return $ ia ! y ! x == Passable && visited == 0
                  ) $ uniq $ concatMap (children (h, w)) p
              bfs ia ma ch $ acc + 1
          backtrack :: IGrid -> Pos -> [Pos] -> [Pos]
          backtrack ia p@(x, y) acc =
              let i = ia ! y ! x
              in if i == 0
                     then acc
                     else if i == 1
                              then p : acc
                              else let ch = children (h, w) p
                                       next = head $
                                           filter (\(x', y') ->
                                                       ia ! y' ! x' == i - 1
                                                  ) ch
                                   in backtrack ia next $ p : acc
          uniq = map head . group . sort

children:: (Int, Int) -> Pos -> [Pos]
children (m, n) (y, x) =
    filter (\(a, b) -> a >= 0 && a <= n && b >= 0 && b <= m)
        [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
__________________________________
module Kata.GetToTheChoppa where
import Data.List 

type Pos = (Int,Int)
data Node = Passable | NotPassable deriving (Eq, Show)
type Grid = [[Node]]
type Path = [Pos]

neighbors :: Grid -> Pos -> Int -> Int -> [Pos]
neighbors grid (a,b) m n = filter (\(x,y)->x >= 0 && y >= 0 && x < m && y < n && (grid !! y !! x == Passable)) [(a+1,b), (a-1,b), (a,b+1), (a,b-1)]

block p q = before ++ [NotPassable] ++ after
    where (before, _:after) = splitAt p q

blockPath :: Grid -> Int -> Int -> Grid
blockPath g x y = map (\(a,b) -> if (a == y) then (block x b) else b) $ zip [0..] g

parsePath :: [Pos] -> Grid -> Int -> Int -> [[Pos]] -> ([[Pos]], Grid)
parsePath p g m n pa
  | neigh == [] = (pa, g)
  | otherwise = foldl (\(a,b) nb -> ((nb:p):a,blockPath b (fst nb) (snd nb))) (pa, g) neigh
  where h = head p
        neigh = neighbors g h m n

findPath :: [[Pos]] -> Grid -> Int -> Int -> Pos -> [Pos]
findPath paths grid m n target
  | not (null winners) = reverse $ head winners
--  | length paths > 0 && length (paths !! 0) > 1 = paths !! 0
  | paths == [] = []
  | otherwise = findPath newPaths newGrid m n target
  where winners = filter (\x -> target == head x) paths
        (newPaths, newGrid) = foldl (\(p,g) pa -> parsePath pa g m n p) ([], grid) paths
shortestPath :: Grid -> Pos -> Pos -> Path
--shortestPath grid st en = blockPath grid 0 1 
shortestPath grid st en 
  | grid == [] = []
--  | otherwise = head . fst $ foldl (\(p,g) pa -> parsePath pa g (length $ grid !! 0) (length grid) p) ([], newGrid) [[(0,2), (0,1), (0,0)]]
  | otherwise = findPath [[st]] newGrid (length $ grid !! 0) (length grid) en
  where newGrid = blockPath grid (fst st) (snd st) 
__________________________________
{-# LANGUAGE LambdaCase #-}
module Kata.GetToTheChoppa where

import qualified Data.List as L (nubBy)
import qualified Data.Vector as V (Vector,fromList,(!?),(!),(//))

type Pos = (Int,Int)
data Node = Passable | NotPassable deriving (Eq, Show)
type Grid = [[Node]]
type Path = [Pos]

shortestPath :: Grid -> Pos -> Pos -> Path
shortestPath [] _ _ = []
shortestPath grid s e = (\(Just p) -> p) $ (findPaths grid' [[e]]) V.! (snd s) V.! (fst s)
  where grid' = (\v -> v V.// [(snd e,(v V.! (snd e)) V.// [(fst e,Just [e])])]).
                V.fromList.map V.fromList.
                map (map (\case Passable -> Just []; _ -> Nothing;))
                $ grid

findPaths :: V.Vector (V.Vector (Maybe Path)) -> [Path] -> V.Vector (V.Vector (Maybe Path))
findPaths g [] = g
findPaths g l = findPaths g' l'
  where l' = L.nubBy (\(a:_) -> \(b:_) -> a==b).concat.map (neighbours g) $ l
        tmp = map (\p -> (head p,Just p)) l'
        g' = g V.// [(i,(g V.! i) V.// (map (\((x,_),p) -> (x,p)).filter (\((_,y),_) -> y==i) $ tmp)) | i <- [0..length g - 1]]  
    
neighbours :: V.Vector (V.Vector (Maybe Path)) -> Path -> [Path]
neighbours g (p@((x,y):_)) = map (\(Just (a,Just b)) -> a:p).
                     filter (\case (Just (_,Just [])) -> True; _ -> False).
                     map (\(i,j) -> (\a -> ((i,j),a)) <$> ((g V.!? j) >>= (V.!? i)))
                     $ [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
