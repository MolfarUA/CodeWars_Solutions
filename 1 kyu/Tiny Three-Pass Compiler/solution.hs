module TinyThreePassCompiler where


import           Control.Applicative
import           Control.Lens
import           Control.Monad.State
import qualified Data.Map as M
import           Data.Maybe (fromJust, listToMaybe)


data AST = Imm Int
         | Arg Int
         | Add AST AST
         | Sub AST AST
         | Mul AST AST
         | Div AST AST
         deriving (Eq, Show)


data Token = TChar Char
           | TInt Int
           | TStr String
           deriving (Eq, Show)


alpha, digit :: String
alpha = ['a'..'z'] ++ ['A'..'Z']
digit = ['0'..'9']

tokenize :: String -> [Token]
tokenize [] = []
tokenize xxs@(c:cs)
  | c `elem` "-+*/()[]" = TChar c : tokenize cs
  | not (null i) = TInt (read i) : tokenize is
  | not (null s) = TStr s : tokenize ss
  | otherwise = tokenize cs
  where
    (i, is) = span (`elem` digit) xxs
    (s, ss) = span (`elem` alpha) xxs


------------------------------------------------------------------------------
-- | Parser state
data ParserSate = ParserSate { _input     :: [ Token ]
                             , _pos       :: Int
                             , _variables :: M.Map String Int
                             }
-- normally this would be template haskell.
input :: Lens' ParserSate [Token]
input a ~(ParserSate x y z) = fmap (\w -> ParserSate w y z) (a x)
pos :: Lens' ParserSate Int
pos a ~(ParserSate x y z) = fmap (\w -> ParserSate x w z) (a y)
variables :: Lens' ParserSate (M.Map String Int)
variables a ~(ParserSate x y z) = fmap (\w -> ParserSate x y w) (a z)


type Parser a = (StateT ParserSate Maybe) a


runParser :: Parser a -> [Token] -> Maybe a
runParser p i = evalStateT p (ParserSate i 0 M.empty)


------------------------------------------------------------------------------
-- | next token
next :: Parser Token
next = do
  t <- liftM listToMaybe $ use input
  input %= tail
  lift t


------------------------------------------------------------------------------
-- | Asserts that the next token is the one we expect
token :: Char -> Parser ()
token x = next >>= \t -> guard $ t == TChar x


------------------------------------------------------------------------------
-- | Reads a variable name and creates the symbol table entry
variable :: Parser ()
variable = next >>= \t -> case t of
  (TStr name) -> do
    p <- pos <%= succ
    variables %= M.insert name (p - 1)
  _           -> mzero


------------------------------------------------------------------------------
-- | Parses a single value either immediate or a variable reference
value :: Parser AST
value = immVal <|> varVal
  where
    immVal = next >>= \t -> case t of
      (TInt i) -> return $ Imm i
      _        -> mzero
    varVal = next >>= \t -> case t of
      (TStr name) -> do
        p <- liftM (M.lookup name) $ use variables
        lift $ Arg <$> p
      _           -> mzero


------------------------------------------------------------------------------
-- | Parser
pass1 :: String -> AST
pass1 = fromJust . runParser function . tokenize
  where
    function      = do
      token '[' *> argument_list <* token ']'
      expression
    argument_list = void $ many variable
    expression    = term >>= expression'  -- left to right recursion rewrite
    expression' l =     (token '+' *> liftM (Add l) term >>= expression')
                    <|> (token '-' *> liftM (Sub l) term >>= expression')
                    <|> return l
    term          = factor >>= term'      -- left to right recursion rewrite
    term' l       =     (token '*' *> liftM (Mul l) factor >>= term')
                    <|> (token '/' *> liftM (Div l) factor >>= term')
                    <|> return l
    factor        = token '(' *> expression <* token ')' <|> value


------------------------------------------------------------------------------
instance Plated AST where
  plate f (Add x y) = Add <$> f x <*> f y
  plate f (Sub x y) = Sub <$> f x <*> f y 
  plate f (Mul x y) = Mul <$> f x <*> f y 
  plate f (Div x y) = Div <$> f x <*> f y
  plate _ x         = pure x


------------------------------------------------------------------------------
-- | Simplifier
pass2 :: AST -> AST
pass2 = transform f
  where f (Add (Imm a) (Imm b)) = Imm $ a + b
        f (Sub (Imm a) (Imm b)) = Imm $ a - b
        f (Mul (Imm a) (Imm b)) = Imm $ a * b
        f (Div (Imm a) (Imm b)) = Imm $ a `div` b
        f x = x        


------------------------------------------------------------------------------
-- | Intruction set
data Instruction = IM Int
                 | AR Int
                 | PU | PO | SW | AD | SU | MU | DI deriving (Eq, Show)


generate :: AST -> [ Instruction ]
generate (Imm x) = [ IM x, PU ]
generate (Arg x) = [ AR x, PU ]
generate (Add x1 x2) = (generate x1) ++ (generate x2) ++ popPush AD
generate (Sub x1 x2) = (generate x1) ++ (generate x2) ++ popPush SU
generate (Mul x1 x2) = (generate x1) ++ (generate x2) ++ popPush MU
generate (Div x1 x2) = (generate x1) ++ (generate x2) ++ popPush DI


popPush :: Instruction -> [Instruction]
popPush x = [ PO, SW, PO, x, PU ]


tPUPOSW :: [Instruction] -> [Instruction]
tPUPOSW (PU:PO:SW:t) = SW:t
tPUPOSW x            = x


tPU_SWPO_ :: [Instruction] -> [Instruction]
tPU_SWPO_ (PU:(IM x):SW:PO:AD:t) = SW:(IM x):AD:t
tPU_SWPO_ (PU:(AR x):SW:PO:MU:t) = SW:(AR x):MU:t
tPU_SWPO_ (PU:(IM x):SW:PO:SU:t) = SW:(IM x):SW:SU:t
tPU_SWPO_ (PU:(AR x):SW:PO:DI:t) = SW:(AR x):SW:DI:t
tPU_SWPO_ x                      = x


t_SW_SW :: [Instruction] -> [Instruction]
t_SW_SW ((IM x):SW:(IM y):SW:t) = (IM y):SW:(IM x):t
t_SW_SW ((IM x):SW:(AR y):SW:t) = (AR y):SW:(IM x):t
t_SW_SW ((AR x):SW:(IM y):SW:t) = (IM y):SW:(AR x):t
t_SW_SW ((AR x):SW:(AR y):SW:t) = (AR y):SW:(AR x):t
t_SW_SW x                       = x



peepHole :: [Instruction] -> [Instruction]
peepHole = transform t_SW_SW . transform tPU_SWPO_ . transform tPUPOSW


------------------------------------------------------------------------------
-- | Code generator
pass3 :: AST -> [ String ]
pass3 = map show . peepHole . init . generate


compile :: String -> [String]
compile = pass3 . pass2 . pass1

_________________________________________________________________________
module TinyThreePassCompiler where

import Text.ParserCombinators.Poly.Plain       
import Text.ParserCombinators.Poly.Base
import Data.Char
import Data.List
import Control.Monad

data AST = Imm Int
         | Arg Int
         | Add AST AST
         | Sub AST AST
         | Mul AST AST
         | Div AST AST
         deriving (Eq, Show)

compile :: String -> [String]
compile = pass3 . pass2 . pass1

pass1 :: String -> AST
pass1 = either error id . fst . runParser pass1Parser

pass2 :: AST -> AST
pass2 ast =
    case ast of
        (Add (Imm n1) (Imm n2)) -> Imm (n1 + n2)
        (Add a b)               -> recurse Add (+) a b
        (Sub (Imm n1) (Imm n2)) -> Imm (n1 - n2)
        (Sub a b)               -> recurse Sub (-) a b
        (Mul (Imm n1) (Imm n2)) -> Imm (n1 * n2)
        (Mul a b)               -> recurse Mul (*) a b
        (Div (Imm n1) (Imm n2)) -> Imm (n1 `div` n2)
        (Div a b)               -> recurse Div div a b
        _                       -> ast
  where
    recurse constructor op astA astB = 
        case (pass2 astA, pass2 astB) of
            (Imm n1, Imm n2) -> Imm (n1 `op` n2)
            (astA', astB')   -> constructor astA' astB'

pass3 :: AST -> [String]
pass3 ast = 
    case ast of
        (Imm n)   -> ["IM " ++ show n]
        (Arg n)   -> ["AR " ++ show n]
        (Add x y) -> operateOn x y "AD"
        (Sub x y) -> operateOn x y "SU"
        (Mul x y) -> operateOn x y "MU"
        (Div x y) -> operateOn x y "DI"
  where
    operateOn ast1 ast2 instruction = 
        pass3 ast1 ++ "PU" : pass3 ast2 ++ ["SW", "PO", instruction] 

--Parsing-----------------------------------------------------

pass1Parser :: Parser Char AST
pass1Parser = do
    arguments <- brackets '[' ']' $ sepBy (stringOf isAlpha) (stringOf (==' '))
    spaces
    let number = (Imm . read) <$> stringOf isDigit 
        variable = 
            flip adjustErrBad (++ "Unknown variable") $ 
            Arg <$> lookupParse (stringOf isAlpha) (zip arguments [0..]) 
        expression = leftAssociate term [('+', Add), ('-', Sub)]
        term       = leftAssociate factor [('*', Mul), ('/', Div)]
        factor     = brackets '(' ')' expression <|> number <|> variable
    expression 

-- Fold over a series of parses separated by operators to build a parse tree.
leftAssociate :: Parser Char AST -> [(Char, AST -> AST -> AST)] 
                 -> Parser Char AST
leftAssociate parser dict =
    foldl' (\arg1 (operator, arg2) -> operator arg1 arg2) 
        <$> (parser <* spaces) 
        <*> many ((,) 
            <$> (lookupParse next dict <* spaces) 
            <*> (parser <* spaces)) 

lookupParse :: Eq a => Parser t a -> [(a, b)] -> Parser t b
lookupParse parser dict = do
    result <- parser 
    maybe (fail "") return (lookup result dict)

spaces :: Parser Char ()
spaces  = void $ many (satisfy (== ' '))

stringOf :: (Char -> Bool) -> Parser Char String
stringOf = many1 . satisfy 

brackets :: Char -> Char -> Parser Char a -> Parser Char a
brackets left right = 
    bracket (satisfy (== left) >> spaces) (spaces >> satisfy (== right))
    
____________________________________________________
module TinyThreePassCompiler where

import Data.List
import Data.Maybe

data AST = Imm Int
         | Arg Int
         | Add AST AST
         | Sub AST AST
         | Mul AST AST
         | Div AST AST
         deriving (Eq, Show)

data Token = TChar Char
           | TInt Int
           | TStr String
           deriving (Eq, Show)

-- Helpers ---

alpha, digit :: String
alpha = ['a'..'z'] ++ ['A'..'Z']
digit = ['0'..'9']

tokenize :: String -> [Token]
tokenize [] = []
tokenize xxs@(c:cs)
  | c `elem` "-+*/()[]" = TChar c : tokenize cs
  | not (null i) = TInt (read i) : tokenize is
  | not (null s) = TStr s : tokenize ss
  | otherwise = tokenize cs
  where
    (i, is) = span (`elem` digit) xxs
    (s, ss) = span (`elem` alpha) xxs
    
splitargs :: [Token] -> ([Token], [Token])
splitargs line =
  let (args, expr) = span (/= (TChar ']')) line
  in  (tail args, tail expr)
    
splitexpr :: [Token] -> ([Token], [Token]) -> Int -> ([Token], Token, [Token])
splitexpr operations (left, right) bracecnt
  | left == [] = ([], TChar 'x', right)
  | (bracecnt == 0) && (e `elem` operations) = (ehead, e, etail)
  | e == (TChar '(') = splitexpr operations (ehead, [e] ++ etail) (bracecnt + 1)
  | e == (TChar ')') = splitexpr operations (ehead, [e] ++ etail) (bracecnt - 1)
  | otherwise = splitexpr operations (ehead, [e] ++ etail) bracecnt
  where
    (ehead, e, etail) = (init left, last left, right)

--- Pass 1 ---

expression :: [Token] -> [Token] -> AST
expression args expr
  | op == (TChar '+') = Add (expression args left) (term args right)
  | op == (TChar '-') = Sub (expression args left) (term args right)
  | otherwise = term args expr
  where
    (left, op, right) = splitexpr [TChar '+', TChar '-'] (expr, []) 0

term :: [Token] -> [Token] -> AST
term args expr
  | op == (TChar '*') = Mul (term args left) (factor args right)
  | op == (TChar '/') = Div (term args left) (factor args right)
  | otherwise = factor args expr
  where
    (left, op, right) = splitexpr [TChar '*', TChar '/'] (expr, []) 0
 
factor :: [Token] -> [Token] -> AST   
factor args (TInt i : []) = Imm i
factor args (arg : []) = Arg $ fromJust (arg `elemIndex` args)
factor args (TChar '(' : expr) = expression args (init expr)

--- Pass 2 ---

reduce :: AST -> AST
reduce (Add (Imm a) (Imm b)) = Imm (a + b)
reduce (Add (Imm 0) y) = reduce y
reduce (Add x (Imm 0)) = reduce x
reduce (Add x y) = Add (reduce x) (reduce y)

reduce (Sub (Imm a) (Imm b)) = Imm (a - b)
reduce (Sub x (Imm 0)) = reduce x
reduce (Sub x y) = Sub (reduce x) (reduce y)

reduce (Mul (Imm a) (Imm b)) = Imm (a * b)
reduce (Mul (Imm 1) x) = reduce x
reduce (Mul x (Imm 1)) = reduce x
reduce (Mul x y) = Mul (reduce x) (reduce y)

reduce (Div (Imm a) (Imm b)) = Imm (a `div` b)
reduce (Div x (Imm 1)) = reduce x
reduce (Div x y) = Div (reduce x) (reduce y)

reduce (Imm i) = Imm i
reduce (Arg n) = Arg n

--- Pass 3 ---

assemble :: AST -> [String]
assemble (Imm i) = ["IM " ++ show i]
assemble (Arg n) = ["AR " ++ show n]
assemble (Add x y) = (assemble x) ++ ["PU"] ++ (assemble y) ++ ["SW", "PO", "AD"]
assemble (Sub x y) = (assemble x) ++ ["PU"] ++ (assemble y) ++ ["SW", "PO", "SU"]
assemble (Mul x y) = (assemble x) ++ ["PU"] ++ (assemble y) ++ ["SW", "PO", "MU"]
assemble (Div x y) = (assemble x) ++ ["PU"] ++ (assemble y) ++ ["SW", "PO", "DI"]

---

compile :: String -> [String]
compile = pass3 . pass2 . pass1

pass1 :: String -> AST
pass1 line =
    let tokens = tokenize line
        (args, expr) = splitargs tokens
    in  expression args expr

pass2 :: AST -> AST
pass2 = reduce . reduce   -- double reduce to get more power of reducing

pass3 :: AST -> [String]
pass3 = assemble

________________________________________________________________________________
{-# LANGUAGE FlexibleContexts #-}
module TinyThreePassCompiler where

import Data.Either ( fromRight )
import Data.Maybe ( fromJust )
import Text.Parsec ( token, many, chainl1, (<|>) )
import Text.Parsec.Pos ( newPos )
import qualified Text.Parsec as P

data AST = Imm Int
         | Arg Int
         | Add AST AST
         | Sub AST AST
         | Mul AST AST
         | Div AST AST
         deriving (Eq, Show)

data Token = TChar Char
           | TInt Int
           | TStr String
           deriving (Eq, Show)

alpha, digit :: String
alpha = ['a'..'z'] ++ ['A'..'Z']
digit = ['0'..'9']

tokenize :: String -> [Token]
tokenize [] = []
tokenize xxs@(c:cs)
  | c `elem` "-+*/()[]" = TChar c : tokenize cs
  | not (null i) = TInt (read i) : tokenize is
  | not (null s) = TStr s : tokenize ss
  | otherwise = tokenize cs
  where
    (i, is) = span (`elem` digit) xxs
    (s, ss) = span (`elem` alpha) xxs

compile :: String -> [String]
compile = pass3 . pass2 . pass1

pass1 :: String -> AST
pass1 = parse . tokenize

parse :: [Token] -> AST
parse = fromRight undefined . P.parse function "" where
  pos = const $ newPos "" 1 1
  variable = token show pos $ \t ->
    case t of
      TStr s -> Just s
      _ -> Nothing
  char c = token show pos $ \t ->
    case t of
      TChar c' | c == c' -> Just c
      _ -> Nothing
  number = token show pos $ \t ->
    case t of
      TInt i -> Just i
      _ -> Nothing
  function = do
    args <- flip zip [0..] <$> (char '[' *> many variable <* char ']')
    let expression = chainl1 term addOp
        term = chainl1 factor mulOp
        factor = Imm <$> number
             <|> Arg . fromJust . flip lookup args <$> variable
             <|> char '(' *> expression <* char ')'
        addOp = char '+' *> pure Add
            <|> char '-' *> pure Sub
        mulOp = char '*' *> pure Mul
            <|> char '/' *> pure Div
    expression
    
pass2 :: AST -> AST
pass2 ast =
  case ast of
    Add lhs rhs -> foldConst Add (+) lhs rhs
    Sub lhs rhs -> foldConst Sub (-) lhs rhs
    Mul lhs rhs -> foldConst Mul (*) lhs rhs
    Div lhs rhs -> foldConst Div div lhs rhs
    _ -> ast

foldConst :: (AST -> AST -> AST) -> (Int -> Int -> Int) -> AST -> AST -> AST
foldConst f g lhs rhs =
  let lhs' = pass2 lhs
      rhs' = pass2 rhs
  in case (lhs', rhs') of
    (Imm l, Imm r) -> Imm (l `g` r)
    _              -> lhs' `f` rhs'
    
pass3 :: AST -> [String]
pass3 ast =
  case ast of
    Imm i -> ["IM " ++ show i]
    Arg a -> ["AR " ++ show a]
    Add lhs rhs -> binop "AD" lhs rhs
    Sub lhs rhs -> binop "SU" lhs rhs
    Mul lhs rhs -> binop "MU" lhs rhs
    Div lhs rhs -> binop "DI" lhs rhs

binop :: String -> AST -> AST -> [String]
binop op lhs rhs = pass3 lhs ++ ["PU"] ++ pass3 rhs ++ ["SW", "PO", op]
