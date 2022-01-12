module CanYouGetTheLoop where
import CanYouGetTheLoop.Types

-- Use Brent's algorithm for finding a cycle.
loopSize :: Eq a => Node a -> Int
loopSize n = findLambda 1 1 n (next n)
    where
        findLambda lam pow tortoise hare
            | tortoise == hare = lam
            | lam == pow = findLambda 1 (pow * 2) hare (next hare)
            | otherwise = findLambda (succ lam) pow tortoise (next hare)
_____________________________________________
module CanYouGetTheLoop where
import CanYouGetTheLoop.Types
import Data.List(elemIndex)
{-
data Node a
instance Eq a => Eq (Node a)

next :: Node a -> Node a
-}

loopSize :: Eq a => Node a -> Int
loopSize n = searchLoop [] n
  where searchLoop stack n = 
          case elemIndex n stack of
            Nothing -> searchLoop (n:stack) (next n)
            Just i  -> i + 1
_____________________________________________
module CanYouGetTheLoop where
import CanYouGetTheLoop.Types
import Data.List

{-
data Node a
instance Eq a => Eq (Node a)

next :: Node a -> Node a
-}

calculate :: Eq a => [Node a] -> Node a -> Int
calculate visited this = case elemIndex this visited of
  (Just i) -> i + 1
  _ -> calculate (this : visited) $ next this
--
    
loopSize :: Eq a => Node a -> Int
loopSize = calculate []
_____________________________________________
module CanYouGetTheLoop where
import CanYouGetTheLoop.Types

import Data.HashMap.Lazy
loopSize :: Node Int-> Int
loopSize node =  go node 0 (fromList []) where
  go (Node no nex) i hmap = if (member no hmap) then (i - (hmap ! no)) else go nex (i+1) (insert no i hmap)
_____________________________________________
module CanYouGetTheLoop where

import CanYouGetTheLoop.Types
import qualified Data.HashMap.Strict as M
import System.IO.Unsafe
import System.Mem.StableName

loopSize :: Eq a => Node a -> Int
loopSize start = unsafePerformIO $ go start M.empty
  where
    go node@(Node label _) seen = do
      label' <- makeStableName label
      case M.lookup label' seen of
        Just lastIndex -> return $ M.size seen - lastIndex
        Nothing -> go (next node) (M.insert label' (M.size seen) seen)

