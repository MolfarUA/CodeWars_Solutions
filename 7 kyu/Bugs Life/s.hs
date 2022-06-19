5b71af678adeae41df00008c


module BugsLife.Kata (shortestDistance) where

import Data.List

shortestDistance :: Double -> Double -> Double -> Double
shortestDistance a b c =
  let [a', b', c'] = sort [a, b, c]
  in sqrt $ (a' + b')^2 + c'^2
____________________________
module BugsLife.Kata (shortestDistance) where

shortestDistance :: Double -> Double -> Double -> Double
shortestDistance a b c = sqrt (a^2 + b^2 + c^2 + 2 * minimum [a*b, b*c, c*a])
____________________________
module BugsLife.Kata (shortestDistance) where
import Data.List

shortestDistance :: Double -> Double -> Double -> Double
shortestDistance a b c = sqrt $ (s1*s1) + (s2*s2)
  where srt = sort [a,b,c]
        s1 = (srt!!1) + (srt!!0)
        s2 = (srt!!2)
____________________________
module BugsLife.Kata
  ( shortestDistance )
where
import Data.List
  ( sort )

shortestDistance :: Double -> Double -> Double -> Double
shortestDistance sideA sideB sideC = let
  [ sideA' , sideB' , sideC' ] = sort [ sideA , sideB , sideC ]
    :: [ Double ]
  in sqrt
    $ ( sideA' + sideB' ) ^ 2 + sideC' ^ 2
____________________________
module BugsLife.Kata (shortestDistance) where

import Data.List

shortestDistance :: Double -> Double -> Double -> Double
shortestDistance a b c = (*) f $ sqrt (b' * b' + b'' * b'') + sqrt (a' * a' + (c' - b'') * (c' - b''))
  where xs = sort [a, b, c]
        f = head xs
        a' = head xs / head xs
        b' = (head $ tail xs) / head xs
        c' = last xs / head xs
        b'' = a'*b'*c' / (a' + b')
        
-- x / b = (c - x) / a
-- x = b * (c - x) / a
-- x = bc - b/ax
-- x(1 + b/a) = bc
-- x = bc / (1 + b/a) = abc / (a + b)
       
