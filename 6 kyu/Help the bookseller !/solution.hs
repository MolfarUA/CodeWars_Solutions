module Codewars.Kata.Bookseller where
import Codewars.Kata.Bookseller.Types

-- data Stock    = Stock String Int deriving (Show, Eq)
stocklist :: [Stock] -> [Char] -> [(Char, Int)]
stocklist _ [] = []
stocklist [] _ = []
stocklist st cs = map (\x -> (x, quantity st x)) cs

quantity :: [Stock] -> Char -> Int
quantity st x = sum [if x == head c then q else 0 | Stock c q <- st]
________________________________________
module Codewars.Kata.Bookseller where
import Codewars.Kata.Bookseller.Types

import Control.Arrow ((&&&))
import Data.Map.Strict (findWithDefault, fromListWith)
import Control.Applicative ((<*>))

stocklist :: [Stock] -> [Char] -> [(Char, Int)]
stocklist [] = const []
stocklist st = map $ (,) <*> flip (findWithDefault 0) counter
  where counter = fromListWith (+) $ map itemize st
        itemize (Stock s c) = (head s, c)
________________________________________
module Codewars.Kata.Bookseller where

import Codewars.Kata.Bookseller.Types

stocklist :: [Stock] -> String -> [(Char, Int)]
stocklist [] _ = []
stocklist st cs = map (\cat -> (cat, sum . map quantity . filter (\b -> (==cat) . head . code $ b) $ st)) $ cs
    where code (Stock c _) = c
          quantity (Stock _ q) = q
________________________________________
module Codewars.Kata.Bookseller where
import Codewars.Kata.Bookseller.Types
import Data.Map

-- data Stock    = Stock String Int deriving (Show, Eq)

stocklist :: [Stock] -> [Char] -> [(Char, Int)]
stocklist [] _ = []
stocklist st cs = 
  let stm = Prelude.foldl (unionWith (+)) empty (fmap s2m st)
  -- in filter (\(c, _) -> c `elem` cs) $ toList stm
  in fmap (\c -> (c, findWithDefault 0 c stm)) cs
 
s2m :: Stock -> Map Char Int
s2m (Stock (c:_) i) = singleton c i
________________________________________
odule Codewars.Kata.Bookseller where
import Codewars.Kata.Bookseller.Types

name :: Stock -> String
name (Stock s n) = s

num :: Stock -> Int
num (Stock s n) = n

stocklist :: [Stock] -> [Char] -> [(Char, Int)]
stocklist [] _ = []
stocklist _ [] = []
stocklist st cs = let lst = [(head $ name t, num t) | t <- st]
                  in [(m, n) | m <- cs, let n = sum $ map snd $ filter (\t->fst t==m) lst]
