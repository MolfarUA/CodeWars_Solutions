module AlphabeticAnagrams where
import Data.List

fac :: Int -> Integer
fac n = product [1,2..(toInteger n)]

vars :: String -> Integer
vars s = (fac $ length s) `div` (product $ (map (fac . length)) $ group $ sort s)

before :: String -> Integer
before s = sum $ map (\x -> vars $ delete x s) $ filter ((>) (head s)) (nub s)

lexiPos :: String -> Integer
lexiPos [] = 1
lexiPos s = (before s) + lexiPos (tail s)

___________________________________________________
module AlphabeticAnagrams where
import Data.List
import qualified Data.Map as Map

lexiPos :: String -> Integer
lexiPos = (\(p, _, _, _) -> p) . foldr pos (1, 1, 1, Map.empty) where
    pos w (p, n, l, ws) = (p + lt * n `div` eq, l * n `div` eq, l + 1, Map.insertWith (+) w 1 ws)
         where eq = Map.findWithDefault 0 w ws + 1
               lt = foldr (+) 0 $ fst $ Map.split w ws

___________________________________________________
module AlphabeticAnagrams where
import Data.List

fact :: Int -> Integer
fact = product . enumFromTo 2 . toInteger

anagrs :: Ord a => [a] -> Integer
anagrs ls = (fact . length $ ls) `div` (product . fmap (fact . length) . group . sort $ ls)

posPerm :: Ord a => [a] -> Integer
posPerm bk = let tm = sort . nub $ bk in sum . fmap snd . takeWhile ((/= head bk) . fst) . zip tm $ anagrs . flip delete bk <$> tm


lexiPos :: String -> Integer
lexiPos s = (+1) . sum  $ posPerm <$> tails s

___________________________________________________
module AlphabeticAnagrams where
import Data.List

lexiPos :: String -> Integer
lexiPos [x] = 1
lexiPos xs@(y:ys) = prev + lexiPos ys
  where prev = sum . map (\c -> perms $ xs \\ [c]) . nub $ filter (<y) ys
        perms xs = f (length xs) `div` (product . map (f . length) . group $ sort xs)
        f 0 = 1
        f n = fromIntegral (n) * f (n - 1)
