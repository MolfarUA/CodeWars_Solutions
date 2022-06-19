5b853229cfde412a470000d0


module TwiceAsOld where
twice_as_old :: Int -> Int -> Int
twice_as_old father son = abs $ father - 2*son
______________________________
module TwiceAsOld where
twice_as_old :: Int -> Int -> Int
twice_as_old = (abs .).(. (*2)).(-)
______________________________
module TwiceAsOld where

-- x+d=2(y+d)=2y-2d => x-2y=d
twice_as_old :: Int -> Int -> Int
twice_as_old x y = abs $ x-2*y
______________________________
module TwiceAsOld where
twice_as_old :: Int -> Int -> Int
twice_as_old f s = abs $ f - s*2

add :: Int -> Int -> Int
add x y = x + y
______________________________
module TwiceAsOld where

twiceAsOld fatherAge sonAge
  | fatherAge == sonAge * 2 = 0
  | fatherAge > sonAge * 2 = 1 + twiceAsOld (fatherAge - 1) sonAge
  | fatherAge < sonAge * 2 = 1 + twiceAsOld (fatherAge + 1) sonAge


twice_as_old :: Int -> Int -> Int
twice_as_old = twiceAsOld
