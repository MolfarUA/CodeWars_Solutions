module ISO where

import Data.Maybe
import Data.Void
-- A type of `Void` have no value.
-- So it is impossible to construct `Void`,
-- unless using undefined, error, unsafeCoerce, infinite recursion, etc
-- And there is a function
-- absurd :: Void -> a
-- That get any value out of `Void`
-- We can do this becuase we can never have void in the zeroth place.

-- so, when are two type, `a` and `b`, considered equal?
-- a definition might be, it is possible to go from `a` to `b`,
-- and from `b` to `a`.
-- Going a roundway trip should leave you the same value.
-- Unfortunately it is virtually impossible to test this in Haskell.
-- This is called Isomorphism.

type ISO a b = (a -> b, b -> a)

-- given ISO a b, we can go from a to b
substL :: ISO a b -> (a -> b)
substL = fst

-- and vice versa
substR :: ISO a b -> (b -> a)
substR = snd

-- There can be more than one ISO a b
isoBool :: ISO Bool Bool
isoBool = (id, id)

isoBoolNot :: ISO Bool Bool
isoBoolNot = (not, not)

-- isomorphism is reflexive
refl :: ISO a a
refl = (id, id)

-- isomorphism is symmetric
symm :: ISO a b -> ISO b a
symm (ab, ba) = (ba, ab)

-- isomorphism is transitive
trans :: ISO a b -> ISO b c -> ISO a c
trans (ab, ba) (bc, cb) = (bc . ab, ba . cb)

-- We can combine isomorphism:
isoTuple :: ISO a b -> ISO c d -> ISO (a, c) (b, d)
isoTuple (ab, ba) (cd, dc) = 
  (\(a, c) -> (ab a, cd c), \(b, d) -> (ba b, dc d))

isoList :: ISO a b -> ISO [a] [b]
isoList (ab, ba) = (map ab, map ba)

isoMaybe :: ISO a b -> ISO (Maybe a) (Maybe b)
isoMaybe (ab, ba) = (fmap ab, fmap ba)

isoEither :: ISO a b -> ISO c d -> ISO (Either a c) (Either b d)
isoEither (ab, ba) (cd, dc) = (left, right)
  where
    left  (Left  a) = Left  (ab a)
    left  (Right c) = Right (cd c)
    right (Left  b) = Left  (ba b)
    right (Right d) = Right (dc d)

isoFunc :: ISO a b -> ISO c d -> ISO (a -> c) (b -> d)
isoFunc (ab, ba) (cd, dc) = (\f -> cd . f . ba, \g -> dc . g . ab)

-- Going another way is hard (and is generally impossible)
isoUnMaybe :: ISO (Maybe a) (Maybe b) -> ISO a b
isoUnMaybe m@(mamb, mbma) = 
  (\a -> get $ mamb $ Just a, substL $ isoUnMaybe $ symm m)
  where
    get (Just b) = b
    get Nothing = fromJust (mamb Nothing)
    -- Suppose mamb return Nothing
    -- Since mamb (Just a) is Nothing, mbma Nothing is Just a.
    -- Since mamb Nothing, mbma Nothing is Nothing
    -- mbma Nothing can only be Just a, or Nothing, but cannot be both!
    -- So there is a contraidction, this case is impossible.

-- We cannot have
-- isoUnEither :: ISO (Either a b) (Either c d) -> ISO a c -> ISO b d.
-- Note that we have
isoEU :: ISO (Either [()] ()) (Either [()] Void)
isoEU = (left, right)
  where
    left  (Left     l)  = Left  (():l)
    left  (Right    _)  = Left  []
    right (Left    [])  = Right ()
    right (Left (_:l))  = Left  l
    right (Right    v)  = absurd v -- absurd :: Void -> a
-- where (), the empty tuple, has 1 value, and Void has 0 value
-- If we have isoUnEither,
-- We have ISO () Void by calling isoUnEither isoEU
-- That is impossible, since we can get a Void by substL on ISO () Void
-- So it is impossible to have isoUnEither

-- And we have isomorphism on isomorphism!
isoSymm :: ISO (ISO a b) (ISO b a)
isoSymm = (symm, symm)

-- Sometimes, we can treat a Type as a Number:
-- if a Type t has n distinct value, it's Number is n.
-- This is formally called cardinality.
-- See https://en.wikipedia.org/wiki/Cardinality

-- Void has cardinality of 0 (we will abreviate it Void is 0).
-- () is 1.
-- Bool is 2.
-- Maybe a is 1 + a.
-- We will be using peano arithmetic so we will write it as S a.
-- https://en.wikipedia.org/wiki/Peano_axioms
-- Either a b is a + b.
-- (a, b) is a * b.
-- a -> b is b ^ a. Try counting (() -> Bool) and (Bool -> ())

-- Algebraic data type got the name because
-- it satisfies a lot of algebraic rules under isomorphism

-- a = b -> c = d -> a * c = b * d
isoProd :: ISO a b -> ISO c d -> ISO (a, c) (b, d)
isoProd = isoTuple

-- a = b -> c = d -> a + c = b + d
isoPlus :: ISO a b -> ISO c d -> ISO (Either a c) (Either b d)
isoPlus = isoEither

-- a = b -> S a = S b
isoS :: ISO a b -> ISO (Maybe a) (Maybe b)
isoS = isoMaybe

-- a = b -> c = d -> c ^ a = d ^ b
isoPow :: ISO a b -> ISO c d -> ISO (a -> c) (b -> d)
isoPow = isoFunc

-- a + b = b + a
plusComm :: ISO (Either a b) (Either b a)
plusComm = (swap, swap)
  where
    swap (Left a) = Right a
    swap (Right a) = Left a

-- a + b + c = a + (b + c)
plusAssoc :: ISO (Either (Either a b) c) (Either a (Either b c))
plusAssoc = (left, right)
  where
    left  (Left  (Left  a)) = Left         a
    left  (Left  (Right b)) = Right (Left  b)
    left  (Right        c)  = Right (Right c)
    right (Left         a)  = Left  (Left  a)
    right (Right (Left  b)) = Left  (Right b)
    right (Right (Right c)) = Right        c

-- a * b = b * a
multComm :: ISO (a, b) (b, a)
multComm = (swap, swap)
  where
    swap (a, b) = (b, a)

-- a * b * c = a * (b * c)
multAssoc :: ISO ((a, b), c) (a, (b, c))
multAssoc = (\((a, b), c) -> (a, (b, c)), \(a, (b, c)) -> ((a, b), c))

-- dist :: a * (b + c) = a * b + a * c
dist :: ISO (a, (Either b c)) (Either (a, b) (a, c))
dist = (left, right)
  where
    left  (a, Left    b) = Left  (a, b)
    left  (a, Right   c) = Right (a, c)
    right (Left  (a, b)) = (a, Left  b)
    right (Right (a, c)) = (a, Right c)

-- (c ^ b) ^ a = c ^ (a * b)
curryISO :: ISO (a -> b -> c) ((a, b) -> c)
curryISO = (\f (a, b) -> f a b, \f a b -> f (a, b))

-- 1 = S O (we are using peano arithmetic)
one :: ISO () (Maybe Void)
one = (const Nothing, const ())

-- 2 = S (S O)
two :: ISO Bool (Maybe (Maybe Void))
two = (left, right)
  where
    left False     = Nothing
    left True      = Just Nothing
    right Nothing  = False
    right (Just _) = True

-- O + b = b
plusO :: ISO (Either Void b) b
plusO = (left, Right)
  where
    left (Left  x) = absurd x -- absurd :: Void -> a
    left (Right x) = x

-- S a + b = S (a + b)
plusS :: ISO (Either (Maybe a) b) (Maybe (Either a b))
plusS = (left, right)
  where
    left  (Left  (Just a)) = Just (Left  a)
    left  (Left   Nothing) = Nothing
    left  (Right        b) = Just (Right b)
    right          Nothing = Left   Nothing
    right (Just (Left  a)) = Left (Just  a)
    right (Just (Right b)) = Right        b

-- 1 + b = S b
plusSO :: ISO (Either () b) (Maybe b)
plusSO = isoPlus one refl `trans` plusS `trans` isoS plusO

-- O * a = O
multO :: ISO (Void, a) Void
multO = (absurd . fst, absurd)

-- S a * b = b + a * b
multS :: ISO (Maybe a, b) (Either b (a, b))
multS = (left, right)
  where
    left  (Nothing,   b) = Left      b
    left  (Just  a,   b) = Right (a, b)
    right (Left       b) = (Nothing, b)
    right (Right (a, b)) = (Just  a, b)

-- 1 * b = b
multSO :: ISO ((), b) b
multSO =
  isoProd one refl `trans`
    multS `trans`
    isoPlus refl multO `trans` 
    plusComm `trans`
    plusO

-- a ^ O = 1
powO :: ISO (Void -> a) ()
powO = (const (), const absurd)

-- a ^ (S b) = a * (a ^ b)
powS :: ISO (Maybe b -> a) (a, b -> a)
powS = (\f -> (f Nothing, f . Just), right)
  where
    right (a, f)  Nothing = a
    right (a, f) (Just b) = f b

-- a ^ 1 = a
powSO :: ISO (() -> a) a
powSO = 
  isoPow one refl `trans` 
    powS `trans`
    isoProd refl powO `trans`
    multComm `trans`
    multSO
________________________________________________
module ISO where

import Control.Monad (join)
import Data.Maybe (fromJust, fromMaybe)
import Data.Function ((&))
import Data.Bifunctor (bimap)
import Data.Void

type ISO a b = (a -> b, b -> a)

substL :: ISO a b -> (a -> b)
substL = fst

substR :: ISO a b -> (b -> a)
substR = snd

isoBool :: ISO Bool Bool
isoBool = (id, id)

isoBoolNot :: ISO Bool Bool
isoBoolNot = (not, not)

refl :: ISO a a
refl = (id, id)

symm :: ISO a b -> ISO b a
symm (ab, ba) = (ba, ab)

trans :: ISO a b -> ISO b c -> ISO a c
trans (ab, ba) (bc, cb) = (bc . ab, ba . cb)

isoTuple :: ISO a b -> ISO c d -> ISO (a, c) (b, d)
isoTuple (ab, ba) (cd, dc) = 
  (\(a, c) -> (ab a, cd c), \(b, d) -> (ba b, dc d))

isoList :: ISO a b -> ISO [a] [b]
isoList (ab, ba) = (map ab, map ba)

isoMaybe :: ISO a b -> ISO (Maybe a) (Maybe b)
isoMaybe (ab, ba) = (fmap ab, fmap ba)

isoEither :: ISO a b -> ISO c d -> ISO (Either a c) (Either b d)
isoEither (ab, ba) (cd, dc) = (bimap ab cd, bimap ba dc)

isoFunc :: ISO a b -> ISO c d -> ISO (a -> c) (b -> d)
isoFunc (ab, ba) (cd, dc) = (\ac -> cd . ac . ba, \bd -> dc . bd . ab)

isoUnMaybe :: ISO (Maybe a) (Maybe b) -> ISO a b
isoUnMaybe (ab, ba) =
  ( fromMaybe (fromJust $ ab Nothing) . ab . Just
  , fromMaybe (fromJust $ ba Nothing) . ba . Just)

isoEU :: ISO (Either [()] ()) (Either [()] Void)
isoEU = (f, g)
  where
    f (Left xs) = Left (() : xs)
    f (Right ()) = Left []
    g (Left []) = Right ()
    g (Left (_:xs)) = Left xs
    
isoSymm :: ISO (ISO a b) (ISO b a)
isoSymm = (symm, symm)
-- Please copy your code of Isomorphism to here.

-- Sometimes, we can treat a Type as a Number:
-- if a Type t has n distinct value, it's Number is n.
-- This is formally called cardinality.
-- See https://en.wikipedia.org/wiki/Cardinality

-- Void has cardinality of 0 (we will abbreviate it Void is 0).
-- () is 1.
-- Bool is 2.
-- Maybe a is 1 + a.
-- We will be using peano arithmetic so we will write it as S a.
-- https://en.wikipedia.org/wiki/Peano_axioms
-- Either a b is a + b.
-- (a, b) is a * b.
-- a -> b is b ^ a. Try counting (() -> Bool) and (Bool -> ())

-- Algebraic data type got the name because
-- it satisfies a lot of algebraic rules under isomorphism

-- a = b -> c = d -> a * c = b * d
isoProd :: ISO a b -> ISO c d -> ISO (a, c) (b, d)
isoProd = isoTuple

-- a = b -> c = d -> a + c = b + d
isoPlus :: ISO a b -> ISO c d -> ISO (Either a c) (Either b d)
isoPlus = isoEither

-- a = b -> S a = S b
isoS :: ISO a b -> ISO (Maybe a) (Maybe b)
isoS = isoMaybe

-- a = b -> c = d -> c ^ a = d ^ b
isoPow :: ISO a b -> ISO c d -> ISO (a -> c) (b -> d)
isoPow = isoFunc

-- a + b = b + a
plusComm :: ISO (Either a b) (Either b a)
plusComm = (f, f)
  where
    f (Left x) = Right x
    f (Right x) = Left x

-- a + b + c = a + (b + c)
plusAssoc :: ISO (Either (Either a b) c) (Either a (Either b c))
plusAssoc = (f, g)
  where
    f (Left (Left a)) = Left a
    f (Left (Right b)) = Right (Left b)
    f (Right c) = Right (Right c)
    g (Left a) = Left (Left a)
    g (Right (Left b)) = Left (Right b)
    g (Right (Right c)) = Right c

-- a * b = b * a
multComm :: ISO (a, b) (b, a)
multComm = (swap, swap)
  where
    swap (x, y) = (y, x)

-- a * b * c = a * (b * c)
multAssoc :: ISO ((a, b), c) (a, (b, c))
multAssoc = (f, g)
  where
    f ((a, b), c) = (a, (b, c))
    g (a, (b, c)) = ((a, b), c)

-- dist :: a * (b + c) = a * b + a * c
dist :: ISO (a, (Either b c)) (Either (a, b) (a, c))
dist = (f, g)
  where
    f (a, Left b) = Left (a, b)
    f (a, Right c) = Right (a, c)
    g (Left (a, b)) = (a, Left b)
    g (Right (a, c)) = (a, Right c)

-- (c ^ b) ^ a = c ^ (a * b)
curryISO :: ISO (a -> b -> c) ((a, b) -> c)
curryISO = (uncurry, curry)

-- 1 = S O (we are using peano arithmetic)
-- https://en.wikipedia.org/wiki/Peano_axioms
one :: ISO () (Maybe Void)
one = (const Nothing, const ())

-- 2 = S (S O)
two :: ISO Bool (Maybe (Maybe Void))
two = (f, g)
  where
    f True = Just Nothing
    f False = Nothing
    g Nothing = False
    g (Just Nothing) = True
    g (Just (Just v)) = absurd v

-- O + b = b
plusO :: ISO (Either Void b) b
plusO = (left, Right)
  where
    left (Left  x) = absurd x
    left (Right x) = x

-- S a + b = S (a + b)
plusS :: ISO (Either (Maybe a) b) (Maybe (Either a b))
plusS = (f, g)
  where
    f (Left Nothing) = Nothing
    f (Left (Just a)) = Just (Left a)
    f (Right b) = Just (Right b)
    g Nothing = Left Nothing
    g (Just (Left a)) = Left (Just a)
    g (Just (Right b)) = Right b

-- 1 + b = S b
plusSO :: ISO (Either () b) (Maybe b)
plusSO = isoPlus one refl `trans` plusS `trans` isoS plusO

-- O * a = O
multO :: ISO (Void, a) Void
multO = (absurd . fst, absurd)

-- S a * b = b + a * b
multS :: ISO (Maybe a, b) (Either b (a, b))
multS = (f, g)
  where
    f (ma, b) = case ma of
      Just a -> Right (a, b)
      Nothing -> Left b
    g (Left b) = (Nothing, b)
    g (Right (a, b)) = (Just a, b)

-- 1 * b = b
multSO :: ISO ((), b) b
multSO =
  isoProd one refl `trans`
    multS `trans`
    isoPlus refl multO `trans` 
    plusComm `trans`
    plusO

-- a ^ O = 1
powO :: ISO (Void -> a) ()
powO = (const (), const absurd)

-- a ^ (S b) = a * (a ^ b)
powS :: ISO (Maybe b -> a) (a, b -> a)
powS = (f, g)
  where
    f mba = (mba Nothing, mba . Just)
    g (a, ba) = maybe a ba

-- a ^ 1 = a
-- Go the hard way (like multSO, plusSO)
-- to prove that you really get what is going on!
powSO :: ISO (() -> a) a
powSO = (($ ()), const)
-- Here's a trick: 
-- replace undefined with the rhs of the comment on previous line
-- When you're not sure what to fill in for a value,
-- Have it as a _
-- GHC will goes like
-- "Found hole `_' with type: ISO (() -> a) (Maybe b0 -> a0)"
-- So you can immediately see value of what type are needed
-- This process can be repeat indefinitely -
-- For example you might replace `_` with `isoFunc _ _`
-- So GHC hint you on more specific type.
-- This is especially usefull if you have complex type.
-- See https://wiki.haskell.org/GHC/Typed_holes
-- And "stepwise refinement" for more details.
__________________________________________________________________
{-# LANGUAGE LambdaCase #-}
{-# OPTIONS_GHC -Wall -Werror #-}

module ISO where

import Control.Arrow ((***))
import Data.Bifunctor (bimap)
import Data.Bool (bool)
import Data.Tuple (swap)
import Data.Void (Void, absurd)

-- Please copy your code of Isomorphism to here.

type ISO a b = (a -> b, b -> a)

substL :: ISO a b -> (a -> b)
substL = fst

substR :: ISO a b -> (b -> a)
substR = snd

isoBool :: ISO Bool Bool
isoBool = (id, id)

isoBoolNot :: ISO Bool Bool
isoBoolNot = (not, not)

refl :: ISO a a
refl = (id, id)

symm :: ISO a b -> ISO b a
symm = swap

trans :: ISO a b -> ISO b c -> ISO a c
trans (a,b) (c,d) = (c . a, b . d)

isoTuple :: ISO a b -> ISO c d -> ISO (a, c) (b, d)
isoTuple (a,b) (c,d) = (a *** c, b *** d)

isoList :: ISO a b -> ISO [a] [b]
isoList = fmap *** fmap

isoMaybe :: ISO a b -> ISO (Maybe a) (Maybe b)
isoMaybe = fmap *** fmap

isoEither :: ISO a b -> ISO c d -> ISO (Either a c) (Either b d)
isoEither (a,b) (c,d) = (bimap a c, bimap b d)

isoFunc :: ISO a b -> ISO c d -> ISO (a -> c) (b -> d)
isoFunc (a,b) (c,d) = ((c .) . (. b), (d .) . (. a))

isoUnMaybe :: ISO (Maybe a) (Maybe b) -> ISO a b
isoUnMaybe (a,b) = (m,n)
 where
  m x = case a (Just x) of
    Just u -> u
    Nothing -> case a Nothing of
      Just u -> u
      Nothing -> undefined
  n x = case b (Just x) of
    Just u -> u
    Nothing -> case b Nothing of
      Just u -> u
      Nothing -> undefined

isoEU :: ISO (Either [()] ()) (Either [()] Void)
isoEU =
  ( fmap Left (():) `either` const (Left [])
  , \case
      Left [] -> Right ()
      Left (_:xs) -> Left xs
      Right x -> absurd x
  )

isoSymm :: ISO (ISO a b) (ISO b a)
isoSymm = (swap, swap)

-- Algebraic data type got the name because
-- it satisfies a lot of algebraic rules under isomorphism

-- a = b -> c = d -> a * c = b * d
isoProd :: ISO a b -> ISO c d -> ISO (a, c) (b, d)
isoProd = isoTuple

-- a = b -> c = d -> a + c = b + d
isoPlus :: ISO a b -> ISO c d -> ISO (Either a c) (Either b d)
isoPlus = isoEither

-- a = b -> S a = S b
isoS :: ISO a b -> ISO (Maybe a) (Maybe b)
isoS = isoMaybe

-- a = b -> c = d -> c ^ a = d ^ b
isoPow :: ISO a b -> ISO c d -> ISO (a -> c) (b -> d)
isoPow = isoFunc

-- a + b = b + a
plusComm :: ISO (Either a b) (Either b a)
plusComm = (either Right Left, either Right Left)

-- a + b + c = a + (b + c)
plusAssoc :: ISO (Either (Either a b) c) (Either a (Either b c))
plusAssoc =
  ( either (either Left (Right . Left)) (Right . Right)
  , either (Left . Left) (either (Left . Right) Right)
  )

-- a * b = b * a
multComm :: ISO (a, b) (b, a)
multComm = (swap, swap)

-- a * b * c = a * (b * c)
multAssoc :: ISO ((a, b), c) (a, (b, c))
multAssoc = (\((a,b),c) -> (a, (b, c)), \(a,(b,c)) -> ((a, b), c))

-- dist :: a * (b + c) = a * b + a * c
dist :: ISO (a, (Either b c)) (Either (a, b) (a, c))
dist = (f, g)
 where
  f (a,Left b) = Left (a, b)
  f (a,Right c) = Right (a, c)
  g (Left (a,b)) = (a, Left b)
  g (Right (a,c)) = (a, Right c)

-- (c ^ b) ^ a = c ^ (a * b)
curryISO :: ISO (a -> b -> c) ((a, b) -> c)
curryISO = (uncurry, curry)

-- 1 = S O (we are using peano arithmetic)
-- https://en.wikipedia.org/wiki/Peano_axioms
one :: ISO () (Maybe Void)
one = (const Nothing, const ())

-- 2 = S (S O)
two :: ISO Bool (Maybe (Maybe Void))
two = (bool Nothing (Just Nothing), maybe False (const True))

-- O + b = b
plusO :: ISO (Either Void b) b
plusO = (either absurd id, Right)

-- S a + b = S (a + b)
plusS :: ISO (Either (Maybe a) b) (Maybe (Either a b))
plusS =
  ( either (maybe Nothing (Just . Left)) (Just . Right)
  , maybe (Left Nothing) (either (Left . Just) Right)
  )

-- 1 + b = S b
plusSO :: ISO (Either () b) (Maybe b)
plusSO = (one `isoPlus` refl)
  `trans` plusS
  `trans` isoS plusO

-- O * a = O
multO :: ISO (Void, a) Void
multO = (fst, absurd)

-- S a * b = b + a * b
multS :: ISO (Maybe a, b) (Either b (a, b))
multS = (f, g)
 where
  f (Nothing,b) = Left b
  f (Just a,b) = Right (a, b)
  g (Left b) = (Nothing, b)
  g (Right (a,b)) = (Just a, b)

-- 1 * b = b
multSO :: ISO ((), b) b
multSO = (one `isoProd` refl)
  `trans` multS
  `trans` (refl `isoPlus` multO)
  `trans` plusComm
  `trans` plusO

-- a ^ O = 1
powO :: ISO (Void -> a) ()
powO = (const (), const absurd)

-- a ^ (S b) = a * (a ^ b)
powS :: ISO (Maybe b -> a) (a, b -> a)
powS = (\f -> (f Nothing, f . Just), uncurry maybe)

-- a ^ 1 = a
powSO :: ISO (() -> a) a
powSO = (one `isoPow` refl)
  `trans` powS
  `trans` (refl `isoProd` powO)
  `trans` multComm
  `trans` multSO
____________________________________________
{-# LANGUAGE TupleSections #-}

module ISO where

import Data.Bool (bool)
import Data.Void (Void, absurd)
import Data.Tuple (swap)
import Data.Maybe (isJust)
import Data.Bifunctor (bimap, first, second)

type ISO a b = (a -> b, b -> a)

substL :: ISO a b -> (a -> b)
substL = fst

substR :: ISO a b -> (b -> a)
substR = snd

refl :: ISO a a
refl = (id, id)

symm :: ISO a b -> ISO b a
symm (ab, ba) = (ba, ab)

trans :: ISO a b -> ISO b c -> ISO a c
trans (ab, ba) (bc, cb) = (bc . ab, ba . cb)

isoTuple :: ISO a b -> ISO c d -> ISO (a, c) (b, d)
isoTuple (ab, ba) (cd, dc) = (bimap ab cd, bimap ba dc)

isoEither :: ISO a b -> ISO c d -> ISO (Either a c) (Either b d)
isoEither (ab, ba) (cd, dc) = (bimap ab cd, bimap ba dc)

isoMaybe :: ISO a b -> ISO (Maybe a) (Maybe b)
isoMaybe (ab, ba) = ((ab <$>), (ba <$>))

isoFunc :: ISO a b -> ISO c d -> ISO (a -> c) (b -> d)
isoFunc (ab, ba) (cd, dc) = (\ac -> cd . ac . ba, \bd -> dc . bd . ab)

isoList :: ISO a b -> ISO [a] [b]
isoList (ab, ba) = ((ab <$>), (ba <$>))

isoSymm :: ISO (ISO a b) (ISO b a)
isoSymm = (symm, symm)

-- a = b -> c = d -> a * c = b * d
isoProd :: ISO a b -> ISO c d -> ISO (a, c) (b, d)
isoProd = isoTuple

-- a = b -> c = d -> a + c = b + d
isoPlus :: ISO a b -> ISO c d -> ISO (Either a c) (Either b d)
isoPlus = isoEither

-- a = b -> S a = S b
isoS :: ISO a b -> ISO (Maybe a) (Maybe b)
isoS = isoMaybe

-- a = b -> c = d -> c ^ a = d ^ b
isoPow :: ISO a b -> ISO c d -> ISO (a -> c) (b -> d)
isoPow = isoFunc

-- a + b = b + a
plusComm :: ISO (Either a b) (Either b a)
plusComm = (either Right Left, either Right Left)

-- a + b + c = a + (b + c)
plusAssoc :: ISO (Either (Either a b) c) (Either a (Either b c))
plusAssoc = (either (second Left) (Right . Right), either (Left . Left) (first Right))

-- a * b = b * a
multComm :: ISO (a, b) (b, a)
multComm = (swap, swap)

-- a * b * c = a * (b * c)
multAssoc :: ISO ((a, b), c) (a, (b, c))
multAssoc = (\((a, b), c) -> (a, (b, c)), \(a, (b, c)) -> ((a, b), c))

-- a * (b + c) = a * b + a * c
dist :: ISO (a, (Either b c)) (Either (a, b) (a, c))
dist = (\(a, e) -> bimap (a,) (a,) e, either (second Left) (second Right))

-- (c ^ b) ^ a = c ^ (a * b)
curryISO :: ISO (a -> b -> c) ((a, b) -> c)
curryISO = (uncurry, curry)

-- 1 = S O (we are using peano arithmetic)
one :: ISO () (Maybe Void)
one = (const Nothing, const ())

-- 2 = S (S O)
two :: ISO Bool (Maybe (Maybe Void))
two = (bool Nothing (Just Nothing), isJust)

-- O + b = b
plusO :: ISO (Either Void b) b
plusO = (either absurd id, Right)

-- S a + b = S (a + b)
plusS :: ISO (Either (Maybe a) b) (Maybe (Either a b))
plusS = (either (Left <$>) (Just . Right), maybe (Left Nothing) (first Just))

-- 1 + b = S b
plusSO :: ISO (Either () b) (Maybe b)
plusSO = (either (const Nothing) Just, maybe (Left ()) Right)
-- plusSO = isoPlus one refl `trans` || 1 + b = S O + b
--            plusS `trans`          ||       = S (O + b)
--            isoS plusO             ||       = S b

-- O * a = O
multO :: ISO (Void, a) Void
multO = (fst, absurd)

-- S a * b = b + a * b
multS :: ISO (Maybe a, b) (Either b (a, b))
multS = (\(m, b) -> maybe (Left b) (Right . (,b)) m, either (Nothing,) (first Just))
        
-- 1 * b = b
multSO :: ISO ((), b) b
multSO = (snd, ((),))
-- multSO = isoProd one refl `trans`     || 1 * b = S O * b
--            multS `trans`              ||       = b + O * b
--            isoPlus refl multO `trans` ||       = b + O
--            plusComm `trans`           ||       = O + b
--            plusO                      ||       = b

-- a ^ O = 1
powO :: ISO (Void -> a) ()
powO = (const (), const absurd)

-- a ^ (S b) = a * (a ^ b)
powS :: ISO (Maybe b -> a) (a, b -> a)
powS = (\f -> (f Nothing, f . Just), uncurry maybe)

-- a ^ 1 = a
powSO :: ISO (() -> a) a
powSO = (\f -> f (), const)
-- powSO = isoPow one refl `trans`     || a ^ 1 = a ^ (S O)
--           powS `trans`              ||       = a * (a ^ O)
--           isoProd refl powO `trans` ||       = a * 1
--           multComm `trans`          ||       = 1 * a
--           multSO                    ||       = a
