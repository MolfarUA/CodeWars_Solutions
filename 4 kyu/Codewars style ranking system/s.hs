module CodewarRanking where

data User = User { rank :: Int, progress :: Int}

ranks :: [Int]
ranks = [-8..(-1)] ++ [1..8]

updateRank :: Int -> Int -> Int
updateRank m n = case drop n . dropWhile (/=m) $ ranks of
  [] -> last ranks
  (x:xs) -> x

diffRank :: Int -> Int -> Int
diffRank m n = if m < n then diff m n else negate (diff n m) where
  diff x y = ((-) 1) . length . dropWhile (/=y) . reverse . dropWhile (/=x) $ ranks

newUser :: User
newUser = User {rank = -8, progress = 0}

incProgress n (User r p)
  | n > 8 || n < -8 || n == 0 = error "invalid"
  | otherwise = User { rank = newRank, progress = if newRank == 8 then 0 else (p + points) `rem` 100} where
  newRank = updateRank r ((p + points) `div` 100)
  points = case diffRank n r of
    -1 -> 1
    0 -> 3
    i -> if i > 0 then 10 * i * i else 0
_____________________________________
module CodewarRanking where

data User = User Int

ranks :: [Int]
ranks = filter (/= 0) [-8..8]

newUser :: User
newUser = User 0

rank :: User -> Int
rank (User s) = ranks !! min 15 (s `div` 100)

progress :: User -> Int
progress u@(User s)
  | rank u == last ranks = 0
  | otherwise            = s `mod` 100

incProgress :: Int -> User -> User
incProgress a u@(User s)
  | not $ elem a ranks = error "Invalid rank"
  | a == r             = User (s + 3)
  | r > a && diff == 1 = User (s + 1)
  | r < a              = User (s + (10 * (diff ^ 2)))
  | otherwise          = u
  where (r, p) = (rank u, progress u)
        diff   = pred . length . filter (/= 0) $ [min r a..max r a]
_____________________________________
module CodewarRanking where
import Control.Monad
import Data.Bool

type User = Int

newUser :: User
newUser = -800

rank :: User -> Int
rank = min 8 . join (bool id succ . (>= 0)) . (`div` 100)

progress :: User -> Int
progress = join (bool (`mod` 100) (const 0) . (>= 700))

incProgress :: Int -> User -> User
incProgress l u | abs l `elem` [1..8] = case compare l (rank u) of
  LT -> u + 1 ; EQ -> u + 3
  GT -> u + 10 * (l - div u 100 - bool 0 1 (l > 0)) ^ 2
_____________________________________
module CodewarRanking where

data User = User { rank     :: Int
                 , progress :: Int
                 }

newUser :: User
newUser = User { rank = -8
               , progress = 0
               }

incProgress :: Int -> User -> User
incProgress x User { rank = r, progress = p }
    | -8 > min x r
    || 8 < max x r
    || x == 0
    || r == 0   = error "invalid range"
    | otherwise = User { rank = r', progress = p' }
  where
    (r', p') | r + r'' > 7        = (8, 0)
             | r < 0 && r >= -r'' = (min 7 $ r + r'' + 1, p'')
             | otherwise          = (r + r'', p'')
    (r'', p'') = flip quotRem 100 $ p + case compare x r of
        GT -> 10 * (x - if x > 0 && r < 0 then r + 1 else r)^2
        EQ -> 3
        _  -> if r - x == 1 || r == 1 && x == -1 then 1 else 0
_____________________________________
module CodewarRanking where

data User = User { rank :: Int
                 , progress :: Int
                 } deriving (Show)

newUser :: User
newUser = User (-8) 0

incProgress :: Int -> User -> User
incProgress prob (User level _) | invalid prob || invalid level = error "input error"
  where invalid l = l < -8 || l > 8 || l == 0
incProgress prob (User level point) = adv (User level (point + calc prob level))
  where adv (User 8 p) = User 8 0
        adv (User 0 p) = adv (User 1 p)
        adv (User n p) = if (p >= 100) then adv (User (n+1) (p-100)) else User n p
        calc p l 
          | p == l          = 3
          | diff l p == 1   = 1
          | diff l p > 1    = 0
          | diff l p < 0    = 10 * (diff p l) ^ 2
        diff p l 
          | p * l > 0 = p - l
          | p > 0     = p - l - 1
          | otherwise = p - l + 1
_____________________________________
module CodewarRanking where

type Rank = Int
type Progress = Int
data User = User {rank::Rank, progress::Progress} deriving (Show)

cr :: Rank -> Rank -> Int
cr or nr | or < -8 || or == 0 || or > 8 = error "Impossible rank"
         | or < 0 && nr >= 0            = 1
         | or > 0 && nr <= 0            = -1
         | otherwise                    = 0

(|+|) :: Rank -> Int -> Rank
(|+|) l r = max (-8) . min 8 $ (l + r + cr l (l + r))

(|-|) :: Rank -> Rank -> Int
(|-|) l r = l - r + cr l r

(|^|) :: User -> Progress -> User
(|^|) (User r p) dp = User nr (if nr == 8 then 0 else np)
 where
  (dr, np) = (p + dp) `divMod` 100
  nr       = r |+| dr


newUser :: User
newUser = User (-8) 0

incProgress :: Int -> User -> User
incProgress cr u | dr < -1   = u
                 | dr == -1  = u |^| 1
                 | dr == 0   = u |^| 3
                 | otherwise = u |^| (10 * dr * dr)
  where dr = cr |-| rank u
