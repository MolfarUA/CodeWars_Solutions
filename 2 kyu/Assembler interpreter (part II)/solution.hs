{-# LANGUAGE FlexibleContexts #-}
module AssemblerInterpreter where

import qualified Data.Vector as V
import qualified Data.Map as M
import Text.Parsec
import Text.Parsec.Char
import Text.Parsec.Language
import Text.Parsec.Token
import Control.Monad.State

type Reg = String

type Lbl = String

data Instruction
  = Mov Reg Arg
  | Inc Reg
  | Dec Reg
  | Add Reg Arg
  | Sub Reg Arg
  | Mul Reg Arg
  | Div Reg Arg
  | Jmp Lbl
  | Cmp Arg Arg
  | Jcc Cond Lbl
  | Call Lbl
  | Ret
  | Msg [MsgArg]
  | End
  deriving (Show)

data Arg
  = ArgImm Int
  | ArgReg Reg
  deriving (Show)
  
data Cond
  = CondNE | CondE | CondGE | CondG | CondLE | CondL
  deriving (Show)
  
data MsgArg
  = MsgStr String
  | MsgReg Reg
  deriving (Show)
            
data Compiler
  = Compiler
  { comLC :: Int
  , comInstructions :: [Instruction]
  , comLbls :: M.Map Lbl Int
  }
  deriving (Show)
  
data Machine
  = Machine
  { macInstructions :: V.Vector Instruction
  , macPC :: Int
  , macStack :: [Int]
  , macCC :: Ordering
  , macRegs :: M.Map Reg Int
  , macLbls :: M.Map Lbl Int
  , macOutput :: String
  , macEnd :: Bool
  }

interpret :: String -> Maybe String
interpret prog = do
  let com = compile prog
  evalStateT run Machine
    { macInstructions = V.fromList . comInstructions $ com
    , macPC = 0
    , macStack = []
    , macCC = EQ
    , macRegs = M.empty
    , macLbls = comLbls com
    , macOutput = ""
    , macEnd = False
    }
  
compile prog =
  let
    TokenParser
      { identifier = identifier
      , integer = integer
      , symbol = symbol
      , reserved = reserved
      , whiteSpace = whiteSpace
      } = makeTokenParser emptyDef
    com = either (error . show) id $ runParser (whiteSpace *> pProg <* eof) Compiler
      { comLC = 0
      , comInstructions = []
      , comLbls = M.empty
      } "" prog
    addInstruction i = modifyState $ \s -> s { comLC = succ $ comLC s
                                             , comInstructions = i : comInstructions s
                                             }
    addLbl l = modifyState $ \s -> s { comLbls = M.insert l (comLC s) $ comLbls s }
    pProg = many pLine >> getState
    pLine = (pInstruction >>= addInstruction)
        <|> pDefLbl
        <|> pComment
    pComment = char ';' >> skipMany (noneOf "\n") >> whiteSpace
    pDefLbl = (pLbl <* symbol ":") >>= addLbl
    pLbl = identifier
    pReg = identifier
    pArg = ArgImm . fromIntegral <$> integer
       <|> ArgReg <$> pReg
    pMsgArg = MsgStr <$ char '\'' <*> manyTill anyChar (char '\'') <* whiteSpace
          <|> MsgReg <$> identifier
    pInstruction = Mov <$ reserved "mov" <*> pReg <* symbol "," <*> pArg
               <|> Inc <$ reserved "inc" <*> pReg
               <|> Dec <$ reserved "dec" <*> pReg
               <|> Add <$ reserved "add" <*> pReg <* symbol "," <*> pArg
               <|> Sub <$ reserved "sub" <*> pReg <* symbol "," <*> pArg
               <|> Mul <$ reserved "mul" <*> pReg <* symbol "," <*> pArg
               <|> Div <$ reserved "div" <*> pReg <* symbol "," <*> pArg
               <|> Jmp <$ reserved "jmp" <*> pLbl
               <|> Cmp <$ reserved "cmp" <*> pArg <* symbol "," <*> pArg
               <|> Jcc CondNE <$ reserved "jne" <*> pLbl
               <|> Jcc CondE <$ reserved "je" <*> pLbl
               <|> Jcc CondGE <$ reserved "jge" <*> pLbl
               <|> Jcc CondG <$ reserved "jg" <*> pLbl
               <|> Jcc CondLE <$ reserved "jle" <*> pLbl
               <|> Jcc CondL <$ reserved "jl" <*> pLbl
               <|> Call <$ reserved "call" <*> pLbl
               <|> Ret <$ reserved "ret"
               <|> Msg <$ reserved "msg" <*> sepBy pMsgArg (symbol ",")
               <|> End <$ reserved "end"
  in
    com { comInstructions = reverse $ comInstructions com }
  
getArg (ArgImm i) = pure i
getArg (ArgReg r) = getReg r
getLbl l = gets $ (M.! l) . macLbls
getReg r = gets $ (M.! r) . macRegs
setReg r v = modify $ \s -> s { macRegs = M.insert r v $ macRegs s }
modReg r f = modify $ \s -> s { macRegs = M.adjust f r $ macRegs s }
getPC = gets macPC
setPC v = modify $ \s -> s { macPC = v }
getCC = gets macCC
setCC v = modify $ \s -> s { macCC = v }
getOutput = gets macOutput
setOutput v = modify $ \s -> s { macOutput = v }
getEnd = gets macEnd
setEnd v = modify $ \s -> s { macEnd = v }
push v = modify $ \s -> s { macStack = v : macStack s }
pop = StateT $ \s -> let (v:vs) = macStack s in pure (v, s { macStack = vs })
formatMsg args = concat <$> mapM showArg args where
  showArg (MsgStr s) = pure s
  showArg (MsgReg r) = show <$> getReg r
fetchInstruction = do
  pc <- getPC
  setPC $ succ pc
  ((V.!? pc) <$> gets macInstructions) >>= lift
  
branch CondNE LT = True
branch CondNE GT = True
branch CondE EQ = True
branch CondGE GT = True
branch CondGE EQ = True
branch CondG GT = True
branch CondLE LT = True
branch CondLE EQ = True
branch CondL LT = True
branch _ _ = False

whenM c m = c >>= flip when m
untilM c m = x where
  x = c >>= \b -> if b then pure () else m >> x

run :: StateT Machine Maybe String
run = untilM getEnd step >> getOutput

step :: StateT Machine Maybe ()
step = do
  instruction <- fetchInstruction
  case instruction of
    Mov x y -> getArg y >>= setReg x
    Inc x -> modReg x succ
    Dec x -> modReg x pred
    Add x y -> ((+) <$> getReg x <*> getArg y) >>= setReg x
    Sub x y -> ((-) <$> getReg x <*> getArg y) >>= setReg x
    Mul x y -> ((*) <$> getReg x <*> getArg y) >>= setReg x
    Div x y -> (div <$> getReg x <*> getArg y) >>= setReg x
    Jmp lbl -> getLbl lbl >>= setPC
    Cmp x y -> (compare <$> getArg x <*> getArg y) >>= setCC
    Jcc cc lbl -> whenM (branch cc <$> getCC) $ getLbl lbl >>= setPC
    Call lbl -> (getPC >>= push) >> getLbl lbl >>= setPC
    Ret -> pop >>= setPC
    Msg args -> formatMsg args >>= setOutput
    End -> setEnd True

____________________________________________________
module AssemblerInterpreter where

import qualified Data.Map.Strict as M
import qualified Data.List as L
import Data.Either (fromRight)
import Data.Maybe (isJust, fromJust)
import Prelude hiding (div)
import qualified Prelude as P (div)

import Control.Applicative 
import Text.Parsec hiding ((<|>), some, many, Empty, label)
import Text.Parsec.String
tryParsers :: [Parser a] -> Parser a
tryParsers = foldr (<|>) empty . map try

-- AST 

type Id = String
type Lbl = Id
type Name = Either Int Id 
type Message = Either String Name
data Ins = Empty 
         | Mov Id Name | Add Id Name | Sub Id Name | Mul Id Name | Div Id Name
         | Inc Id | Dec Id 
         | Label Lbl
         | Cmp Name Name
         | Jmp Lbl | Jne Lbl | Je Lbl | Jge Lbl | Jg Lbl | Jle Lbl | Jl Lbl 
         | Call Lbl | Ret
         | Msg [Message]
         | End
         deriving (Eq, Show)
         
-- Parse

identifier :: Parser Id
identifier = do
  i <- oneOf "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm_"
  is <- many (oneOf "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm_0123456789")
  return $ i:is
  
number :: Parser Int
number = tryParsers [p1, p2] where
  p1 = do
    num <- many1 (oneOf "0123456789")
    return $ read num
  p2 = do
    char '-'
    num <- many1 (oneOf "0123456789")
    return $ negate $ read num
    
name :: Parser Name
name = tryParsers [p1, p2] where
  p1 = do
    n <- number
    return $ Left n
  p2 = do
    i <- identifier
    return $ Right i
    
binary :: String -> (Id -> Name -> Ins) -> Parser Ins
binary str op = do
  string str
  spaces
  i <- identifier
  spaces
  char ','
  spaces
  n <- name
  return $ op i n
  
mov = binary "mov" Mov
add = binary "add" Add
sub = binary "sub" Sub 
mul = binary "mul" Mul 
div = binary "div" Div

unary :: String -> (Id -> Ins) -> Parser Ins
unary str op = do
  string str
  spaces
  i <- identifier
  return $ op i
  
inc = unary "inc" Inc
dec = unary "dec" Dec

label :: Parser Ins
label = do
  i <- identifier
  spaces
  char ':'
  return $ Label i
  
cmp :: Parser Ins
cmp = do
  string "cmp"
  spaces
  n1 <- name
  spaces
  char ','
  spaces
  n2 <- name
  return $ Cmp n1 $ n2
  
jump :: String -> (Lbl -> Ins) -> Parser Ins
jump str op = do
  string str
  spaces
  i <- identifier
  return $ op i
  
jmp = jump "jmp" Jmp
jne = jump "jne" Jne
je = jump "je" Je
jge = jump "jge" Jge
jg = jump "jg" Jg
jle = jump "jle" Jle
jl = jump "jl" Jl

call = jump "call" Call

ret :: Parser Ins
ret = do
  string "ret"
  return Ret

message :: Parser Message
message = tryParsers [p1, p2] where
  p1 = do
    char '\''
    str <- many $ satisfy (/= '\'')
    char '\''
    return $ Left str
  p2 = do
    n <- name
    return $ Right n

msg :: Parser Ins
msg = do
  string "msg"
  spaces
  ms <- msg'
  return $ Msg ms
  where
    msg' = tryParsers [p1, p2] where
      p1 = do
        m <- message
        spaces
        char ','
        spaces
        ms <- msg'
        return $ m:ms
      p2 = do
        m <- message
        return [m]
      
end :: Parser Ins
end = do
  string "end"
  return End
  
emp :: Parser Ins
emp = do
  spaces
  return Empty

ins :: Parser Ins 
ins = tryParsers [p1, p2] where
  ins' = tryParsers [mov, add, sub, mul, div, inc, dec, label, cmp, jmp, jne, je, jge, jg, jle, jl, call, ret, msg, end, emp]
  p1 = do
    spaces
    i <- ins'
    spaces
    char ';'
    many anyChar
    return i
  p2 = do
    spaces
    i <- ins'
    spaces
    return i

parseAll :: String -> [Ins]
parseAll prog = [fromRight (error "parse error") $ parse ins "instruction" i | i <- L.lines prog]

-- execute

type ProgramTable = M.Map Int Ins
type NameTable = M.Map Id Int
type LabelTable = M.Map Lbl Int
type Comp = Maybe Ordering
type CallStack = [Int]
type Env = (Int, NameTable, Comp, String, CallStack) -- Int: ProgPtr, String: Msg

interpret :: String -> Maybe String
interpret prog = interpret' initEnv where
  pTab = M.fromList $ zip [0..] $ parseAll prog
  isLabel ins = case ins of 
    Label lbl -> Just lbl
    otherwise -> Nothing
  lTab = M.fromList [(fromJust . isLabel $ pTab M.! i, i) | i <- [0..M.size pTab-1], isJust . isLabel $ pTab M.! i]
  initEnv = (0, M.empty, Nothing, "", [])
  interpret' (ptr, nTab, comp, mesg, cSt)
    | ptr == M.size pTab = Nothing
    | pTab M.! ptr == End = Just mesg
    | otherwise = interpret' (ptr', nTab', comp', mesg', cSt') where
      -- Recognize name and get its value
      readInt ('-':n) = negate $ readInt n 
      readInt n = read n
      getName :: String -> Name
      getName str | (head str) `elem` "-0123456789" = Left $ readInt str 
                  | otherwise = Right str
      getValue (Left n) = n
      getValue (Right k) = nTab M.! k
      -- Show message
      showM (Left str) = str
      showM (Right n) = show $ getValue n
      -- Current instruction
      ins = pTab M.! ptr
      -- Update environment
      ptr' = case ins of
        Jmp lbl -> lTab M.! lbl
        Jne lbl -> if comp `elem` [Just LT, Just GT] then lTab M.! lbl else ptr + 1
        Je lbl -> if comp `elem` [Just EQ] then lTab M.! lbl else ptr + 1
        Jge lbl -> if comp `elem` [Just EQ, Just GT] then lTab M.! lbl else ptr + 1
        Jg lbl -> if comp `elem` [Just GT] then lTab M.! lbl else ptr + 1
        Jle lbl -> if comp `elem` [Just LT, Just EQ] then lTab M.! lbl else ptr + 1
        Jl lbl -> if comp `elem` [Just LT] then lTab M.! lbl else ptr + 1
        Call lbl -> lTab M.! lbl
        Ret -> head cSt + 1
        otherwise -> ptr + 1
      nTab' = case ins of
        Mov i n -> M.insert i (getValue n) nTab
        Add i n -> M.insert i ((nTab M.! i) + getValue n) nTab
        Sub i n -> M.insert i ((nTab M.! i) - getValue n) nTab
        Mul i n -> M.insert i ((nTab M.! i) * getValue n) nTab
        Div i n -> M.insert i (P.div (nTab M.! i) (getValue n)) nTab
        Inc i -> M.insert i ((nTab M.! i) + 1) nTab
        Dec i -> M.insert i ((nTab M.! i) - 1) nTab
        otherwise -> nTab
      comp' = case ins of
        Cmp n1 n2 -> Just $ compare (getValue n1) (getValue n2) 
        otherwise -> comp
      mesg' = case ins of
        Msg ms -> mesg ++ concat [showM m | m <- ms]
        otherwise -> mesg
      cSt' = case ins of 
        Call lbl -> ptr:cSt
        Ret -> tail cSt
        otherwise -> cSt
        
____________________________________________________
{-# OPTIONS_GHC -Wall -Werror #-}
{-# LANGUAGE BangPatterns #-}
module AssemblerInterpreter where
import Control.Monad.RWS
import Control.Monad.State
import Data.Maybe (fromMaybe, listToMaybe, mapMaybe)
import Data.Void (Void)
import qualified Data.Map.Strict as M
import Data.Foldable (foldrM)
import Text.Megaparsec hiding (State, token, Label)
import Text.Megaparsec.Char hiding (space)
import Text.Megaparsec.Char.Lexer

-- Machine

type Address = String
type Value = Int
type Offset = Int
type Identifier = String

-- For convenience, the unnamed register is just a register for cmp to push to
type Registers = M.Map (Maybe Address) Value
type Labels a = M.Map Identifier (ListZipper a)
type CallStack a = [ListZipper a]

data Instruction
  = Mov Address (Either Address Value)
  | Inc Address
  | Dec Address
  | Add Address (Either Address Value)
  | Sub Address (Either Address Value)
  | Mul Address (Either Address Value)
  | Div Address (Either Address Value)
  | Label Identifier
  | Jmp Identifier
  | Cmp (Either Address Value) (Either Address Value)
  | Jne Identifier
  | Je Identifier
  | Jge Identifier
  | Jg Identifier
  | Jle Identifier
  | Jl Identifier
  | Call Identifier
  | Ret
  | Msg [Either String Address]
  | End
  | Jnz (Either Address Value) (Either Address Offset)
  deriving Show
  
data ProgramIO
  = JumpToOffset Int
  | JumpToLabel { fnCall :: Bool, jumpToLabel :: Identifier }
  | PreviousStack
  | Print String
  | Terminate

-- ListZipper can be seen as a datatype representing a list focused on a specific point
-- In our case, the list is our program (a sequence of instructions), and the point is the instruction being interpreted
data ListZipper a = ListZipper { previous :: [a], current :: a, next :: [a] }
  deriving Show

-- ListZipper function, mostly uninteresting

atStart :: [a] -> Maybe (ListZipper a)
atStart [] = Nothing
atStart (a : as) = Just (ListZipper [] a as)

stepFwd :: ListZipper a -> Maybe (ListZipper a)
stepFwd (ListZipper _ _ []) = Nothing
stepFwd (ListZipper ps a (b:bs)) = Just (ListZipper (a : ps) b bs)

stepBwd :: ListZipper a -> Maybe (ListZipper a)
stepBwd (ListZipper [] _ _) = Nothing
stepBwd (ListZipper (b : bs) a ns) = Just (ListZipper bs b (a : ns))

move :: Int -> ListZipper a -> Maybe (ListZipper a)
move n z = case compare n 0 of
  LT -> maybe (Just z) (move (n + 1)) (stepBwd z)
  EQ -> Just z
  GT -> move (n - 1) =<< stepFwd z

-- Functions to lookup addresses and set their values

lookupAddress :: Maybe Address -> State Registers Value
lookupAddress a = gets $ fromMaybe 0 . M.lookup a

setAddress :: Maybe Address -> Value -> State Registers ()
setAddress a v = modify (M.insert a v)

-- | setAddressWith f a v sets *a = f *a v
setAddressWith :: (Value -> Value -> Value) -> Maybe Address -> Value -> State Registers ()
setAddressWith f a v = modify (M.insertWith (flip f) a v)

-- | An instruction step can only modify registers. If it's a jump or a print it returns a ProgramIO spec
instructionStep :: Instruction -> State Registers (Maybe ProgramIO)
instructionStep i = case i of
  Mov a (Right v) -> setAddress (Just a) v >> pure Nothing
  Mov a (Left from) -> do
    v <- lookupAddress (Just from)
    setAddress (Just a) v
    pure Nothing
  Inc a -> setAddressWith (+) (Just a) 1 >> pure Nothing
  Dec a -> setAddressWith (+) (Just a) (-1) >> pure Nothing
  Jnz a b -> do
    v <- either (lookupAddress . Just) pure a
    offset <- either (lookupAddress . Just) pure b
    pure (if v /= 0 then Just (JumpToOffset offset) else Nothing)
  Add a b -> arithInstruction (+) a b
  Sub a b -> arithInstruction (-) a b
  Mul a b -> arithInstruction (*) a b
  Div a b -> arithInstruction div a b
  Label _ -> pure Nothing -- Label definitions are parsed before execution
  Call labelId -> pure (Just (JumpToLabel True labelId))
  Cmp a b -> do
    va <- either (lookupAddress . Just) pure a
    vb <- either (lookupAddress . Just) pure b
    setAddress Nothing (case compare va vb of
      GT -> 1
      EQ -> 0
      LT -> -1)
    pure Nothing
  Jmp labelId -> jumpInstruction (const True) labelId
  Jne labelId -> jumpInstruction (/= 0) labelId
  Je labelId -> jumpInstruction (== 0) labelId
  Jge labelId -> jumpInstruction (>= 0) labelId
  Jg labelId -> jumpInstruction (> 0) labelId
  Jle labelId -> jumpInstruction (<= 0) labelId
  Jl labelId -> jumpInstruction (< 0) labelId
  Ret -> pure (Just PreviousStack)
  End -> pure (Just Terminate)
  Msg l -> Just . Print <$> foldrM (\ v soFar -> do
    pr <- either pure (fmap show . lookupAddress . Just) v
    pure (pr <> soFar)) "" l
  where
    arithInstruction :: (Int -> Int -> Int) -> Address -> Either Address Value -> State Registers (Maybe a)
    arithInstruction f a b = do
      v <- either (lookupAddress . Just) pure b
      setAddressWith f (Just a) v
      pure Nothing
    jumpInstruction :: (Int -> Bool) -> Identifier -> State Registers (Maybe ProgramIO)
    jumpInstruction test labelId = do
      v <- lookupAddress Nothing
      pure (if test v then Just (JumpToLabel False labelId) else Nothing)
  
-- Execution State
data Env a = Env { registers :: Registers, callstack :: CallStack a } deriving Show
type RunM a = RWS (Labels a) (Maybe String) (Env a)

toEnv :: State Registers x -> RunM a x
toEnv f = rws $ \ _labels env -> (\ !(x, newRs) -> (x, env { registers = newRs }, Nothing)) (runState f (registers env))

pushToStack :: ListZipper a -> RunM a ()
pushToStack n = modify (\ e -> e { callstack = n : callstack e })

popStack :: RunM a (Maybe (ListZipper a))
popStack = do
  h <- gets (listToMaybe . callstack)
  modify (\ e -> e { callstack = tail (callstack e) })
  pure h

clearStack :: RunM a ()
clearStack = modify (\ e -> e { callstack = [] })

-- | runInstructions: Do instructionStep, and perform ProgramIO if needed
runInstructions :: ListZipper Instruction -> RunM Instruction ()
runInstructions i = do
  mio <- toEnv (instructionStep (current i))
  case mio of
    Nothing -> maybe (pure ()) runInstructions $ stepFwd i
    Just (JumpToOffset offset) -> maybe (pure ()) runInstructions $ move offset i
    Just (JumpToLabel fCall labl) -> do
      when fCall (maybe (pure ()) pushToStack (stepFwd i))
      labelCode <- asks (M.lookup labl)
      maybe (error ("No such label: " <> labl)) runInstructions $ labelCode
    Just PreviousStack -> do
      resumeFrom <- popStack
      maybe (error "Unexpected ret") runInstructions resumeFrom
    Just (Print s) -> tell (Just s) >> maybe (pure ()) runInstructions (stepFwd i)
    Just Terminate -> clearStack

-- Parsing stuff. Not really interesting

type Parser = Parsec Void String

token :: Parser a -> Parser a
token = lexeme (space space1 empty empty)

instructionParser :: Parser (Maybe Instruction)
instructionParser = space space1 (() <$ string ";" <* many anySingle) empty *>
  ((Just <$> (
      ((Mov <$ token (string "mov")) <*> address <* optional (token (string ",")) <*> addressOrValue)
  <|> ((Inc <$ token (string "inc")) <*> address)
  <|> ((Dec <$ token (string "dec")) <*> address)
  <|> ((Jnz <$ token (string "jnz")) <*> addressOrValue <*> addressOrOffset)
  <|> ((Call <$ token (string "call")) <*> labelP)
  <|> ((Jne <$ token (string "jne")) <*> labelP)
  <|> ((Je <$ token (string "je")) <*> labelP)
  <|> ((Jge <$ token (string "jge")) <*> labelP)
  <|> ((Jg <$ token (string "jg")) <*> labelP)
  <|> ((Jle <$ token (string "jle")) <*> labelP)
  <|> ((Jl <$ token (string "jl")) <*> labelP)
  <|> ((Jmp <$ token (string "jmp")) <*> labelP)
  <|> ((Cmp <$ token (string "cmp")) <*> addressOrValue <* optional (token (string ",")) <*> addressOrValue)
  <|> ((Add <$ token (string "add")) <*> address <* optional (token (string ",")) <*> addressOrValue)
  <|> ((Sub <$ token (string "sub")) <*> address <* optional (token (string ",")) <*> addressOrValue)
  <|> ((Mul <$ token (string "mul")) <*> address <* optional (token (string ",")) <*> addressOrValue)
  <|> ((Div <$ token (string "div")) <*> address <* optional (token (string ",")) <*> addressOrValue)
  <|> ((Msg <$ token (string "msg")) <*> argList)
  <|> (End <$ token (string "end"))
  <|> (Ret <$ token (string "ret"))
  <|> (Label <$> labelP <* string ":")
  ) <* space space1 (() <$ string ";" <* many anySingle) empty)
  <|> (Nothing <$ string ";" <* many anySingle)
  <|> (Nothing <$ eof))
  
address :: Parser Address
address = token ((:) <$> letterChar <*> many alphaNumChar)

value :: Parser Value
value = token (signed (pure ()) decimal)

addressOrValue :: Parser (Either Address Value)
addressOrValue = (Left <$> address) <|> (Right <$> value)

offsetP :: Parser Offset
offsetP = token (signed (pure ()) decimal)

addressOrOffset :: Parser (Either Address Offset)
addressOrOffset = (Left <$> address) <|> (Right <$> offsetP)

labelP :: Parser Identifier
labelP = token (many (satisfy (/= ':')))

argList :: Parser [Either String Address]
argList = addressOrString `sepBy` token (string ",")

addressOrString :: Parser (Either String Address)
addressOrString = (Left <$> stringP) <|> (Right <$> address)

stringP :: Parser String
stringP = do
 _ <- string "'"
 res <- many (satisfy (/= '\''))
 _ <- string "'"
 pure res


-- Put everything together
 
simpleAssembler :: [String] -> (Env Instruction, Maybe String)
simpleAssembler is = execRWS
  (maybe (pure ()) runInstructions instructions)
  (maybe M.empty parseLabels instructions)
  (Env M.empty [])
  where
    parseLabels is' = addLabelQ (maybe M.empty parseLabels (stepFwd is'))
      where addLabelQ = case current is' of { Label l -> M.insert l is'; _ -> id}
    instructions = atStart $ mapMaybe (either (error . show) id . parse (instructionParser <* eof) "Input") is

interpret :: String -> Maybe String
interpret prgm = case simpleAssembler (lines prgm) of
  (env, res) -> guard (null (callstack env)) >> res
