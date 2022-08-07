5861487fdb20cff3ab000030


module Boolfuck where

import Boolfuck.Preload (brainfuckToBoolfuck)
import Data.Char

data Input = Input [Bool] String;
data Output = Output Int Int String;
data Tape = Tape [Bool] Bool [Bool]
data State = State Tape Input Output
data Code = Code String String

readBit :: Input -> (Bool, Input)
readBit (Input [] "") = (False, Input [] "")
readBit (Input (b : bs) s) = (b, Input bs s)
readBit (Input [] (ch : s)) = readBit (Input (go 8 $ ord ch `divMod` 2) s) where
  go 0 _ = []
  go n (d, m) = (m == 1) : go (n - 1) (d `divMod` 2)

writeBit :: Bool -> Output -> Output
writeBit b (Output n ch s) = go (n + 1) (if b then 2 ^ n + ch else ch) s where
  go 8 ch s = Output 0 0 (chr ch : s)
  go n ch s = Output n ch s

initInput :: String -> Input
initInput s = Input [] s

initOutput :: Output
initOutput = Output 0 0 ""

initTape :: Tape
initTape = Tape [] False []

initState :: String -> State
initState s = State initTape (initInput s) initOutput

initCode :: String -> Code
initCode s = Code s []

nextCmd :: Code -> Maybe (Char, Code)
nextCmd (Code [] _) = Nothing
nextCmd (Code (cmd : cmds) revs) = Just (cmd, Code cmds (cmd : revs))

alterTape :: (Tape -> Tape) -> State -> State
alterTape f (State tape input output) = State (f tape) input output

flipCell :: State -> State
flipCell = alterTape go where
  go (Tape prev cell next) = Tape prev (not cell) next

readInput :: State -> State
readInput (State (Tape prev _ next) input output) = go prev next output $ readBit input where
  go prev next output (cell, input) = State (Tape prev cell next) input output

writeOutput :: State -> State
writeOutput (State (Tape prev cell next) input output) = State (Tape prev cell next) input (writeBit cell output)

moveLeft :: State -> State
moveLeft = alterTape go where
  go (Tape [] cell next) = Tape [] False (cell : next)
  go (Tape (pCell : prev) cell next) = Tape prev pCell (cell : next)

moveRight :: State -> State
moveRight = alterTape go where
  go (Tape prev cell []) = Tape (cell : prev) False []
  go (Tape prev cell (nCell : next)) = Tape (cell : prev) nCell next

currentCell :: State -> Bool
currentCell (State (Tape _ cell _) _ _) = cell

skipAhead :: Code -> Code
skipAhead (Code cmds revs) = go 0 cmds revs where
  go 0 (']' : cmds) revs = Code cmds (']' : revs)
  go n (']' : cmds) revs = go (n - 1) cmds (']' : revs)
  go n ('[' : cmds) revs = go (n + 1) cmds ('[' : revs)
  go n (ch : cmds) revs = go n cmds (ch : revs)
  go _ [] _ = Code [] []

skipBehind :: Code -> Code
skipBehind (Code cmds []) = error "Invalid Skip Behind"
skipBehind (Code cmds (cmd : revs)) = go 0 (cmd : cmds) revs where
  go 0 cmds ('[' : revs) = Code cmds ('[' : revs)
  go n cmds ('[' : revs) = go (n - 1) ('[' : cmds) revs
  go n cmds (']' : revs) = go (n + 1) (']' : cmds) revs
  go n cmds (ch : revs) = go n (ch : cmds) revs
  go _ _ [] = Code [] []

printOutput :: State -> String
printOutput (State _ _ (Output 0 _ s)) = reverse s
printOutput (State _ _ (Output _ ch s)) = reverse (chr ch : s)

boolfuck :: String -> String -> String
boolfuck code input = go (nextCmd $ initCode code) $ initState input where
  go Nothing state = printOutput state
  go (Just ('+', code)) state = go (nextCmd code) $ flipCell state
  go (Just (',', code)) state = go (nextCmd code) $ readInput state
  go (Just (';', code)) state = go (nextCmd code) $ writeOutput state
  go (Just ('<', code)) state = go (nextCmd code) $ moveLeft state
  go (Just ('>', code)) state = go (nextCmd code) $ moveRight state
  go (Just ('[', code)) state | currentCell state = go (nextCmd code) state
                              | otherwise         = go (nextCmd $ skipAhead code) state
  go (Just (']', code)) state | currentCell state = go (nextCmd $ skipBehind code) state
                              | otherwise         = go (nextCmd code) state
  go (Just (_, code)) state = go (nextCmd code) state
_____________________________
module Boolfuck where

-- import Boolfuck.Preload (brainfuckToBoolfuck)

import Data.Char (chr, ord)
import Data.List (splitAt, unfoldr, zipWith)


bitInByte :: Int
bitInByte = 8

powers :: [Int]
powers = [2^i | i <- [0..(bitInByte-1)]]

dot :: Num a => [a] -> [a] -> a
dot x y = sum $ zipWith (*) x y

findEndBracket :: String -> Int
findEndBracket str = let
  recFunc _ [] = error "Incorrect brackets in string"
  recFunc num (char:chars)
    | char == '[' = recFunc (num + 1) chars
    | char == ']' = if num == 0 then length chars + 1 else recFunc (num - 1) chars
    | otherwise = recFunc num chars
  in length str - recFunc 0 str

data Bit = Zero | One deriving (Show, Eq)

bitToInt :: Bit -> Int
bitToInt Zero = 0
bitToInt One = 1

swapBit :: Bit -> Bit
swapBit Zero = One
swapBit One = Zero

addZeros :: [Bit] -> [Bit]
addZeros = take bitInByte . (++ repeat Zero)

byteToInt :: [Bit] -> Int
byteToInt byte
  | length byte /= bitInByte = error "Is not byte"
  | otherwise = dot powers . map bitToInt $ byte

intToByte :: Int -> [Bit]
intToByte = addZeros . unfoldr (\n -> if n == 0 then Nothing else Just (case n `mod` 2 of 0 -> Zero; 1 -> One, n `div` 2))

convertToString :: [Bit] -> String
convertToString [] = []
convertToString bitList = let
  accFunc (headStack:tailStack) [] = reverse (addZeros headStack : tailStack)
  accFunc stack bitList = accFunc (byte : stack) nextBitList where (byte, nextBitList) = splitAt 8 bitList
  splitToBytes = accFunc []
  in map (chr . byteToInt) . splitToBytes $ bitList

convertToBitList :: String -> [Bit]
convertToBitList = concatMap (intToByte . ord)

data Stream a = a :> Stream a

repeatStream :: a -> Stream a
repeatStream x = let s = x :> s in s

data Tape a = Tape { left :: Stream a, cur :: a, right :: Stream a }

repeatTape :: a -> Tape a
repeatTape x = let s = repeatStream x in Tape s x s

setCur :: a -> Tape a -> Tape a
setCur a (Tape left _ right) = Tape left a right

moveLeft, moveRight :: Tape a -> Tape a
moveLeft (Tape (l :> left) bit right) = Tape left l (bit :> right)
moveRight (Tape left bit (r :> right)) = Tape (bit :> left) r right

data Operation
  = Swap
  | Read
  | Write
  | MoveL
  | MoveR
  | Loop [Operation]

parse :: String -> [Operation]
parse [] = []
parse (op:ops) = case op of
  '+' -> Swap  : parse ops
  ',' -> Read  : parse ops
  ';' -> Write : parse ops
  '<' -> MoveL : parse ops
  '>' -> MoveR : parse ops
  '[' -> Loop (parse fstPart) : parse sndPart where (fstPart, sndPart) = splitAt (findEndBracket ops) ops
  _   -> parse ops

data State = State { tape :: Tape Bit, inp :: [Bit], out :: [Bit] }

runOp :: Operation -> State -> State
runOp op state  = case op of
  Swap  -> state {tape = setCur (swapBit . cur $ t) t}
  Read  -> case i of
      []  -> state {tape = setCur Zero t}
      i   -> state {tape = setCur (head i) t, inp = tail i}
  Write -> state {out = cur t : o}
  MoveL -> state {tape = moveLeft t}
  MoveR -> state {tape = moveRight t}
  Loop opLst -> loopFunc opLst state
  where t = tape state
        i = inp state
        o = out state
        loopFunc opLst state = case cur . tape $ state of
          Zero -> state
          One -> loopFunc opLst (foldl (flip runOp) state opLst)

boolfuck :: String -> String -> String
boolfuck code inp = convertToString . reverse . out $ foldl (flip runOp) (State (repeatTape Zero) (convertToBitList inp) []) (parse code)
_____________________________
{-# LANGUAGE BlockArguments #-}
{-# LANGUAGE DerivingStrategies #-}
{-# LANGUAGE LambdaCase #-}
{-# LANGUAGE NamedFieldPuns #-}
{-# LANGUAGE TemplateHaskell #-}

module Boolfuck where

import Boolfuck.Preload (brainfuckToBoolfuck)
import Control.Lens hiding ((:>))
import Control.Lens.TH
import Control.Monad.State
import Data.Bits
import Data.Char as Char
import Data.Foldable (traverse_)

data Stream a = a :> Stream a

repeatStream :: a -> Stream a
repeatStream x = let s = x :> s in s

data Tape a = Tape (Stream a) a (Stream a)

repeatTape :: a -> Tape a
repeatTape x =
  let s = repeatStream x
   in Tape s x s

tapeLeft, tapeRight :: Tape a -> Tape a
tapeLeft (Tape ls x (r :> rs)) = Tape (x :> ls) r rs
tapeRight (Tape (l :> ls) x rs) = Tape ls l (x :> rs)

current :: Lens' (Tape a) a
current next (Tape l x r) = (\x -> Tape l x r) <$> next x

parse :: String -> [Instr]
parse src = snd (go src)
  where
    go = \case
      "" -> ("", [])
      '+' : is -> (SWAP :) <$> go is
      ',' : is -> (READ :) <$> go is
      ';' : is -> (WRITE :) <$> go is
      '<' : is -> (MOVEL :) <$> go is
      '>' : is -> (MOVER :) <$> go is
      '[' : is | (is, body) <- go is -> (LOOP body :) <$> go is
      ']' : is -> (is, [])
      _ : is -> go is

data Instr
  = SWAP
  | READ
  | WRITE
  | MOVEL
  | MOVER
  | LOOP [Instr]
  deriving stock (Show)

data K = K
  { _tape :: Tape Bool,
    _input :: [Bool],
    _output :: [Bool]
  }

makeLenses ''K

type M = State K

run :: [Instr] -> M ()
run = traverse_ step

step :: Instr -> M ()
step = \case
  SWAP -> do
    tape . current %= not
  READ -> do
    preuse (input . _Cons) >>= \case
      Nothing -> do
        tape . current .= False
      Just (x, input') -> do
        input .= input'
        tape . current .= x
  WRITE -> do
    x <- use (tape . current)
    output %= (x :)
  MOVEL -> do
    tape %= tapeLeft
  MOVER -> do
    tape %= tapeRight
  LOOP body -> do
    whenM (use (tape . current)) do
      run body
      whenM (use (tape . current)) do
        step (LOOP body)

whenM :: Monad m => m Bool -> m () -> m ()
whenM cond body = do
  condB <- cond
  when condB body

toBits :: String -> [Bool]
toBits cs = do
  b <- Char.ord <$> cs
  [testBit b i | i <- [0 .. 7]]

fromBits :: [Bool] -> String
fromBits bs =
  [(Char.chr . fromBits . padRight 8 False) c | c <- chunks 8 bs]
  where
    chunks :: Int -> [a] -> [[a]]
    chunks n xs = case splitAt n xs of
      ([], []) -> []
      (c, []) -> [c]
      (c, xs) -> c : chunks n xs

    padRight :: Int -> a -> [a] -> [a]
    padRight size x xs = take size (xs ++ repeat x)

    fromBits :: [Bool] -> Int
    fromBits = foldr (\b r -> (if b then 1 else 0) .|. (r `shiftL` 1)) 0

boolfuck :: String -> String -> String
boolfuck src input =
  let K {_output} = execState (run (parse src)) ctx
   in fromBits (reverse _output)
  where
    ctx =
      K
        { _tape = repeatTape False,
          _input = toBits input,
          _output = []
        }
