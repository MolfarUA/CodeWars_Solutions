53f40dff5f9d31b813000774


module RecoverSecretFromTriplets where

import Data.Set (fromList, toList)
import Data.Char (ord, chr)
import Data.Graph (buildG, topSort)

recoverSecret :: [String] -> String
recoverSecret triplets = filter (`elem` alpha) $ map chr $ topSort graph
                         where alpha = (toList . fromList . concat) triplets
                               edges = concat $ map (\[p,i,s]->[(ord p, ord i), (ord i,ord s)]) triplets
                               graph = buildG (ord $ minimum alpha, ord $ maximum alpha) $ edges

#########################
module RecoverSecretFromTriplets where

import Data.List (nub)

recoverSecret :: [String] -> String
recoverSecret [] = []
recoverSecret ts = c : recoverSecret (rmChar ts c)
  where cs          = nub $ concat ts
        c           = head $ (filter (isFst ts) cs)
        isFst xs c  = and $ map ((notElem c) . tail) xs
        rmChar xs c = filter (/="") $ map (filter (/=c)) xs

##############################
module RecoverSecretFromTriplets where

import Data.List

recoverSecret :: [String] -> String
recoverSecret [] = ""
recoverSecret triplets = c : (recoverSecret . removenull . removeletter c) triplets where
  c = nextletter (candidates triplets) (successors triplets)

removeletter :: Char -> [String] -> [String]
removeletter c = map (filter (/= c))

removenull :: [String] -> [String]
removenull = filter (not . null)

nextletter :: [Char] -> [Char] -> Char
nextletter cs ss = head (cs \\ ss)

candidates :: [String] -> String
candidates = uniques . map head

successors :: [String] -> String
successors = uniques . intercalate "" . map tail

uniques :: Eq a => [a] -> [a]
uniques [] = []
uniques (c:cs) = c : uniques (filter (/= c) cs)
