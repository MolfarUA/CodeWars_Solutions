55225023e1be1ec8bc000390


module Codewars.Kata.Jenny where

greet :: String -> String
greet "Johnny" = "Hello, my love!"
greet name     = "Hello, " ++ name ++ "!"
__________________________________
module Codewars.Kata.Jenny where

import Data.Bool (bool)
import Text.Printf (printf)

greet :: String -> String
greet = ((printf "Hello, %s!") .) . bool id (const "my love") =<< (== "Johnny")
__________________________________
module Codewars.Kata.Jenny where
import Text.Printf
import Data.Bool
greet :: String -> String
greet = printf "Hello, %s!".(bool "my love"<*> (/="Johnny"))
