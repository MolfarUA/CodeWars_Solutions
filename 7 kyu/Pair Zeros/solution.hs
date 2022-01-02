module PairZeros (pairZeros) where

pairZeros :: [Int] -> [Int]
pairZeros xs = fst (foldl go (id,True) xs) [] where
  go (z,False) 0 = (z        ,  True)
  go (z, True) 0 = (z . (0 :), False)
  go (z, keep) x = (z . (x :),  keep)
  
_____________________________________
module PairZeros (pairZeros) where

import Control.Arrow ((&&&))
import Control.Monad ((>=>))
import Control.Monad.State (evalStateT, state)
import Control.Monad.Writer (execWriter, tell)
import Data.Bool (bool)
import Data.Monoid (Endo(Endo), appEndo)

pairZeros :: [Int] -> [Int]
pairZeros =
  (`appEndo` []) . execWriter . (`evalStateT` cycle [(:), const id]) .
  mapM_ ((<*>) <$> bool (pure (:)) (state $ head &&& tail) . (== 0) <*> pure >=> tell . Endo)
  
_____________________________________
module PairZeros (pairZeros) where

pairZeros :: [Int] -> [Int]
pairZeros lst
    = p' lst 0
        where p' (x:xs) c
                | x /= 0    = x : p' xs c
                | x == 0 && c == 1   = p' xs (c - 1)
                | otherwise = x : p' xs (c + 1)
              p' [] c = []
              
_____________________________________
module PairZeros (pairZeros) where

pairZeros :: [Int] -> [Int]
pairZeros = pairZeros' $ cycle [(:), const id]

pairZeros'    (f : fs) (0 : ds) = 0 `f` pairZeros' fs ds
pairZeros' fs@(f :  _) (d : ds) = d  :  pairZeros' fs ds
pairZeros'          _       []  =       []

