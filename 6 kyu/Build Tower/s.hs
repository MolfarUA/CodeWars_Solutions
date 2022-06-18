576757b1df89ecf5bd00073b


module Codewars.BuildTower where

buildTower :: Int -> [String]
buildTower n = [(sp x++ st x++ sp x) | x <- [1..n]]
    where sp x = replicate (n-x) ' '
          st x = replicate (2*x-1) '*'
_____________________________
module Codewars.BuildTower where

buildTower :: Int -> [String]
buildTower count = map floor [1..count] where
  spacing i = replicate (count - i) ' '
  tower i = replicate (2*i-1) '*'
  floor i = spacing i ++ tower i ++ spacing i
_____________________________
module Codewars.BuildTower where

buildFloor :: Int -> Int -> String
buildFloor i n = [if abs j < i then '*' else ' ' | j <- [1 - n .. n - 1]]

buildTower :: Int -> [String]
buildTower n = [buildFloor i n | i <- [1..n]]
_____________________________
module Codewars.BuildTower where

buildTower :: Int -> [String]
buildTower 0 = []
buildTower n = map (\s -> " " ++ s ++ " ") (buildTower (n-1)) ++ [replicate (2 * n - 1) '*']
_____________________________
module Codewars.BuildTower where

buildTower :: Int -> [String]
buildTower 0 = []
buildTower x = map (\x -> ' ' : x ++ " ") (buildTower (x - 1)) ++ [replicate (2 * x - 1) '*']
_____________________________
module Codewars.BuildTower where

buildTower :: Int -> [String]
buildTower n = map level [1..n]
  where level k = padding k ++ floor k ++ padding k
        floor k = replicate (2 * k - 1) '*'
        padding k = replicate (n - k) ' '
        
