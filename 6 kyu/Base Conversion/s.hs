module BaseConversion where

import Data.List (genericLength, elemIndex, unfoldr)
import Data.Maybe (fromJust)

newtype Alphabet = Alphabet { getDigits :: [Char] } deriving (Show)

convert :: Alphabet -> Alphabet -> String -> String
convert (Alphabet a) (Alphabet b) = fromDec (Alphabet b) . toDec (Alphabet a)

toDec :: Alphabet -> String -> Integer
toDec (Alphabet a) = foldl (\r d -> r * genericLength a + (toInteger . fromJust . elemIndex d $ a)) 0

fromDec :: Alphabet -> Integer -> String
fromDec (Alphabet a) 0 = [head a]
fromDec (Alphabet a) n = map (a!!) . reverse . unfoldr digit $ n
    where   digit 0 = Nothing
            digit n = let (d, m) = divMod n (genericLength a) in Just (fromInteger m, d)
__________________________________________
module BaseConversion where
import Data.List (elemIndex, genericLength, unfoldr)
import Data.Maybe (fromJust)

newtype Alphabet = Alphabet { getDigits :: [Char] } deriving (Show)

convert :: Alphabet -> Alphabet -> String -> String
convert a b = format b . parse a 

parse :: Alphabet -> String -> Integer
parse (Alphabet a) = foldl step 0
  where 
    step n c = len * n + (fromIntegral $ fromJust $ elemIndex c a)
    len      = genericLength a

format :: Alphabet -> Integer -> String
format (Alphabet a) 0 = [head a]
format (Alphabet a) n = reverse $ unfoldr step n
  where
    step 0 = Nothing
    step n = Just (a !! fromIntegral (n `mod` len), n `div` len)
    len    = genericLength a
__________________________________________
module BaseConversion where

import Data.List
import Data.Maybe
import Numeric

newtype Alphabet = Alphabet { getDigits :: [Char] } deriving (Show)

convert :: Alphabet -> Alphabet -> String -> String
convert (Alphabet a) (Alphabet b) = to . from
  where
    to = ($ "") . showIntAtBase (genericLength b) (b !!)
    from = fst . head . readInt (genericLength a) (flip elem a) (fromJust . flip elemIndex a)
