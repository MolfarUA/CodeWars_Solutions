56c5847f27be2c3db20009c3


module LetsGoCrazy where

subtractSum :: Int -> String
subtractSum = const "apple"
_______________________________________
module LetsGoCrazy where

subtractSum :: Int -> String
subtractSum _ = "apple"
_______________________________________
module LetsGoCrazy where

import Data.Maybe

fruits = [
  (1, "kiwi"), 
  (2, "pear"),
  (3, "kiwi"),
  (4, "banana"),
  (5, "melon"),
  (6, "banana"),
  (7, "melon"),
  (8, "pineapple"),
  (9, "apple")]

subtractSum :: Int -> String
subtractSum = fromMaybe "apple" . flip lookup fruits
