525c65e51bf619685c000059


module Baker where

type Ingredient = String
type Amount     = Int
type Recipe     = [(Ingredient, Amount)]
type Storage    = [(Ingredient, Amount)]

cakes :: Recipe -> Storage -> Int
cakes recipe storage = minimum $ map (\ (w,q) -> maybe 0 (`div` q) $ lookup w storage) recipe
________________________________
module Baker where
import Data.Functor

type Ingredient = String
type Amount     = Int
type Recipe     = [(Ingredient, Amount)]
type Storage    = [(Ingredient, Amount)]

cakes :: Recipe -> Storage -> Int
cakes recipe storage = maybe 0 minimum $ mapM storageQuotient recipe
  where storageQuotient (ingr, reqAmt) = (`div` reqAmt) <$> lookup ingr storage
________________________________
module Baker where

type Ingredient = String
type Amount     = Int
type Recipe     = [(Ingredient, Amount)]
type Storage    = [(Ingredient, Amount)]

bound :: Storage -> (Ingredient, Amount) -> Int
bound s (i, a) = maybe 0 (`div` a) (lookup i s)

cakes :: Recipe -> Storage -> Int
cakes recipe storage = minimum $ map (bound storage) recipe

