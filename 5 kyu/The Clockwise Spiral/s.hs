536a155256eb459b8700077e


module Spiral (createSpiral) where

-- adds a column to the left and to the right of a matrix
addWalls :: [a] -> [a] -> [[a]] -> [[a]]
addWalls (lx:lxs) (rx:rxs) (x:xs) = (lx : x ++ [rx]) : addWalls lxs rxs xs
addWalls _ _ _                    = []

createSpiral :: Int -> [[Int]]
createSpiral 1 = [[1]]
createSpiral n
  | n < 1 = []
  | otherwise = top ++ addWalls left right center ++ bottom
  where
    top = [[1 .. n]]
    center = (map . map) (+ (4 * n - 4)) (createSpiral $ n - 2)
    bottom = [reverse [(2 * n - 1) .. (3 * n - 2)]]
    left = reverse [(3 * n - 1) .. (4 * n - 4)]
    right = [(n + 1) .. (2 * n - 2)]
_________________________
module Spiral (createSpiral) where

import Data.List (transpose)

createSpiral :: Int -> [[Int]]
createSpiral n
    | n >= 1 = cs n n 1
    | otherwise = []
    where
        cs :: Int -> Int -> Int -> [[Int]]
        cs 0 _ _ = [[]]
        cs w h x = [x..x+w-1] : rot90 (cs (h-1) w (x+w))
        rot90 = (map reverse) . transpose
_________________________
module Spiral (createSpiral) where

createSpiral :: Int -> [[Int]]
createSpiral n | n < 1 = []
createSpiral 1 = [[1]]
createSpiral n = [1 .. n] : map reverse (zipWith (:) [n + 1 .. x] corner)
  where
    x = 2*n - 1
    corner = reverse $ map (map (+x)) $ createSpiral (n - 1)
