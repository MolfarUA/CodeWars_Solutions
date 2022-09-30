55b2549a781b5336c0000103


module Codewars.Exercise.Powers where
import Data.Word
type Power = (Word, Word)

comparePowers :: Power -> Power -> Ordering
comparePowers a b = compare (f a) (f b)
    where f (n, p) = fromIntegral p * log (fromIntegral n)
________________________________
module Codewars.Exercise.Powers where

import Data.Ord (comparing)
import Data.Word (Word(..))

type Power = (Word, Word)

comparePowers :: Power -> Power -> Ordering
comparePowers = comparing $ \(n, p) -> log (fromIntegral n) * fromIntegral p
________________________________
module Codewars.Exercise.Powers where
import Data.Word
import Data.Ord (comparing)
type Power = (Word, Word)

comparePowers :: Power -> Power -> Ordering
comparePowers = comparing logOfPower
  where logOfPower (n, p) = log (fromIntegral n) * fromIntegral p
