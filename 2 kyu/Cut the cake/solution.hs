module Kata.Cut.Cake (cut) where

type CakeCut = ((Int, Int), (Int, Int))

cut :: String -> [String]
cut cake = reverse $ map (unlines . cutToPieces) $ 
    cutDaCake [[]] raisins
  where
    raisins = length $ filter (=='o') cake
    height = length actCake
    width = length (head actCake)
    cutSize = height * width `div` raisins
    actCake = lines cake
    cutToPieces :: CakeCut -> [String]
    cutToPieces ((y, x), (y', x'))
      | y > y'    = []
      | otherwise = drop x (take (x' + 1) (actCake !! y)) : cutToPieces ((y + 1, x), (y', x'))
    pieces :: (Int, Int) -> [CakeCut] -> [CakeCut]
    pieces (y,x) taken = [((y, x), (y', x')) | y' <- [y..height-1], x' <- [x..width-1],
        (y' - y + 1) * (x' - x + 1) == cutSize,
        containsRaisins y x y' x' [] == 1,
        notTaken y x x' taken]
    containsRaisins :: Int -> Int -> Int -> Int -> String -> Int
    containsRaisins y x y' x' some
      | null some && y > y' = 0
      | null some           = containsRaisins (y + 1) x y' x' (drop x (take (x' + 1) (actCake !! y)))
      | otherwise           = (if head some == 'o' then 1 else 0) + containsRaisins y x y' x' (tail some)
    notTaken :: Int -> Int -> Int -> [CakeCut] -> Bool
    notTaken y x x' taken = not (any (\((_, tx), (_, tx')) -> x <= tx && tx <= x' || tx <= x && x <= tx')
        (filter ((>=y) . fst . snd) taken))
    corners = [(y, x) | y <- [0..height-1], x <- [0..width-1]]
    cutDaCake :: [[CakeCut]] -> Int -> [CakeCut]
    cutDaCake soFarTaken m
      | m == 0    = if null soFarTaken then [] else head soFarTaken
      | otherwise = cutDaCake (findNewPiece soFarTaken) (m - 1)
      where
        findNewPiece :: [[CakeCut]] -> [[CakeCut]]
        findNewPiece list = concatMap (\taken -> [piece:taken | piece <- pieces (next taken) taken]) list
          where
            next taken = head $ filter (\(y, x) -> notTaken y x x taken) corners
            
_____________________________________________________
module Kata.Cut.Cake (cut) where

import qualified Data.Set as S (Set,fromList,elemAt,member,difference)

cut :: String -> [String]
cut cake' = if null sols then [] else head $ sols
  where (nx,ny) = (length.words $ cake',length.head.words $ cake')
        cake = map (flip divMod ny.fst).filter ((=='o').snd).zip [0..].filter (/='\n') $ cake'
        n = length cake
        a = nx*ny `div` n
        rs = recs 1
        recs k | k^2>=a = if k^2==a then [(k,k)] else []
               | True = let (k',r) = a `divMod` k in if r==0 then (k,k'):(k',k):recs (k+1) else recs (k+1) 
        f s k l | k==n = map reverse [l]
                | True = concat [f (S.difference s (S.fromList [(x+i,y+j) | i<-[0..dx-1], j<-[0..dy-1]])) (k+1) (((x,y),(dx,dy)):l)| (dx,dy)<-rs']
          where (x,y) = S.elemAt 0 s
                rs' = filter (fit s (x,y)) rs
        fit s (x,y) (dx,dy) = c1 && c2
          where c1 = and.map (flip S.member s) $ [(x+i,y+j) | i<-[0..dx-1], j<-[0..dy-1]]
                c2 = (==1).length.filter (\(a,b) -> x<=a && a<x+dx && y<=b && b<y+dy) $ cake
        sols = map (map (\((x,y),(dx,dy)) -> concat [[cake' !! (i*(ny+1)+j) | j<-[y..y+dy-1]] ++ "\n" | i<-[x..x+dx-1]])) $
               f (S.fromList [(i,j) | i<-[0..nx-1], j<-[0..ny-1]]) 0 []

_____________________________________________________
{-# LANGUAGE TupleSections #-}
module Kata.Cut.Cake (cut) where

import qualified Data.Array as Array
import qualified Data.Set as Set
import qualified Data.List as List
import qualified Data.Maybe as Maybe
import qualified Data.List.Split as Split
import Data.Array((//), (!))

cut :: String -> [String]
cut cake = if areaMod == 0
         then case place Set.empty [] (Array.indices board) pieceCount of
                (Just pieces) -> map (showBoard . cutBoard board) pieces
                Nothing -> []
         else []
  where board = parseBoard cake
        raisins = Set.fromList $ map fst $
          filter ((==CellRaisin) . snd) $ Array.assocs board
        area =
          let (_, (lastRow, lastCol)) = Array.bounds board
           in (lastRow+1)*(lastCol+1)
        pieceCount = Set.size raisins
        (pieceArea, areaMod) = area `divMod` pieceCount
        sizes = map (\v -> (v, pieceArea `div` v)) $ divisors pieceArea
        place _ pieces _ 0 = Just $ reverse pieces
        place _ _ [] _ = Nothing
        place seen pieces (p:ps) cnt =
          let posRect = makeRectangle p (1,1)
           in if noIntersections pieces posRect
             then let cands = Maybe.mapMaybe ((\rect ->
                       if canPlace pieces rect
                          then (rect,) <$> singleRaisin seen rect
                          else Nothing) . makeRectangle p) sizes
                   in case Maybe.mapMaybe (\(rect, raisin) -> place (Set.insert raisin seen) (rect:pieces) ps (cnt-1)) cands of
                        (v:_) -> Just v
                        [] -> Nothing
             else place seen pieces ps cnt
        singleRaisin seen rect =
          let cutRaisins = filter (rectanglesIntersect rect . flip makeRectangle (1, 1)) $ Set.toList raisins
           in if (length cutRaisins == 1) && not (Set.member (head cutRaisins) seen)
                 then Just $ head cutRaisins
                 else Nothing
        canPlace pieces rect =
          let (_, (lastRow, lastCol)) = Array.bounds board
              (rectBottom, rectRight) = rectangleBottomRight rect
           in rectBottom <= lastRow && rectRight <= lastCol && noIntersections pieces rect
        noIntersections targets rect =
          all (not . rectanglesIntersect rect) targets

type Vect = (Int, Int)

data Rectangle = Rectangle Vect Vect

data Cell = CellEmpty | CellRaisin
  deriving Eq

makeRectangle posTopLeft@(row, col) (height, width) =
  Rectangle posTopLeft (row+height-1, col+width-1)
rectangleBottomRight (Rectangle _ posBottomRight) = posBottomRight

parseBoard :: (Integral a, Array.Ix a) => String -> Array.Array (a, a) Cell
parseBoard board =
  let ls = lines board
      height = fromIntegral $ length ls
      width = maybe 0 (fromIntegral . length . fst) $ List.uncons ls
   in if height > 0 && width > 0
         then Array.listArray ((0, 0), (height-1, width-1)) $
           map (\v -> if v == 'o' then CellRaisin else CellEmpty) $ concat ls
         else Array.listArray ((0, 0), (0, 0)) [CellEmpty]

showBoard :: (Integral a) => Array.Array (a, a) Cell -> String
showBoard board =
  let (_, (_, lastCol)) = Array.bounds board
   in List.intercalate "\n" (Split.chunksOf (fromIntegral $ lastCol+1) $
     map showCell $ Array.elems board) ++ ['\n']
       where showCell CellEmpty = '.'
             showCell CellRaisin = 'o'

cutBoard :: Array.Array (Int, Int) Cell -> Rectangle -> Array.Array (Int, Int) Cell
cutBoard board (Rectangle (rb, cb) (re, ce)) =
  let res = Array.listArray ((0, 0), (re-rb, ce-cb)) $ repeat CellEmpty
   in res // map (\idx@(r, c) -> (idx, board!(rb + r, cb + c))) (Array.indices res)

rectanglesIntersect :: Rectangle -> Rectangle -> Bool
rectanglesIntersect (Rectangle (rb1, cb1) (re1, ce1)) (Rectangle (rb2, cb2) (re2, ce2)) =
  intersect (rb1, re1) (rb2, re2) && intersect (cb1, ce1) (cb2, ce2)
    where intersect (b1, e1) (b2, e2) =
            let s1 = signum (e2-b1)
                s2 = signum (b2-e1)
             in s1 /= s2 || s1 == 0

divisors val = List.sort $ concatMap (\v -> List.nub [v, val `div` v]) $
  filter ((==0) . (val`mod`)) $ takeWhile ((<=val) . (^2)) [1..]
_____________________________________________________
module Kata.Cut.Cake (cut) where
import Data.List
cut :: String -> [String]
cut cake
 | null cake||r==0||mod (m*n) r/=0||null solution = [] -- special cases where no solution exist
 | otherwise = head solution -- take the first solution that you find
 where x = lines cake -- convert the cake into a list of lines
       m = length (head x) -- width of the cake
       n = length x -- height of the cake
       r = length (filter (=='o') cake) -- number of raisins
       ar = div (m*n) r -- area of each piece
       all = [(i,j)|j<-[0..(n-1)],i<-[0..(m-1)]] -- all coordinates of x
       solution = [s|s<-go all r, length s==r] -- look for a list of r pieces that can be cut off
       go :: [(Int,Int)] -> Int -> [[String]]
       go rest s -- return all lists of pieces that can be cut off
        | null next = [[]] -- no piece can be cut off anymore
        | otherwise =  [(piece (div ar d) d):l|d<-next, l<-go (rest\\[(a+i,b+j)|i<-[0..(div ar d -1)],j<-[0..(d-1)]]) (r-1)]
        where (a,b) = head rest -- position of the next piece
              mw = head [w|w<-[1..], (a+w,b) `notElem` rest] -- maximal width of the next piece
              mh = head [h|h<-[1..], (a,b+h) `notElem` rest] -- maximal width of the next piece
              divisors = [d|d<-[1..mh], mod ar d==0, div ar d<=mw] -- possible heights of the next piece
              piece w h = unlines [take w (drop a (x!!j))|j<-[b..(b+h-1)]] -- returns a piece with given width and height
              next = [d|d<-divisors, length (filter (=='o') (piece (div ar d) d))==1] -- possible heights such that the next piece only contains one raisin

