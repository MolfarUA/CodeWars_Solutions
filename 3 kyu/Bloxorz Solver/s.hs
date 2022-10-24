5a2a597a8882f392020005e5

module Bloxorz (bloxSolver) where

import Control.Applicative
import Data.Foldable
import Data.List
import qualified Data.Map as M
import Data.Maybe

-- an interesting problem
-- https://www.codewars.com/kata/5a2a597a8882f392020005e5/train/haskell

data Loc = Loc Int Int deriving (Eq, Show, Ord)

data BoxState = Upward | Horizontal | Vertical deriving (Eq, Show, Ord)

data Position = Position Loc BoxState deriving (Eq, Show, Ord)

type Maze = [[Char]]

bloxSolver :: [[Char]] -> [Char]
bloxSolver tiles = reverse . fromJust $ getST tiles >>= (\(s, t) -> bfs tiles [Position s Upward] (Position s Upward) (Position t Upward) [Position s Upward] M.empty)

getST :: Maze -> Maybe (Loc, Loc)
getST maze = case (go maze 'B' 0, go maze 'X' 0) of
  (Just x, Just y) -> Just (x, y)
  _ -> Nothing
  where
    go :: Maze -> Char -> Int -> Maybe Loc
    go (l : m) c n = (elemIndex c l >>= (Just . Loc n)) <|> go m c (n + 1)
    go [] _ _ = Nothing
    
avai :: Maze -> [Position] -> Position -> Bool
avai m visited p@(Position l@(Loc x y) Vertical) =
  (isJust (get m l) && get m l /= Just '0') && (get m (Loc (x + 1) y) /= Just '0' && isJust (get m (Loc (x + 1) y)))
    && p `notElem` visited
avai m visited p@(Position l@(Loc x y) Horizontal) =
  (get m l /= Just '0' && isJust (get m l)) && (get m (Loc x (y + 1)) /= Just '0' && isJust (get m (Loc x (y + 1))))
    && p `notElem` visited
avai m visited p@(Position l@(Loc x y) Upward) =
    get m l /= Just '0' && isJust (get m l) && p `notElem` visited

-- 占据两个位置的，总是考虑最左上
neighbors :: Maze -> [Position] -> Position -> [(Position, Char)]
neighbors m visited pos = filter (avai m visited . fst) (nbs pos)

(!?) :: [a] -> Int -> Maybe a
_ !? n | n < 0 = Nothing
[] !? n = Nothing
(x : xs) !? 0 = Just x
(x : xs) !? n = xs !? (n - 1)

get :: Maze -> Loc -> Maybe Char
get m (Loc x y) = m !? x >>= (!? y)

bfs :: Maze -> [Position] -> Position -> Position -> [Position] -> M.Map Position Char -> Maybe [Char]
bfs m (top : queue) start target visited bfsTree
  | target `elem` poses = buildRoute (foldr (uncurry M.insert) bfsTree ns) target
  | otherwise =
    bfs
      m
      (queue ++ poses)
      start
      target
      (poses ++ visited)
      (foldr (uncurry M.insert) bfsTree ns)
  where
    ns = neighbors m (top : visited) top
    poses = map fst ns
    buildRoute :: M.Map Position Char -> Position -> Maybe [Char]
    buildRoute map p
      | p == start = Just []
      | otherwise = do
        c <- M.lookup p map
        rest <- buildRoute map (op (inverse c) p)
        return (c : rest)
bfs maze [] _ _ _ _ = error (show maze)

nbs :: Position -> [(Position, Char)]
nbs (Position (Loc x y) Upward) =
  [ (Position (Loc (x - 2) y) Vertical, 'U'),
    (Position (Loc (x + 1) y) Vertical, 'D'),
    (Position (Loc x (y + 1)) Horizontal, 'R'),
    (Position (Loc x (y - 2)) Horizontal, 'L')
  ]
nbs (Position (Loc x y) Horizontal) =
  [ (Position (Loc (x - 1) y) Horizontal, 'U'),
    (Position (Loc (x + 1) y) Horizontal, 'D'),
    (Position (Loc x (y + 2)) Upward, 'R'),
    (Position (Loc x (y - 1)) Upward, 'L')
  ]
nbs (Position (Loc x y) Vertical) =
  [ (Position (Loc (x - 1) y) Upward, 'U'),
    (Position (Loc (x + 2) y) Upward, 'D'),
    (Position (Loc x (y + 1)) Vertical, 'R'),
    (Position (Loc x (y - 1)) Vertical, 'L')
  ]

up :: Position -> Position
up p = fst $ head (nbs p)

down :: Position -> Position
down p = fst $ nbs p !! 1

right :: Position -> Position
right p = fst $ nbs p !! 2

left :: Position -> Position
left p = fst $ nbs p !! 3

op :: Char -> Position -> Position
op 'U' = up
op 'D' = down
op 'R' = right
op 'L' = left
op _ = id

inverse :: Char -> Char
inverse 'U' = 'D'
inverse 'D' = 'U'
inverse 'L' = 'R'
inverse 'R' = 'L'
inverse a = a

jjj :: [[Char]]
jjj =
  -- RRRDD-RUU, RRRRR-UL
  [ "000001X11",
    "B11111111",
    "000011100",
    "000011100"
  ]

err =
  [ "00001110000000000000",
    "00001111111100000000",
    "00001000001100000000",
    "01111111001100000000",
    "01B10011101100000000",
    "01100011111110000000",
    "01100011111110000000",
    "00000000000011100000",
    "00000000000011100000",
    "00001111111111111000",
    "01111101110000000000",
    "01101111110011111111",
    "011111001111111011X1",
    "01100000011101001111"
  ]

main :: IO ()
main = print (bloxSolver jjj)
_________________________________
{-# LANGUAGE RecordWildCards #-}
module Bloxorz (bloxSolver) where

import Control.Applicative (liftA2)
import Data.Array ((!), Array, array, assocs, bounds, inRange, range)
import Data.Monoid
import Data.Sequence (Seq, Seq(..),(|>))
import qualified Data.Set as S
import qualified Control.Monad.State as St
import Debug.Trace

data Tri = Tri !Int !Int !Int deriving (Show, Eq, Ord)
newtype Rot = Rot Tri deriving (Show, Eq, Ord)

data Move = Move {
      tx :: Tri,
      ty :: Tri,
      rot :: Rot
   } deriving (Show)
   
rotate :: Rot -> Tri -> Tri
rotate (Rot x) y = r x y 
  where
    r (Tri 0 1 2) x = x
    r (Tri 0 2 1) (Tri x1 x2 x3) = Tri x1 x3 x2
    r (Tri 1 0 2) (Tri x1 x2 x3)  = Tri x2 x1 x3
    r (Tri 1 2 0) (Tri x1 x2 x3) = Tri x2 x3 x1
    r (Tri 2 0 1) (Tri x1 x2 x3) = Tri x3 x1 x2
    r (Tri 2 1 0) (Tri x1 x2 x3)  = Tri x3 x2 x1
    r _ _ = error "Corrupted rotation"

up = Move {
    tx = Tri 0 0 0,
    ty = Tri 0 0 $ -1,
    rot = Rot $ Tri 0 2 1
  }      
  
down = Move {
    tx = Tri 0 0 0,
    ty = Tri 0 1 0,
    rot = Rot $ Tri 0 2 1
  }

left = Move {
    tx = Tri 0 0 $ -1,
    ty = Tri 0 0 0,
    rot = Rot $ Tri 2 1 0
  }

right = Move {
    tx = Tri 1 0 0,
    ty = Tri 0 0 0,
    rot = Rot $ Tri 2 1 0
 }

type Board = Array (Int, Int) Char
data Position = Position {
    coordinate :: (Int, Int),
    orient :: Tri
  } deriving (Show, Eq, Ord)
  
isFloor :: Char -> Bool
isFloor = (== '1')
isEmpty = (== '0')
isStartingPoint = (== 'B')
isGoal = (== 'X')
canLay = isFloor `aor` isStartingPoint `aor`  isGoal
  where
    aor = liftA2 (||)

newPosition :: Position -> Move -> Position
newPosition (Position (px, py) o) (Move {..}) =
  Position (px + dx, py + dy) o'
  where
    o' = rotate rot o
    Tri lx ly lz = o
    m (Tri x1 x2 x3) = x1 * lx + x2 * ly + x3 * lz
    dx = m tx
    dy = m ty

isValidMove :: Board -> Position -> Bool
isValidMove b (Position (sx, sy) (Tri lx ly _)) =
  and [inRange bnds (x, y) && (canLay $ b ! (x, y))
    | x <- [sx..sx+lx-1], y <- [sy..sy+ly-1]]
    where
     bnds = bounds b

isFinished :: Board -> Position -> Bool
isFinished b p@(Position c (Tri ox oy _)) = isValidMove b p && (isGoal $ b!c) && (ox, oy) == (1, 1)

data Step = U | L | D | R deriving (Show, Eq, Bounded, Enum)
data GameState = GS {
   pos :: Position,
   steps :: [Step]
  } deriving (Show)
  
data SearchState = SS {
    openStates :: Seq GameState,
    seenPositions :: S.Set Position,
    board :: Board
  } deriving (Show)
  
stepToMove = go
  where
    go U = up
    go L = left
    go D = down
    go R = right

search :: St.State SearchState [Step]
search = do
  ss@SS{..} <- St.get
  let (h :<| hs) = openStates
  St.put ss{openStates=hs}
  let gs@GS{..} = h
      takeMoves [] = search
      takeMoves (e:es)
        | not $ isValidMove board pos' = con
        | isFinished board pos' = return steps'
        | S.member pos' seenPositions = con
        | otherwise = do
            St.modify $ \SS{openStates=hs',seenPositions=sp} ->
              SS{openStates=hs' |> gs', seenPositions=S.insert pos' sp, board=board}
            con
        where
          con = takeMoves es
          steps' = e:steps
          pos' = newPosition pos $ stepToMove e
          gs' = GS pos' steps'
      go = takeMoves $ enumFrom U
  if isFinished board pos
    then return $ steps
    else go

readBoard :: [[Char]] -> Board
readBoard cs = array ((0,0), maximum [p | (p, _) <- ass]) ass
  where
    ass = do
      (y, r) <- zip [0..] cs
      (x, c) <- zip [0..] r
      return ((x, y), c)
  
showSteps :: [Step] -> String
showSteps ss = reverse ss >>= show

bloxSolver :: [[Char]] -> [Char]
bloxSolver tiles = showSteps rs
  where
    b = readBoard tiles
    (p, _):_ = [k | k@(_, c) <- assocs b, isStartingPoint c]
    pos = Position p (Tri 1 1 2)
    gs = GS{pos=pos, steps=[]}
    ss = SS{openStates=gs :<| Empty, seenPositions=S.singleton pos, board=b}
    rs = St.evalState search ss
_________________________________
module Bloxorz (bloxSolver) where

import Control.Monad (join)
import qualified Data.List as L (nubBy)
import qualified Data.Vector as V (Vector,fromList,(!),(!?))
import qualified Data.Map as M (Map,fromList,lookup,union)

bloxSolver :: [[Char]] -> [Char]
bloxSolver tiles' = (\(Just s) -> reverse s).M.lookup posF $ f [(posI,"")] (M.fromList [(posI,"")])
  where tiles = V.fromList.map V.fromList $ tiles'
        (nx,ny) = (length tiles,length.(V.! 0) $ tiles)
        posI = (\(Just p) -> Left p).head.filter (not.null) $
          [if tiles V.! i V.! j == 'B' then Just (i,j) else Nothing | i<-[0..nx-1], j<-[0..ny-1]]
        posF = (\(Just p) -> Left p).head.filter (not.null) $
          [if tiles V.! i V.! j == 'X' then Just (i,j) else Nothing | i<-[0..nx-1], j<-[0..ny-1]]
        f [] m = m
        f ps m = f ps' m'
          where ps' = filter (null.flip M.lookup m.fst).
                  L.nubBy (\a b -> fst a == fst b).concat.map neighbours $ ps
                m' = M.union m (M.fromList ps')
        neighbours ((Left (i,j)),s) = filter (lookup.fst) $
          [(Right ((i+1,j),(i+2,j)),'D':s),(Right ((i,j+1),(i,j+2)),'R':s)
          ,(Right ((i-2,j),(i-1,j)),'U':s),(Right ((i,j-2),(i,j-1)),'L':s)]
        neighbours ((Right ((i1,j1),(i2,j2))),s) | i1==i2 = filter (lookup.fst) $
          [(Right ((i1+1,j1),(i2+1,j2)),'D':s),(Left (i1,j2 + 1),'R':s)
          ,(Right ((i1-1,j1),(i2-1,j2)),'U':s),(Left (i1,j1 - 1),'L':s)]
        neighbours ((Right ((i1,j1),(i2,j2))),s) | j1==j2 = filter (lookup.fst) $
          [(Left (i2 + 1,j1),'D':s),(Right ((i1,j1+1),(i2,j2+1)),'R':s)
          ,(Left (i1 - 1,j1),'U':s),(Right ((i1,j1-1),(i2,j2-1)),'L':s)]
        lookup (Left (i,j)) = let t = join.fmap (V.!? j) $ tiles V.!? i in t/=Nothing && t/=Just '0'
        lookup (Right (a,b)) = lookup (Left a) && lookup (Left b)
_________________________________
module Bloxorz where
import Prelude
import Data.List ( nub,elemIndex )

-- Functions that get useful information from the bluperint

position :: Char-> String -> Int
position i xs = maybe (-1) (+0) $ i `elemIndex` xs

dimension :: [String] ->  (Int, Int)
dimension a = (length a, length (head a))

whichrowsmallerthann :: Char -> Int -> [String] -> (Int, Int)
whichrowsmallerthann i n blueprint
    | position i (blueprint !! n)/=(-1) = (n ,position i (blueprint !! n))
    | n>(-1) = whichrowsmallerthann i (n-1) blueprint
    | otherwise = error "There is no"

whichrow :: Char -> [String] -> (Int, Int)
whichrow i blueprint=whichrowsmallerthann i (length blueprint-1) blueprint

start :: [String] -> (Int, Int)
start = whichrow 'B'

finish :: [String] -> (Int, Int)
finish = whichrow 'X'

-- I define a new type for the different states of the block and for paths. The path is given with the final position instea of original position.
data State = State Int Int Char deriving (Show, Eq)
data Path = Path String State deriving (Show, Eq)

origin :: State -> (Int,Int)
origin (State  x y _)  = (x, y)
direction:: State -> Char
direction (State  _ _ a)
    | a `elem` "XYZ" =a
    | otherwise=error "The block is in a superposition"

destination :: Path -> State
destination (Path a b)=  b
actionstaken :: Path -> String
actionstaken (Path a b) = a

--I provide the transformation 

transition :: State -> Char -> State
transition st action
    | origin st ==(-1,-1)= st
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    | action=='U' &&  direction st == 'X' = State (fst (origin st)-1)  (snd (origin st)) 'X'
    | action=='U' &&  direction st == 'Y' = State (fst (origin st)-2)  (snd (origin st)) 'Z'
    | action=='U' &&  direction st == 'Z' =  State (fst (origin st)-1)  (snd (origin st)) 'Y'
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    | action=='D' &&  direction st == 'X' = State (fst (origin st)+1)  (snd (origin st)) 'X'
    | action=='D' &&  direction st == 'Y' = State (fst (origin st)+1)  (snd (origin st)) 'Z'
    | action=='D' &&  direction st == 'Z' =  State (fst (origin st)+2)  (snd (origin st)) 'Y'
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    | action=='L' &&  direction st == 'X' = State (fst (origin st))  (snd (origin st)-1) 'Z'
    | action=='L' &&  direction st == 'Y' = State (fst (origin st))  (snd (origin st)-1) 'Y'
    | action=='L' &&  direction st == 'Z' =  State (fst (origin st))  (snd (origin st)-2) 'X'
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    | action=='R' &&  direction st == 'X' = State (fst (origin st))  (snd (origin st)+2) 'Z'
    | action=='R' &&  direction st == 'Y' = State (fst (origin st))  (snd (origin st)+1) 'Y'
    | action=='R' &&  direction st == 'Z' =  State (fst (origin st))  (snd (origin st)+1) 'X'

    | otherwise= State (-1) (-1) 'Z'

--Check if a state is actual valid for a specific blueprinnt

isitavalidstate :: State -> [String] -> Bool
isitavalidstate st blueprint
    | direction st=='X' && not( -1<(fst (origin st))  && (fst (dimension blueprint))>(fst (origin st)) &&  ( -1<snd (origin st) ) && (snd (origin st)+1<(snd (dimension blueprint)))) = False
    | direction st=='X' && (blueprint !! (fst (origin st)) ) !! (snd (origin st)) `elem` "XB1"&& (blueprint !! (fst (origin st)) ) !! (snd (origin st)+1) `elem` "XB1"= True
    | direction st=='Y' && not( 0<(fst (origin st))  && (fst (dimension blueprint))>(fst (origin st)) &&  ( -1<snd (origin st) ) && (snd (origin st)<(snd (dimension blueprint)))) = False
    | direction st=='Y' && (blueprint !! (fst (origin st)) ) !! (snd (origin st)) `elem` "XB1"&& (blueprint !! (fst (origin st)-1) ) !! (snd (origin st)) `elem` "XB1"= True
    | direction st=='Z' && not( -1<(fst (origin st))  && (fst (dimension blueprint))>(fst (origin st)) &&  ( -1<snd (origin st) ) && (snd (origin st)<(snd (dimension blueprint)))) = False
    | direction st=='Z' && (blueprint !! (fst (origin st)) ) !! (snd (origin st)) `elem` "XB1"= True
    | otherwise = False



--
--Path iteration
shouldIextendPath :: Path -> Char -> [String] -> [State]-> Bool
shouldIextendPath  path action blueprint visitedstates
    | isitavalidstate (transition (destination path) action) blueprint  && notElem (transition (destination path) action) visitedstates= True
    | otherwise = False

extendpath2 :: Path -> (Char, [String], [State]) -> [Path]
extendpath2  path (action, blueprint, visitedstates)
    |  shouldIextendPath  path action blueprint visitedstates= [Path (actionstaken path++[action]) (transition (destination path) action)]
    |   otherwise = []

extendpath1 :: ([Path], [String], [State]) -> Char -> [Path]
extendpath1 (pathlist, blueprint, visitedstates) action =concatMap (`extendpath2`  (action, blueprint, visitedstates)) pathlist

extendpath :: ([String], [Path], [State]) -> [Path]
extendpath (blueprint, pathlist, visitedstates)= concatMap ((pathlist, blueprint, visitedstates)`extendpath1`) "LRUD"


extendvisitedstates2 :: (Path, [String], [State]) -> Char -> [State]
extendvisitedstates2 (path, blueprint, visitedstates) action
    |shouldIextendPath  path action blueprint visitedstates = visitedstates ++[transition (destination path) action]
    |otherwise= []

extendvisitedstates1 :: ([String], [State]) -> Path -> [State]
extendvisitedstates1 (blueprint, visitedstates) path= concatMap ( (path, blueprint, visitedstates) `extendvisitedstates2`) "LRUD"

extendvisitedstates :: ([String], [Path], [State]) -> [State]
extendvisitedstates (blueprint , pathlist, visitedstates) = nub (concatMap ((blueprint, visitedstates)  `extendvisitedstates1 ` ) pathlist)


obliterate :: ([String], [Path], [State]) -> ([String], [Path], [State])
obliterate (blueprint, pathlist,visitedstates)=(blueprint, extendpath (blueprint,pathlist, visitedstates),extendvisitedstates (blueprint , pathlist, visitedstates))


originalpath :: [String] -> Path
originalpath blueprint= Path [] ( State (fst(start blueprint)) (snd(start blueprint))  'Z') 

originalstate :: [String] -> State
originalstate blueprint =destination (originalpath blueprint)

isdestination :: [String] -> Path -> Bool
isdestination blueprint path= destination path==( State (fst(finish blueprint)) (snd(finish blueprint))  'Z')

solution :: ([String], [Path], [State]) -> [String]
solution (blueprint, pathlist, visitedstates)
        | ( State (fst(finish blueprint)) (snd(finish blueprint))  'Z') `elem` visitedstates = map actionstaken (filter (blueprint `isdestination` ) pathlist)
        | otherwise = solution (obliterate (blueprint, pathlist, visitedstates))


bloxSolver :: [[Char]] -> [Char]
bloxSolver tiles = solution (tiles,[originalpath tiles],[originalstate tiles]) !! 0
