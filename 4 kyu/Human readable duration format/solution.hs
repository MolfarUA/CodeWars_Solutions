52742f58faf5485cae000b9a


module FormatDuration where

import Data.Maybe(catMaybes)

formatDuration :: (Integral i) => i -> String
formatDuration n = show (toEnum (fromIntegral n) :: Time)

data Time = Time {
  year :: Int,
  day :: Int,
  hour :: Int,
  minute :: Int,
  second :: Int
} deriving (Eq, Ord)

instance Enum Time where
  fromEnum Time {year=y, day=d, hour=h, minute=m, second=s}
    = 60 * (60 * (24 * (365 * y + d) + h) + m) + s
  toEnum ss = Time y d h m s
    where (ms,s) = ss `divMod` 60
          (hs,m) = ms `divMod` 60
          (ds,h) = hs `divMod` 24
          (y,d) = ds `divMod` 365

instance Show Time where
  show Time {year=y, day=d, hour=h, minute=m, second=s}
    = (toHumanReadable . formatList) [y, d, h, m, s]

toHumanReadable :: [String] -> String
toHumanReadable [] = ""
toHumanReadable [s] = s
toHumanReadable [s1, s2] = s1 ++ " and " ++ s2
toHumanReadable (str:strs) = str ++ ", " ++ toHumanReadable strs

formatList :: [Int] -> [String]
formatList [0, 0, 0, 0, 0] = ["now"]
formatList values = catMaybes $ zipWith showMaybeTimeUnit units values
  where units = ["year", "day", "hour", "minute", "second"]
        showMaybeTimeUnit :: String -> Int -> Maybe String
        showMaybeTimeUnit unit x
          | x <= 0 = Nothing
          | x == 1 = Just (show x ++ " " ++ unit)
          | otherwise = Just (show x ++ " " ++ unit ++ "s")

__________________________________________________
module FormatDuration where

import Text.Printf
import Data.List

formatDuration :: (Integral i) => i -> String
formatDuration n = join $ filter (not . null) ss
  where (ms, s) = divMod n  60
        (hs, m) = divMod ms 60
        (ds, h) = divMod hs 24
        (y , d) = divMod ds 365
        print 0 _ = ""
        print 1 u = "1 " ++ u
        print n u = printf "%d %ss" (fromIntegral n :: Int) u :: String
        ss = zipWith print [y, d, h, m, s] ["year", "day", "hour", "minute", "second"]
        join [] = "now"
        join [s] = s
        join ss = intercalate ", " (init ss) ++ " and " ++ last ss
        
__________________________________________________
module FormatDuration where
import Data.List

show' (0, s) = ""
show' (1, s) = "1 " ++ s
show' (n, s) = show n ++ " " ++ s ++ "s"

formatDuration :: (Integral i, Show i) => i -> String
formatDuration x
          | x == 0     = "now"
          | null init' = last'
          | otherwise  = init' ++ " and " ++ last'
      where divMod' d (x:xs) =  let (l, r) = divMod x d in l : r : xs
            dateParts = foldr divMod' [x] [365,24,60,60]
            namedParts = map show' . zip dateParts $ ["year", "day", "hour", "minute", "second"]
            readableParts = filter (not . null) namedParts
            init' = intercalate ", " . init $ readableParts
            last' = last readableParts
            
__________________________________________________
module FormatDuration where
import Data.List (intercalate)
formatDuration :: (Integral i, Show i) => i -> String
formatDuration n = g $ f [a, b, c, d, e] where
  f xs =
    [if x == 1 then show x ++ y else show x ++ y ++ "s"
    | (x, y) <- zip xs [" year", " day", " hour", " minute", " second"]
    , x /= 0]
  g [] = "now"
  g [x] = x
  g [x, y] = x ++ " and " ++ y
  g xs = g [intercalate ", " $ init xs, last xs]
  (a, b') = divMod n 31536000
  (b, c') = divMod b' 86400
  (c, d') = divMod c' 3600
  (d, e) = divMod d' 60
  
