5263c6999e0f40dee200059d


module PIN where

subst '0' = "08"
subst '1' = "124"
subst '2' = "1235"
subst '3' = "236"
subst '4' = "1457"
subst '5' = "24568"
subst '6' = "3569"
subst '7' = "478"
subst '8' = "57890"
subst '9' = "689"

getPINs :: String -> [String]
getPINs = mapM subst
______________________________
module PIN where

import Data.Traversable

getPINs :: String -> [String]
getPINs = traverse f where
  f '1' = "124";  f '2' = "1235";  f '3' = "236";
  f '4' = "1457"; f '5' = "24568"; f '6' = "3569";
  f '7' = "478";  f '8' = "57890"; f '9' = "689";
                  f '0' = "08";
______________________________
module PIN where

import Control.Monad (liftM2)

adjacent :: Char -> String 
adjacent '1' = "124"
adjacent '2' = "1235"
adjacent '3' = "236"
adjacent '4' = "1457"
adjacent '5' = "24568"
adjacent '6' = "3569"
adjacent '7' = "478"
adjacent '8' = "57890"
adjacent '9' = "689"
adjacent '0' = "80"

getPINs :: String -> [String]
getPINs = foldr (liftM2 (:) . adjacent) [[]]
