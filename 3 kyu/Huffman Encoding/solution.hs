54cf7f926b85dcc4e2000d9d


module Huffman
    ( frequencies
    , encode
    , decode
    , Bit (..)
    ) where

import qualified Data.List as DL
import qualified Data.Tuple as DT

frequencies :: Ord a => [a] -> [(a, Int)]
frequencies ls = map (\(c:cs) -> (c,length (c:cs))) (DL.group (DL.sort ls))

data Tree a = Node (Tree a) (Tree a) | Leaf a deriving (Show)

buildTree :: Ord a => [(a,Int)] -> Tree a
buildTree freq = fst $ reduce $ map (\(c,n) -> (Leaf c,n)) (map DT.swap $ DL.sort $ map DT.swap freq)
    where reduce [t] = t
          reduce ((t1,n1):(t2,n2):r) =
                  let p = (\x -> snd x < n1+n2) in
                  reduce $
                  takeWhile p r ++ [(Node t1 t2, n1+n2)] ++ dropWhile p r

data Bit = Z | O deriving (Eq, Show)

treeCode :: Ord a => Tree a -> [(a,[Bit])]
treeCode (Leaf c)     = [(c,[])]
treeCode (Node t1 t2) = map (\(c,ls) -> (c,Z:ls)) (treeCode t1) ++
                        map (\(c,ls) -> (c,O:ls)) (treeCode t2)

-- | Encode a sequence using the given frequencies.
encode :: Ord a => [(a, Int)] -> [a] -> Maybe [Bit]
encode freq t | length freq < 2 = Nothing
              | otherwise       = fmap concat $ sequence $ map (flip lookup table) t
        where table = (treeCode . buildTree) freq

-- | Decode a bit sequence using the given frequencies.
decode :: Ord a => [(a, Int)] -> [Bit] -> Maybe [a]
decode freq t | length freq < 2 = Nothing
              | otherwise       = let (rest,cleartxt) = foldl fld ([],[]) t in
                                  if rest == [] then Just cleartxt else Nothing
        where table = map DT.swap (treeCode (buildTree freq))
              fld (bs,decoded) b = case lookup (bs++[b]) table of
                                   Nothing -> (bs++[b],decoded)
                                   Just c  -> ([],decoded++[c])
                                   
___________________________________________________
module Huffman
    ( frequencies
    , encode
    , decode
    , Bit (..)
    ) where

import Prelude hiding (lookup)
import Data.List (sortBy, groupBy)
import Data.Ord (comparing)
import Data.Map (Map, fromList, size, lookup)

data Bit = Z | O deriving (Eq, Show)
data HTree a = Leaf Int a | Branch Int (HTree a) (HTree a) deriving Show

-- | Calculate symbol frequencies of a text.
frequencies :: Ord a => [a] -> [(a, Int)]
frequencies xs = sortBy (comparing snd) [(head a, length a) | a <- groupBy (==) xs]

-- | Encode a sequence using the given frequencies.
encode :: Ord a => [(a, Int)] -> [a] -> Maybe [Bit]
encode freqs l = (pairsToCodes freqs) >>= myEncode l

myEncode :: Ord a => [a] -> Map a [Bit] -> Maybe [Bit] 
myEncode str codes = concat <$> (sequence $ map ((flip lookup) codes) str)

-- | Decode a bit sequence using the given frequencies.
decode :: [(a, Int)] -> [Bit] -> Maybe [a]
decode pairs bits = (myDecode <$> (buildTreeFromPairs pairs)) <*> Just bits

decodeOnce :: HTree a -> [Bit] -> Maybe (a, [Bit])
decodeOnce (Leaf _ x) bits = Just (x, bits)
decodeOnce (Branch _ l r) (b:bits) = case b of
    Z -> decodeOnce l bits
    O -> decodeOnce r bits
decodeOnce _ [] = Nothing

myDecode :: HTree a -> [Bit] -> [a]
myDecode tree bits = case decodeOnce tree bits of
    Just (a, bts) -> a:(myDecode tree bts)
    Nothing -> []

pairsToCodes :: Ord a => [(a, Int)] -> Maybe (Map a [Bit])
pairsToCodes pairs = fromList <$> (treeToCodes [] <$> (buildTreeFromPairs $ sortBy (comparing snd) pairs))

treeToCodes :: [Bit] -> HTree a -> [(a, [Bit])]
treeToCodes bits (Leaf _ x) = [(x, bits)]
treeToCodes bits (Branch _ l r) = (treeToCodes (bits ++ [Z]) l) ++ (treeToCodes (bits ++ [O]) r) 

insertSortedBy :: Ord a => (b -> a) -> b -> [b] -> [b]
insertSortedBy x e [] = [e]
insertSortedBy f e (x:xs)
    | ve <= vx = e:x:xs
    | otherwise = x:(insertSortedBy f e xs)
    where ve = f e
          vx = f x

treeVal :: HTree a -> Int
treeVal (Leaf n _) = n
treeVal (Branch n _ _) = n

insertSortedTree = insertSortedBy treeVal

pairToLeaf (x, n) = Leaf n x

buildTree :: [HTree a] -> [HTree a]
buildTree [] = []
buildTree (tree:[]) = [tree]
buildTree (a:b:xs) = buildTree $ insertSortedTree (Branch (sum $ map treeVal [a, b]) a b) xs

buildTreeFromPairs :: [(a, Int)] -> Maybe (HTree a)
buildTreeFromPairs x
    | length x <= 1 = Nothing
    | otherwise = Just $ head xs
    where xs = buildTree $ map pairToLeaf x

buildTreeFromList :: Ord a => [a] -> Maybe (HTree a)
buildTreeFromList = buildTreeFromPairs . frequencies

___________________________________________________
module Huffman
    ( frequencies
    , encode
    , decode
    , Bit (..)
    ) where

import Data.List

data Bit = Z | O deriving (Eq, Show)

-- | Calculate symbol frequencies of a text.
frequencies :: Ord a => [a] -> [(a, Int)]
frequencies = map (\xs -> (head xs, length xs)) . group . sort

-- | Encode a sequence using the given frequencies.
encode :: Ord a => [(a, Int)] -> [a] -> Maybe [Bit]
encode fs xs = case tree fs of
  Nothing -> Nothing
  Just t  -> Just $ encodeWithTree t xs
  where
  encodeWithTree t [] = []
  encodeWithTree t (x:xs) = let Just bs = bits t x [] in reverse bs ++ encodeWithTree t xs

-- | Decode a bit sequence using the given frequencies.
decode :: [(a, Int)] -> [Bit] -> Maybe [a]
decode fs xs = case tree fs of
  Nothing -> Nothing
  Just t  -> Just $ decodeWithTree t xs
  where
  decodeWithTree t [] = []
  decodeWithTree t bs = case go t bs of
    Nothing       -> []
    Just (x, bs') -> x : decodeWithTree t bs'
  go (Leaf _ x)   bs     = Just (x, bs)
  go _            []     = Nothing
  go (Node _ t _) (Z:bs) = go t bs
  go (Node _ _ t) (O:bs) = go t bs


data Tree a = Leaf Int a | Node Int (Tree a) (Tree a)

freq :: Tree a -> Int
freq (Leaf n _) = n
freq (Node n _ _) = n

instance Eq (Tree a) where
  t1 == t2 = freq t1 == freq t2
  
instance Ord (Tree a) where
  compare t1 t2 = compare (freq t1) (freq t2)

tree :: [(a, Int)] -> Maybe (Tree a)
tree = mkTree . sort . map (\(x, n) -> Leaf n x)
  
mkTree :: [Tree a] -> Maybe (Tree a)
mkTree [] = Nothing
mkTree [Leaf _ _] = Nothing
mkTree [t] = Just t
mkTree (t1:t2:ts) = 
  let
    t0 = Node (freq t1 + freq t2) t1 t2
  in
    mkTree (insert t0 ts)

bits :: Eq a => Tree a -> a -> [Bit] -> Maybe [Bit]
bits (Leaf _ x) y bs = if x == y then Just bs else Nothing
bits (Node _ t1 t2) y bs =
    case bits t1 y (Z:bs) of
      Nothing  -> bits t2 y (O:bs)
      Just bs' -> Just bs'
