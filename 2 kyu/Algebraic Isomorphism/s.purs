module AlgebraicIsomorphism where

import Prelude

import Data.Tuple (Tuple(..), fst, snd, swap, uncurry, curry)
import Data.Maybe (Maybe(..), maybe)
import Data.List (List(..), (:))
import Data.Either (Either(..), either)
import Data.Bifunctor (bimap)

type ISO a b = Tuple (a -> b) (b -> a)

substL :: forall a b. ISO a b -> a -> b
substL = fst

substR :: forall a b. ISO a b -> b -> a
substR = snd

isoBoolean :: ISO Boolean Boolean
isoBoolean = Tuple identity identity

isoBooleanNot :: ISO Boolean Boolean
isoBooleanNot = Tuple not not

refl :: forall a. ISO a a
refl = Tuple identity identity

symm :: forall a b. ISO a b -> ISO b a
symm = swap

trans :: forall a b c. ISO a b -> ISO b c -> ISO a c
trans (Tuple ab ba) (Tuple bc cb) = Tuple (bc <<< ab) (ba <<< cb)

isoTuple :: forall a b c d. ISO a b -> ISO c d -> ISO (Tuple a c) (Tuple b d)
isoTuple (Tuple ab ba) (Tuple cd dc) =
  Tuple (\(Tuple a c) -> Tuple (ab a) (cd c)) (\(Tuple b d) -> Tuple (ba b) (dc d))

isoList :: forall a b. ISO a b -> ISO (List a) (List b)
isoList (Tuple ab ba) = Tuple (map ab) (map ba)

isoMaybe :: forall a b. ISO a b -> ISO (Maybe a) (Maybe b)
isoMaybe (Tuple ab ba) = Tuple (map ab) (map ba)

isoEither :: forall a b c d. ISO a b -> ISO c d -> ISO (Either a c) (Either b d)
isoEither (Tuple ab ba) (Tuple cd dc) =  Tuple (bimap ab cd) (bimap ba dc)

isoFunc :: forall a b c d. ISO a b -> ISO c d -> ISO (a -> c) (b -> d)
isoFunc (Tuple ab ba) (Tuple cd dc) = Tuple (\ac -> cd <<< ac <<< ba) (\bd -> dc <<< bd <<< ab)

isoSymm :: forall a b. ISO (ISO a b) (ISO b a)
isoSymm = Tuple swap swap

-- a = b -> c = d -> a * c = b * d
isoProd :: forall a b c d. ISO a b -> ISO c d -> ISO (Tuple a c) (Tuple b d)
isoProd = isoTuple

-- a = b -> c = d -> a + c = b + d
isoPlus :: forall a b c d. ISO a b -> ISO c d -> ISO (Either a c) (Either b d)
isoPlus = isoEither

-- a = b -> S a = S b
isoS :: forall a b. ISO a b -> ISO (Maybe a) (Maybe b)
isoS = isoMaybe

-- a = b -> c = d -> c ^ a = d ^ b
isoPow :: forall a b c d. ISO a b -> ISO c d -> ISO (a -> c) (b -> d)
isoPow = isoFunc

-- a + b = b + a
plusComm :: forall a b. ISO (Either a b) (Either b a)
plusComm = Tuple (either Right Left) (either Right Left)

-- (a + b) + c = a + (b + c)
plusAssoc :: forall a b c. ISO (Either (Either a b) c) (Either a (Either b c))
plusAssoc = Tuple (either (either Left (Right <<< Left)) (Right <<< Right))
                  (either (Left <<< Left) (either (Left <<< Right) Right))

-- a * b = b * a
multComm :: forall a b. ISO (Tuple a b) (Tuple b a)
multComm = Tuple swap swap

-- (a * b) * c = a * (b * c)
multAssoc :: forall a b c. ISO (Tuple (Tuple a b) c) (Tuple a (Tuple b c))
multAssoc = Tuple (\(Tuple (Tuple a b) c) -> Tuple a (Tuple b c)) (\(Tuple a (Tuple b c)) -> Tuple (Tuple a b) c)

-- a * (b + c) = a * b + a * c
dist :: forall a b c. ISO (Tuple a (Either b c)) (Either (Tuple a b) (Tuple a c))
dist = Tuple (\(Tuple a bc) -> either (Left <<< Tuple a) (Right <<< Tuple a) bc)
             (either (\(Tuple a b) -> Tuple a (Left b)) (\(Tuple a c) -> Tuple a (Right c)))

-- (c ^ b) ^ a = c ^ (a * b)
curryISO :: forall a b c. ISO (a -> b -> c) (Tuple a b -> c)
curryISO = Tuple uncurry curry

-- 1 = S O (we are using Peano arithmetic)
-- https://en.wikipedia.org/wiki/Peano_axioms
one :: ISO Unit (Maybe Void)
one = Tuple (const Nothing) (const unit)

-- 2 = S (S O)
two :: ISO Boolean (Maybe (Maybe Void))
two = Tuple fw bw
  where
    fw true = Just Nothing
    fw false = Nothing
    bw (Just _) = true
    bw Nothing = false

-- O + b = b
plusO :: forall b. ISO (Either Void b) b
plusO = Tuple left Right
  where
    left (Left x) = absurd x -- absurd :: forall a. Void -> a
    left (Right x) = x

-- S a + b = S (a + b)
plusS :: forall a b. ISO (Either (Maybe a) b) (Maybe (Either a b))
plusS = Tuple (either (maybe Nothing (Just <<< Left)) (Just <<< Right))
              (maybe (Left Nothing) (either (Left <<< Just) Right))

-- 1 + b = S b
plusSO :: forall b. ISO (Either Unit b) (Maybe b)
plusSO = isoPlus one refl `trans` plusS `trans` isoS plusO

-- O * a = O
multO :: forall a. ISO (Tuple Void a) Void
multO = Tuple (absurd <<< fst) absurd

-- S a * b = b + a * b
multS :: forall a b. ISO (Tuple (Maybe a) b) (Either b (Tuple a b))
multS = Tuple (\(Tuple a' b) -> maybe (Left b) (Right <<< flip Tuple b) a')
              (either (Tuple Nothing) (\(Tuple a b) -> Tuple (Just a) b))

-- 1 * b = b
multSO :: forall b. ISO (Tuple Unit b) b
multSO =
  isoProd one refl `trans`
    multS `trans`
    isoPlus refl multO `trans` 
    plusComm `trans`
    plusO

-- a ^ O = 1
powO :: forall a. ISO (Void -> a) Unit
powO = Tuple (const unit) (const absurd)

-- a ^ (S b) = a * (a ^ b)
powS :: forall a b. ISO (Maybe b -> a) (Tuple a (b -> a))
powS = Tuple (\f -> Tuple (f Nothing) (f <<< Just)) (uncurry maybe)

-- a ^ 1 = a
-- Go the hard way (like multSO, plusSO)
-- to prove that you really get what is going on!
powSO :: forall a. ISO (Unit -> a) a
powSO = 
  isoPow one refl `trans`
  powS `trans`
  isoProd refl powO `trans`
  multComm `trans`
  multSO
_____________________________________________________
module AlgebraicIsomorphism where

import Prelude
import Data.Tuple (Tuple(..),fst,snd,curry,uncurry,swap)
import Data.Either (Either(..),either)
import Data.Maybe (Maybe(..),maybe,isJust)
import Data.Bifunctor (bimap,lmap)

type ISO a b = Tuple (a -> b) (b -> a)

substL :: forall a b. ISO a b -> a -> b
substL = fst

substR :: forall a b. ISO a b -> b -> a
substR = snd

refl :: forall a. ISO a a
refl = Tuple identity identity

symm :: forall a b. ISO a b -> ISO b a
symm = swap

trans :: forall a b c. ISO a b -> ISO b c -> ISO a c
trans (Tuple ba ab) (Tuple cb bc) = Tuple (cb <<< ba) (ab <<< bc)

isoTuple :: forall a b c d. ISO a b -> ISO c d -> ISO (Tuple a c) (Tuple b d)
isoTuple (Tuple ba ab) (Tuple dc cd) = Tuple (bimap ba dc) (bimap ab cd)

isoEither :: forall a b c d. ISO a b -> ISO c d -> ISO (Either a c) (Either b d)
isoEither (Tuple ba ab) (Tuple dc cd) = Tuple (either (Left <<< ba) (Right <<< dc)) (either (Left <<< ab) (Right <<< cd))

isoFunctor :: forall a b f. Functor f => ISO a b -> ISO (f a) (f b)
isoFunctor = bimap map map
isoList = isoFunctor

isoFunc :: forall a b c d. ISO a b -> ISO c d -> ISO (a -> c) (b -> d)
isoFunc (Tuple ba ab) (Tuple dc cd) = Tuple ( \ ca -> dc <<< ca <<< ab ) ( \ db -> cd <<< db <<< ba )

isoSymm :: forall a b. ISO (ISO a b) (ISO b a)
isoSymm = Tuple symm symm

-- a = b -> c = d -> a * c = b * d
-- Sometimes, we can treat a type as a number - if a type `t`
-- has `n` distinct values then we say that its number is `n`.
-- This is formally called cardinality.
-- See https://en.wikipedia.org/wiki/Cardinality

-- Void has a cardinality of 0 (we will abbreviate it as "Void is 0").
-- Unit is 1.
-- Boolean is 2.
-- Maybe a is 1 + a.
-- We will be using Peano arithmetic so we will write it as S a.
-- https://en.wikipedia.org/wiki/Peano_axioms
-- Either a b is a + b.
-- Tuple a b is a * b.
-- a -> b is b ^ a. Try counting Unit -> Boolean and Boolean -> Unit

-- Algebraic data type got its name because
-- it satisfies a lot of algebraic rules under isomorphism

isoProd :: forall a b c d. ISO a b -> ISO c d -> ISO (Tuple a c) (Tuple b d)
isoProd = isoTuple

-- a = b -> c = d -> a + c = b + d
isoPlus :: forall a b c d. ISO a b -> ISO c d -> ISO (Either a c) (Either b d)
isoPlus = isoEither

-- a = b -> S a = S b
isoS :: forall a b. ISO a b -> ISO (Maybe a) (Maybe b)
isoS = isoFunctor

-- a = b -> c = d -> c ^ a = d ^ b
isoPow :: forall a b c d. ISO a b -> ISO c d -> ISO (a -> c) (b -> d)
isoPow = isoFunc

-- a + b = b + a
plusComm :: forall a b. ISO (Either a b) (Either b a)
plusComm = Tuple (either Right Left) (either Right Left)

-- (a + b) + c = a + (b + c)
plusAssoc :: forall a b c. ISO (Either (Either a b) c) (Either a (Either b c))
plusAssoc = Tuple (either (either Left (Right <<< Left)) (Right <<< Right))
                  (either (Left <<< Left) (either (Left <<< Right) Right))

-- a * b = b * a
multComm :: forall a b. ISO (Tuple a b) (Tuple b a)
multComm = Tuple swap swap

-- (a * b) * c = a * (b * c)
multAssoc :: forall a b c. ISO (Tuple (Tuple a b) c) (Tuple a (Tuple b c))
multAssoc = Tuple ( \ (Tuple (Tuple a b) c) -> Tuple a (Tuple b c) )
                  ( \ (Tuple a (Tuple b c)) -> Tuple (Tuple a b) c )

-- a * (b + c) = a * b + a * c
dist :: forall a b c. ISO (Tuple a (Either b c)) (Either (Tuple a b) (Tuple a c))
dist = Tuple f (either (map Left) (map Right)) where
  f (Tuple a (Left b)) = Left $ Tuple a b
  f (Tuple a (Right c)) = Right $ Tuple a c

-- (c ^ b) ^ a = c ^ (a * b)
curryISO :: forall a b c. ISO (a -> b -> c) (Tuple a b -> c)
curryISO = Tuple uncurry curry

-- 1 = S O (we are using Peano arithmetic)
-- https://en.wikipedia.org/wiki/Peano_axioms
one :: ISO Unit (Maybe Void)
one = Tuple (const Nothing) (const unit)

-- 2 = S (S O)
two :: ISO Boolean (Maybe (Maybe Void))
two = Tuple ( \ bool -> if bool then Just Nothing else Nothing ) isJust
  
-- O + b = b
plusO :: forall b. ISO (Either Void b) b
plusO = Tuple (either absurd identity) Right

-- S a + b = S (a + b)
plusS :: forall a b. ISO (Either (Maybe a) b) (Maybe (Either a b))
plusS = Tuple (either (map Left) (Just <<< Right)) (maybe (Left Nothing) (either (Left <<< Just) Right))

-- 1 + b = S b
plusSO :: forall b. ISO (Either Unit b) (Maybe b)
plusSO = isoPlus one refl `trans` plusS `trans` isoS plusO

-- O * a = O
multO :: forall a. ISO (Tuple Void a) Void
multO = Tuple fst absurd

-- S a * b = b + a * b
multS :: forall a b. ISO (Tuple (Maybe a) b) (Either b (Tuple a b))
multS = Tuple f g where
  f (Tuple Nothing b) = Left b
  f (Tuple (Just a) b) = Right $ Tuple a b
  g = either (Tuple Nothing) (lmap Just)

-- 1 * b = b
multSO :: forall b. ISO (Tuple Unit b) b
multSO =
  isoProd one refl `trans`
    multS `trans`
    isoPlus refl multO `trans` 
    plusComm `trans`
    plusO

-- a ^ O = 1
powO :: forall a. ISO (Void -> a) Unit
powO = Tuple (const unit) (const absurd)

-- a ^ (S b) = a * (a ^ b)
powS :: forall a b. ISO (Maybe b -> a) (Tuple a (b -> a))
powS = Tuple f g where
  f amb = Tuple (amb Nothing) ( \ b -> amb $ Just b )
  g (Tuple a ab) = maybe a ab

-- a ^ 1 = a
-- Go the hard way (like multSO, plusSO)
-- to prove that you really get what is going on!
powSO :: forall a. ISO (Unit -> a) a
-- powSO = ?powSO -- ?hole1 `trans` powS `trans` ?hole2
powSO = Tuple (_ $ unit) const

-- 0 ^ 0 = 0
-- proof :: ISO (Void -> Void) Void
-- proof = Tuple (const _) (const identity) -- `Tuple (const _) const` would also be possible
   -- there is no value to fill in for `_` either way

-- 0 ^ 0 = 1
proof :: ISO (Void -> Void) Unit
proof = Tuple (const unit) (const identity)
_________________________________________________________________
module AlgebraicIsomorphism where

import Prelude

import Data.Bifunctor (bimap)
import Data.Either (Either(..))
import Data.List (List, (:))
import Data.List as List
import Data.Maybe (Maybe(..), fromJust)
import Data.Tuple (Tuple(..), fst, snd, swap)
import Partial.Unsafe (unsafePartial)

-- Please copy your solution to Isomorphism here.
type ISO a b = Tuple (a -> b) (b -> a)

-- Given ISO a b, we can go from a to b ... 
substL :: forall a b. ISO a b -> a -> b
substL = fst -- This is given; you do not need to change it :)

-- ... and vice versa
substR :: forall a b. ISO a b -> b -> a
substR = snd

-- There can exist more than one isomorphism between two types `a` and `b`

isoBoolean :: ISO Boolean Boolean
isoBoolean = Tuple identity identity

isoBooleanNot :: ISO Boolean Boolean
isoBooleanNot = Tuple not not

-- Isomorphism denotes an equivalence relation so it naturally satisfies
-- the 3 major properties of equivalence relations (isomorphism is denoted
-- as `<=>` below):
-- 1) Reflexivity: a <=> a
-- 2) Symmetry: (a <=> b) -> (b <=> a)
-- 3) Transitivity: (a <=> b) /\ (b <=> c) -> (a <=> c)
-- Here, `/\` denotes logical conjunction, otherwise known as "AND"

refl :: forall a. ISO a a
refl = Tuple identity identity

symm :: forall a b. ISO a b -> ISO b a
symm iso = Tuple (substR iso) (substL iso)

trans :: forall a b c. ISO a b -> ISO b c -> ISO a c
trans iso_ab iso_bc = Tuple (substL iso_ab >>> substL iso_bc) (substR iso_ab <<< substR iso_bc)

-- We can combine isomorphisms using the Cartesian product ... 
isoTuple :: forall a b c d. ISO a b -> ISO c d -> ISO (Tuple a c) (Tuple b d)
isoTuple iso_ab iso_cd = Tuple (\(Tuple a c) -> Tuple (substL iso_ab a) (substL iso_cd c)) (\(Tuple b d) -> Tuple (substR iso_ab b) (substR iso_cd d))

-- And derive new isomorphisms from known ones ... 

isoList :: forall a b. ISO a b -> ISO (List a) (List b)
isoList iso_ab = Tuple (map (substL iso_ab)) (map (substR iso_ab))

isoMaybe :: forall a b. ISO a b -> ISO (Maybe a) (Maybe b)
isoMaybe iso_ab = Tuple (map (substL iso_ab)) (map (substR iso_ab))

isoEither :: forall a b c d. ISO a b -> ISO c d -> ISO (Either a c) (Either b d)
isoEither iso_ab iso_cd = Tuple (bimap (substL iso_ab) (substL iso_cd)) (bimap (substR iso_ab) (substR iso_cd))

isoFunc :: forall a b c d. ISO a b -> ISO c d -> ISO (a -> c) (b -> d)
isoFunc iso_ab iso_cd = Tuple (\a_c -> substR iso_ab >>> a_c >>> substL iso_cd) (\b_d -> substL iso_ab >>> b_d >>> substR iso_cd)

-- Going another way is hard (and is generally impossible)
-- Remember, for all valid isomorphisms, converting to and fro
-- should always give you the original value.
-- You need this to prove that some cases are impossible.
isoUnMaybe :: forall a b. ISO (Maybe a) (Maybe b) -> ISO a b
isoUnMaybe iso_ma_mb = Tuple left right
    where
    left a =
        case substL iso_ma_mb (Just a) of
            Nothing ->  unsafePartial $ fromJust (substL iso_ma_mb Nothing)
            Just b -> b
    right b =
        case substR iso_ma_mb (Just b) of
            Nothing -> unsafePartial $ fromJust (substR iso_ma_mb Nothing)
            Just a -> a

-- We cannot construct:
--   isoUnEither :: forall a b c d. ISO (Either a b) (Either c d) -> ISO a c -> ISO b d
-- because we have this:
isoEU :: ISO (Either (List Unit) Unit) (Either (List Unit) Void)
isoEU = Tuple left right
    where
    left (Left units) = Left (unit : units)
    left (Right unit) = Left (List.fromFoldable [])
    right (Left list) =
        case List.uncons list of
            Just { head: _, tail: units } -> Left units
            Nothing -> Right unit
    right (Right a) = absurd a

-- where `Unit` has exactly 1 member and `Void` has no members.
-- The existence of isoUnEither would imply the existence of
-- ISO Unit Void which would mean we could construct a value of
-- type Void from a value of type Unit (which is obviously impossible)

-- Last but not least, we can define isomorphisms on isomorphisms ;)
isoSymm :: forall a b. ISO (ISO a b) (ISO b a)
isoSymm = Tuple symm symm

-- Sometimes, we can treat a type as a number - if a type `t`
-- has `n` distinct values then we say that its number is `n`.
-- This is formally called cardinality.
-- See https://en.wikipedia.org/wiki/Cardinality

-- Void has a cardinality of 0 (we will abbreviate it as "Void is 0").
-- Unit is 1.
-- Boolean is 2.
-- Maybe a is 1 + a.
-- We will be using Peano arithmetic so we will write it as S a.
-- https://en.wikipedia.org/wiki/Peano_axioms
-- Either a b is a + b.
-- Tuple a b is a * b.
-- a -> b is b ^ a. Try counting Unit -> Boolean and Boolean -> Unit

-- Algebraic data type got its name because
-- it satisfies a lot of algebraic rules under isomorphism

-- a = b -> c = d -> a * c = b * d
isoProd :: forall a b c d. ISO a b -> ISO c d -> ISO (Tuple a c) (Tuple b d)
isoProd = isoTuple

-- a = b -> c = d -> a + c = b + d
isoPlus :: forall a b c d. ISO a b -> ISO c d -> ISO (Either a c) (Either b d)
isoPlus = isoEither

-- a = b -> S a = S b
isoS :: forall a b. ISO a b -> ISO (Maybe a) (Maybe b)
isoS = isoMaybe

-- a = b -> c = d -> c ^ a = d ^ b
isoPow :: forall a b c d. ISO a b -> ISO c d -> ISO (a -> c) (b -> d)
isoPow = isoFunc

-- a + b = b + a
plusComm :: forall a b. ISO (Either a b) (Either b a)
plusComm = Tuple left right
    where
    left (Left a) = Right a
    left (Right b) = Left b
    right (Left b) = Right b
    right (Right a) = Left a

-- (a + b) + c = a + (b + c)
plusAssoc :: forall a b c. ISO (Either (Either a b) c) (Either a (Either b c))
plusAssoc = Tuple left right
    where
    left (Left (Left a)) = Left a
    left (Left (Right b)) = Right (Left b)
    left (Right c) = Right (Right c)
    right (Left a) = Left (Left a)
    right (Right (Left b)) = Left (Right b)
    right (Right (Right c)) = Right c

-- a * b = b * a
multComm :: forall a b. ISO (Tuple a b) (Tuple b a)
multComm = Tuple swap swap

-- (a * b) * c = a * (b * c)
multAssoc :: forall a b c. ISO (Tuple (Tuple a b) c) (Tuple a (Tuple b c))
multAssoc = Tuple left right
    where
    left (Tuple (Tuple a b) c) = Tuple a (Tuple b c)
    right (Tuple a (Tuple b c)) = Tuple (Tuple a b) c

-- a * (b + c) = a * b + a * c
dist :: forall a b c. ISO (Tuple a (Either b c)) (Either (Tuple a b) (Tuple a c))
dist = Tuple left right
    where
    left (Tuple a (Left b)) = Left (Tuple a b)
    left (Tuple a (Right c)) = Right (Tuple a c)
    right (Left (Tuple a b)) = Tuple a (Left b)
    right (Right (Tuple a c)) = Tuple a (Right c)

-- (c ^ b) ^ a = c ^ (a * b)
curryISO :: forall a b c. ISO (a -> b -> c) (Tuple a b -> c)
curryISO = Tuple left right
    where
    left f (Tuple a b) = f a b
    right f a b = f (Tuple a b)

-- 1 = S O (we are using Peano arithmetic)
-- https://en.wikipedia.org/wiki/Peano_axioms
one :: ISO Unit (Maybe Void)
one = Tuple (const Nothing) (const unit)

-- 2 = S (S O)
two :: ISO Boolean (Maybe (Maybe Void))
two = Tuple left right
    where
    left false = Nothing
    left true = Just Nothing
    right Nothing = false
    right (Just _) = true

-- O + b = b
plusO :: forall b. ISO (Either Void b) b
plusO = Tuple left Right
  where
    left (Left x) = absurd x -- absurd :: forall a. Void -> a
    left (Right x) = x

-- S a + b = S (a + b)
plusS :: forall a b. ISO (Either (Maybe a) b) (Maybe (Either a b))
plusS = Tuple left right
    where
    left (Left Nothing) = Nothing
    left (Left (Just a)) = Just (Left a)
    left (Right b) = Just (Right b)
    right Nothing = Left Nothing
    right (Just (Left a)) = Left (Just a)
    right (Just (Right b)) = Right b

-- 1 + b = S b
plusSO :: forall b. ISO (Either Unit b) (Maybe b)
plusSO = isoPlus one refl `trans` plusS `trans` isoS plusO

-- O * a = O
multO :: forall a. ISO (Tuple Void a) Void
multO = Tuple left right
    where
    left (Tuple v _) = v
    right v = (Tuple v (absurd v))

-- S a * b = b + a * b
multS :: forall a b. ISO (Tuple (Maybe a) b) (Either b (Tuple a b))
multS = Tuple left right
    where
    left (Tuple Nothing b) = Left b
    left (Tuple (Just a) b) = Right (Tuple a b)
    right (Left b) = Tuple Nothing b
    right (Right (Tuple a b)) = Tuple (Just a) b

-- 1 * b = b
multSO :: forall b. ISO (Tuple Unit b) b
multSO =
  isoProd one refl `trans`
    multS `trans`
    isoPlus refl multO `trans` 
    plusComm `trans`
    plusO

-- a ^ O = 1
powO :: forall a. ISO (Void -> a) Unit
powO = Tuple left right
    where
    left _ = unit
    right unit = absurd

-- a ^ (S b) = a * (a ^ b)
powS :: forall a b. ISO (Maybe b -> a) (Tuple a (b -> a))
powS = Tuple left right
    where
    left f = Tuple (f Nothing) (\b -> f (Just b))
    right (Tuple a b_a) = case _ of
        Just b -> b_a b
        Nothing -> a

-- a ^ 1 = a
-- Go the hard way (like multSO, plusSO)
-- to prove that you really get what is going on!
powSO :: forall a. ISO (Unit -> a) a
powSO = Tuple left right
    where
    left f = f unit
    right a = \unit -> a
