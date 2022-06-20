57aa218e72292d98d500240f


module HeronsFormula where

heron a b c = sqrt (s*(s-a)*(s-b)*(s-c))
  where s = (a + b + c) / 2.0
________________________
module HeronsFormula where

heron a b c = sqrt $ s * (s - a) * (s - b) * (s - c)
  where
    s = (a + b + c) / 2
________________________
module HeronsFormula where

heron :: Floating a => a -> a -> a -> a
heron a b c = sqrt (s * (s - a) * (s - b) * (s - c))
  where
    s = (a + b + c) / 2
