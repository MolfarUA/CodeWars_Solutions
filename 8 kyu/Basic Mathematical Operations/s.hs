module BasicMathematicalOperations (basicOp) where

basicOp :: Char -> Int -> Int -> Int
basicOp '+' = (+)
basicOp '-' = (-)
basicOp '*' = (*)
basicOp '/' = div
________________________________
module BasicMathematicalOperations (basicOp) where

basicOp :: Char -> Int -> Int -> Int
basicOp char a b
    | char == '+' = a + b
    | char == '-' = a - b
    | char == '*' = a * b
    | char == '/' = div a b
    | otherwise = error "Wrong Input"
________________________________
module BasicMathematicalOperations (basicOp) where
import qualified Data.Map as Map
import Data.Maybe

ops :: Map.Map Char (Int -> Int -> Int)
ops = Map.fromList [('+', (+)), ('-', (-)), ('*', (*)), ('/', div)]

basicOp :: Char -> Int -> Int -> Int
basicOp op a b = action a b
  where action = fromJust $ Map.lookup op ops
________________________________
module BasicMathematicalOperations (basicOp) where

basicOp :: Char -> Int -> Int -> Int

basicOp '+' a b = a + b
basicOp '-' a b = a - b
basicOp '*' a b = a * b
basicOp '/' a b = div a  b
basicOp op a b = error "undefined operator"
________________________________
module BasicMathematicalOperations (basicOp) where

basicOp :: Char -> Int -> Int -> Int
basicOp c a b =
  case c of '+' -> a + b
            '-' -> a - b
            '*' -> a * b
            '/' -> div a b
  
