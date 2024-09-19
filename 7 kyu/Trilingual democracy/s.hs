
module TrilingualDemocracy (trilingualDemocracy) where

trilingualDemocracy :: [Char] -> Char
trilingualDemocracy (first:second:third:group) =
  if (first == second && second == third) then first
  else if (first == second) then third
  else if (second == third) then first
  else if (first == third) then second
  else let full = ['D','F','I','K'] in
          head (filter (/= third) (filter (/= second) (filter (/= first) full)))

____________________
module TrilingualDemocracy (trilingualDemocracy) where

import Data.List (sort, nub, (\\))

trilingualDemocracy :: [Char] -> Char
trilingualDemocracy s = case (length $ nub t, t) of
                        (1, (x:_)) -> x
                        (2, [x, y, z]) -> if x == y then z else x
                        (3, xs) -> head $ "DFIK" \\ xs
                        where t = sort s
________________
module TrilingualDemocracy (trilingualDemocracy) where

import Data.List ((\\))

trilingualDemocracy :: [Char] -> Char
trilingualDemocracy [x, y, z] 
  | x == y    = z                           -- AAA or AAB
  | y == z    = x                           -- ABB
  | z == x    = y                           -- ABA
  | otherwise = head ("DFIK" \\ [x, y, z])  -- ABC
