module Codewars.Kata.Plural where
import Codewars.Kata.Plural.Types

plural :: (Num a, Eq a) => a -> Grammar
plural 1 = Singular
plural _ = Plural
__________________
module Codewars.Kata.Plural where
import Codewars.Kata.Plural.Types

plural :: (Num a, Eq a) => a -> Grammar
plural n = if n == 1 then Singular else Plural
__________________
module Codewars.Kata.Plural where
import Codewars.Kata.Plural.Types
import Data.Bool

-- data Grammar = Singular | Plural
plural :: (Num a, Eq a) => a -> Grammar
plural = bool Singular Plural . (/=1)
__________________
{-# Language StandaloneDeriving #-}

module Codewars.Kata.Plural where

import Codewars.Kata.Plural.Types (Grammar(..)) -- data Grammar = Singular | Plural

deriving instance Enum Grammar

plural :: (Num a,Eq a) => a -> Grammar
plural n = toEnum $ fromEnum $ n /= 1
__________________
{-# LANGUAGE LambdaCase #-}

module Codewars.Kata.Plural where
import Codewars.Kata.Plural.Types

-- data Grammar = Singular | Plural
plural :: (Num a, Eq a) => a -> Grammar
plural = \case
  1 -> Singular
  _ -> Plural
