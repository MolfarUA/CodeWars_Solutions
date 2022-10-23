525f3eda17c7cd9f9e000b39


module CalculatingWithFunctions (plus,minus,times,dividedBy,zero,one,two,three,four,five,six,seven,eight,nine) where

plus x = x (+)
minus x = x (flip (-))
times x = x (*)
dividedBy x = x (flip div)

zero,one,two,three,four,five,six,seven,eight,nine :: Num t1 => (t1 -> t2) -> t2
zero f = f 0
one f = f 1
two f = f 2
three f = f 3
four f = f 4
five f = f 5
six f = f 6
seven f = f 7
eight f = f 8
nine f = f 9
__________________________
{-# LANGUAGE FlexibleInstances #-}
module CalculatingWithFunctions (plus,minus,times,dividedBy,zero,one,two,three,four,five,six,seven,eight,nine) where

class Lit a where
  zero :: a
  one :: a
  two :: a
  three :: a
  four :: a
  five :: a
  six :: a
  seven :: a
  eight :: a
  nine :: a

instance Lit Int where
  zero = 0
  one = 1
  two = 2
  three = 3
  four = 4
  five = 5
  six = 6
  seven = 7
  eight = 8
  nine = 9

instance Lit ((Int -> Int) -> Int) where
  zero operation = operation 0
  one operation = operation 1
  two operation = operation 2
  three operation = operation 3
  four operation = operation 4
  five operation = operation 5
  six operation = operation 6
  seven operation = operation 7
  eight operation = operation 8
  nine operation = operation 9

plus,minus,times,dividedBy :: Int -> Int -> Int
plus = (+)
minus = flip (-)
times = (*)
dividedBy = flip div
__________________________
module CalculatingWithFunctions (plus,minus,times,dividedBy,zero,one,two,three,four,five,six,seven,eight,nine) where

plus,minus,times,dividedBy :: ((Int -> Int) -> Int) -> (Int -> Int)
plus = \u -> (+(u id))
minus = \u -> subtract (u id)
times = \u -> (*(u id))
dividedBy = \u -> (`div` (u id))

zero,one,two,three,four,five,six,seven,eight,nine :: (Int -> Int) -> Int
zero = \u -> u 0
one = \u -> u 1
two = \u -> u 2
three = \u -> u 3
four = \u -> u 4
five = \u -> u 5
six = \u -> u 6
seven = \u -> u 7
eight = \u -> u 8
nine = \u -> u 9
