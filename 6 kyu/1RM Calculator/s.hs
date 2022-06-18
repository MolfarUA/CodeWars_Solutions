595bbea8a930ac0b91000130

module Calculate1RM where

type Weight = Int
type Reps = Int

calculate1RM :: Weight -> Reps -> Weight
calculate1RM w r
  | r == 0 = 0
  | r == 1 = w
  | otherwise = round $ max l $ max e m
  where w' = fromIntegral w
        r' = fromIntegral r
        e = w' * (1+ (r'/30))
        m = (100*w')/(101.3 - 2.67123 * r')
        l = w' * r'**0.1
_______________________________
module Calculate1RM where

type Weight = Int
type Reps = Int

calculate1RM :: Weight -> Reps -> Weight
calculate1RM _ 0 = 0
calculate1RM w 1 = w
calculate1RM w r = round (maximum [epley, mcGlothin, lombardi]) where
  w' = fromIntegral w
  r' = fromIntegral r
  epley = w' * (1 + r' / 30)
  mcGlothin = 100 * w' / (101.3 - 2.67123 * r')
  lombardi = w' * r' ** 0.1
_______________________________
module Calculate1RM where

type Weight = Int
type Reps = Int

calculate1RM :: Weight -> Reps -> Weight
calculate1RM w r | r == 0    = 0
                 | r == 1    = w
                 | otherwise = round $ maximum [b * a**0.1, b * (1.0 + a / 30.0), 100 * b / (101.3 - 2.67123 * a)]
                  where
                  a = fromIntegral r
                  b = fromIntegral w
_______________________________
module Calculate1RM where

type Weight = Int
type Reps = Int

calculate1RM :: Weight -> Reps -> Weight
calculate1RM w 0 = 0
calculate1RM w 1 = w
calculate1RM w r = round $ maximum $ map (\f -> f (fromIntegral w) (fromIntegral r)) [f1, f2, f3]

f1 :: Double -> Double -> Double
f1 w r = w * (1 + r / 30)

f2 :: Double -> Double -> Double
f2 w r = 100 * w / (101.3 - 2.67123 * r)

f3 :: Double -> Double -> Double
f3 w r = w * (r ** 0.1)
_______________________________
module Calculate1RM where

type Weight = Int
type Reps = Int

calculate1RM :: Weight -> Reps -> Weight
calculate1RM _ 0 = 0
calculate1RM w 1 = w
calculate1RM w r = maximum [epiley, mcGlothin, lombardi] where
    epiley = round . (*(fromIntegral w)) . (+1) . (/30) . fromIntegral $ r
    mcGlothin = round $ (fromIntegral (100*w)) / (101.3 - 2.67123 * (fromIntegral r))
    lombardi = round $ (fromIntegral w) * (fromIntegral r) ** 0.1 
