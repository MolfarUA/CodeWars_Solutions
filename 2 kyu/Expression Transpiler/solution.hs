{-# LANGUAGE FlexibleContexts #-}
module Transpiler where

import Text.Parsec
import Data.Bifunctor (bimap)
import Data.List (intercalate)

transpile :: String -> Either String String
transpile = bimap (const "Hugh?") id . parse parser ""

symbol s = string s *> spaces
braces   = symbol "{" `between` symbol "}"
brackets = symbol "(" `between` symbol ")"
name = (:) <$> (char '_' <|> letter) <*> many (char '_' <|> alphaNum) <* spaces
number = many1 digit <* spaces
nameOrNum = name <|> number

parser = spaces *> (try parseAN <|> parseA1) <* eof
parseAN = showAppN <$> parseE <*> brackets parseP <*> option [] ((:[]) <$> parseL)
parseA1 = showApp1 <$> parseE <*> parseL
parseE = nameOrNum <|> parseL
parseP = parseE `sepBy` symbol ","
parsePL = intercalate "," <$> (nameOrNum `sepBy1` symbol ",") <* symbol "->"
parseL = braces $ showL <$> many (try parsePL) <*> many nameOrNum

showApp1 e p = e ++ "(" ++ p ++ ")"
showAppN e es ps = e ++ "(" ++ intercalate "," (es ++ ps) ++ ")"
showL ps ns = "(" ++ intercalate "," ps ++ "){" ++ concatMap (++ ";") ns ++ "}"
_____________________________________________________
module Transpiler where

import Text.Parsec.Language
import Text.Parsec.String
import Text.Parsec.Token
import Text.Parsec hiding((<|>))
import Control.Applicative hiding (many)
import Data.List (intercalate)
import Data.Functor
import Data.Maybe

TokenParser{ parens = m_parens
           , braces = m_braces
           , identifier = m_identifier
           , reservedOp = m_reservedOp
           , commaSep = m_commaSep
           , commaSep1 = m_commaSep1
           , integer = m_integer
           , whiteSpace = m_whiteSpace } = makeTokenParser emptyDef {
            reservedOpNames = ["->"]
           }


data Function = F1 Expression Parameters (Maybe Lambda) | F2 Expression Lambda
  deriving(Show)
data Expression = E1 NameOrNumber | E2 Lambda
  deriving(Show)
newtype NameOrNumber = NameOrNumber String
  deriving(Show)
newtype Parameters = Parameters [Expression]
  deriving(Show)
data Lambda = Lambda LambdaParams LambdaStatements
  deriving(Show)
newtype LambdaStatements = LambdaStatements [NameOrNumber]
  deriving(Show)
newtype LambdaParams = LambdaParams [NameOrNumber]
  deriving(Show)

transpile :: String -> Either String String
transpile = mapBoth (const "Hugh?") write . runP (m_whiteSpace *> function_parser <* eof) () ""
  
mapBoth f _ (Left x)  = Left (f x)
mapBoth _ f (Right x) = Right (f x)

function_parser :: Parser Function
function_parser = try f1 <|> try f2
  where f1 = F1 <$> expression_parser <*> m_parens parameter_parser <*>
                     option Nothing (Just <$> lambda_parser)
        f2 = F2 <$> expression_parser <*> lambda_parser
        parameter_parser = Parameters <$> m_commaSep expression_parser

expression_parser = (E1 <$> name_or_number_parser) <|> (E2 <$> lambda_parser)

lambda_parser = m_braces $ Lambda <$> option (LambdaParams []) (try p) <*> b
  where p = LambdaParams <$> (m_commaSep1 name_or_number_parser <* m_reservedOp "->")
        b = LambdaStatements <$> many name_or_number_parser

name_or_number_parser = NameOrNumber <$> p
  where p = m_identifier <|> show <$> m_integer


class Write t where
  write :: t -> String

instance Write Function where
  write f = write a ++ "(" ++ write b ++ ")"
    where (a, b) = normalize f
          normalize (F1 exp (Parameters params) lambda) = 
            (exp, Parameters (params ++ map E2 (maybeToList lambda)))
          normalize (F2 exp lambda) = (exp, Parameters [E2 lambda])

instance Write Expression where
  write (E1 n) = write n
  write (E2 n) = write n

instance Write NameOrNumber where
  write (NameOrNumber s) = s

instance Write Parameters where
  write (Parameters arr) = intercalate "," . map write $ arr

instance Write Lambda where
  write (Lambda params stmts) = p ++ b    
    where p = "(" ++ write params ++ ")"
          b = "{" ++ write stmts ++ "}"
    
instance Write LambdaParams where
  write (LambdaParams params) = intercalate "," (map write params)

instance Write LambdaStatements where
  write (LambdaStatements stmts) = concatMap ((++";").write) stmts
  
_____________________________________________________
module Transpiler where

import Data.Maybe

import Control.Applicative 
import Text.Parsec hiding ((<|>), some, many)
import Text.Parsec.String
pMaybe :: Parser a -> Parser (Maybe a)
pMaybe p = tryParsers [p', return Nothing] where
  p' = do
    a <- p
    return $ Just a
tryParsers :: [Parser a] -> Parser a
tryParsers = foldr (<|>) empty . map try

-- src lang

-- function ::= expression "(" [parameters] ")" [lambda]
--            | expression lambda
-- expression ::= nameOrNumber
--              | lambda
-- parameters ::= expression ["," parameters]
-- lambdaparam ::= nameOrNumber ["," lambdaparam]
-- lambdastmt  ::= nameOrNumber [lambdastmt]
-- lambda ::= "{" [lambdaparam "->"] [lambdastmt] "}"
-- nameOrNumber ::= name 
--                | number
-- name ::= [_A-Za-z][_A-Za-z0-9]*
-- number ::= [0-9]+

-- AST

data Name = Name String 
data Number = Number String 
data NameOrNumber = NameOrNumber (Either Name Number) 
data LambdaParam = LambdaParam NameOrNumber (Maybe LambdaParam) 
data LambdaStmt = LambdaStmt NameOrNumber (Maybe LambdaStmt) 
data Lambda = Lambda (Maybe LambdaParam) (Maybe LambdaStmt) 
data Expression = Expression (Either NameOrNumber Lambda) 
data Parameters = Parameters Expression (Maybe Parameters) 
data Function = Function (Either (Expression, Maybe Parameters, Maybe Lambda) (Expression, Lambda)) 

-- Parsing

name :: Parser Name
name = do
  head <- oneOf "_QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm"
  tail <- many (oneOf "_QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm0123456789")
  return $ Name (head:tail)
  
number :: Parser Number
number = do
  num <- many1 (oneOf "0123456789")
  return $ Number num
  
nameOrNumber :: Parser NameOrNumber
nameOrNumber = tryParsers [p1, p2] where
  p1 = do
    n <- name
    return $ NameOrNumber $ Left n
  p2 = do
    n <- number
    return $ NameOrNumber $ Right n
    
lambdaParam :: Parser LambdaParam
lambdaParam = do
  n <- nameOrNumber
  spaces
  mlp <- pMaybe p
  return $ LambdaParam n mlp where
  p = do
    char ','
    spaces
    lp <- lambdaParam
    return lp
  
lambdaStmt :: Parser LambdaStmt
lambdaStmt = do
  n <- nameOrNumber
  spaces
  mls <- pMaybe lambdaStmt
  return $ LambdaStmt n mls
  
lambda :: Parser Lambda 
lambda = do
  char '{'
  spaces
  mlp <- pMaybe p
  spaces
  mls <- pMaybe lambdaStmt
  spaces
  char '}'
  return $ Lambda mlp $ mls where
  p = do
    lp <- lambdaParam
    spaces
    char '-'
    char '>'
    return lp

expression :: Parser Expression
expression = tryParsers [p1, p2] where
  p1 = do
    n <- nameOrNumber
    return $ Expression $ Left n
  p2 = do
    n <- lambda
    return $ Expression $ Right n
    
parameters :: Parser Parameters
parameters = do
  e <- expression
  spaces
  mpa <- pMaybe p
  return $ Parameters e mpa where
  p = do
    char ','
    spaces
    pa <- parameters
    return pa
    
function :: Parser Function
function = tryParsers [p1, p2] where
  p1 = do
    e <- expression
    spaces
    char '('
    spaces
    mpa <- pMaybe parameters
    spaces
    char ')'
    spaces 
    mla <- pMaybe lambda
    return $ Function $ Left (e, mpa, mla)
  p2 = do
    e <- expression
    spaces
    la <- lambda
    return $ Function $ Right (e, la)

-- tgt

-- function ::= expression "(" [parameters] ")"
-- expression ::= nameOrNumber
--              | lambda
-- parameters ::= expression ["," parameters]
-- lambdaparam ::= nameOrNumber ["," lambdaparam]
-- lambdastmt  ::= nameOrNumber ";" [lambdastmt]
-- lambda ::= "(" [lambdaparam] "){" [lambdastmt] "}"

showM :: Show a => Maybe a -> String
showM Nothing = ""
showM (Just a) = show a

instance Show Name where 
  show (Name str) = str
instance Show Number where 
  show (Number str) = str  
instance Show NameOrNumber where
  show (NameOrNumber (Left n)) = show n
  show (NameOrNumber (Right n)) = show n
instance Show LambdaParam where
  show (LambdaParam n mlp) = if isNothing mlp then show n 
    else show n ++ "," ++ showM mlp
instance Show LambdaStmt where
  show (LambdaStmt n mls) = if isNothing mls then show n ++ ";"
    else show n ++ ";" ++ showM mls
instance Show Lambda where
  show (Lambda mlp mls) = "(" ++ showM mlp ++ "){" ++ showM mls ++ "}"
instance Show Expression where
  show (Expression (Left n)) = show n
  show (Expression (Right n)) = show n
instance Show Parameters where
  show (Parameters e mpa) = if isNothing mpa then show e 
    else show e ++ "," ++ showM mpa
instance Show Function where
  show (Function (Left (e, mpa, mla))) = show e 
    ++ "(" 
    ++ if (not $ isNothing mpa) && (not $ isNothing mla) 
       then showM mpa ++ "," ++ showM mla ++ ")"
       else showM mpa ++ showM mla ++ ")"
  show (Function (Right (e, la))) = show e ++ "(" ++ show la ++ ")"
  
transpiler :: Parser String
transpiler = do
  spaces
  f <- function
  spaces
  return $ show f

transpile :: String -> Either String String
transpile s = case parse (transpiler <* eof) "Transpiler" s of
  Left sth -> Left "Hugh?"
  Right msg -> Right msg

_____________________________________________________
module Transpiler where

import           Data.List                      ( intercalate )
import           Text.Parsec                    ( (<|>)
                                                , char
                                                , choice
                                                , digit
                                                , eof
                                                , letter
                                                , many
                                                , many1
                                                , option
                                                , parse
                                                , sepBy
                                                , sepBy1
                                                , string
                                                , try
                                                )
import           Text.Parsec.String             ( Parser )

type Whitespaces = String
type Name = String
type Number = Int
data NameOrNumber = DataName Name
                  | DataNumber Number

newtype LambdaParam = LambdaParam NameOrNumber
newtype LambdaStatement = LambdaStatement NameOrNumber
data Lambda = Lambda [LambdaParam] [LambdaStatement]

data Expression = ExpressionNameOrNumber NameOrNumber
                | ExpressionLambda Lambda

newtype Parameter = Parameter Expression

data Function = FunctionWithParameters Expression [Parameter] [Lambda]
              | FunctionWithoutParameters Expression Lambda

instance Show NameOrNumber where
    show (DataName   n) = n
    show (DataNumber n) = show n

instance Show LambdaParam where
    show (LambdaParam n) = show n

instance Show LambdaStatement where
    show (LambdaStatement n) = show n

instance Show Lambda where
    show (Lambda ps sts) = ps' ++ sts'
      where
        ps'  = "(" ++ intercalate "," (map show ps) ++ ")"
        sts' = "{" ++ concatMap ((++ ";") . show) sts ++ "}"

instance Show Expression where
    show (ExpressionNameOrNumber n) = show n
    show (ExpressionLambda       l) = show l

instance Show Parameter where
    show (Parameter e) = show e

instance Show Function where
    show (FunctionWithParameters e ps ls) = show e ++ "(" ++ intercalate "," (map show ps ++ map show ls) ++ ")"
    show (FunctionWithoutParameters e l ) = show e ++ "(" ++ show l ++ ")"

transpile :: String -> Either String String
transpile str =
    let parsed = parse function "" str
    in  case parsed of
            Right s -> Right $ show s
            Left  _ -> Left "Hugh?"

whitespaces :: Parser Whitespaces
whitespaces = many (char ' ' <|> char '\t' <|> char '\n')

lexeme :: Parser a -> Parser a
lexeme p = do
    whitespaces
    x <- p
    whitespaces
    return x

dataName :: Parser NameOrNumber
dataName = do
    hd <- letter <|> char '_'
    tl <- many (letter <|> digit <|> char '_')
    return $ DataName $ hd : tl

dataNumber :: Parser NameOrNumber
dataNumber = do
    n <- many1 digit
    let m = read n
    return $ DataNumber m

nameOrNumber :: Parser NameOrNumber
nameOrNumber = dataName <|> dataNumber

lambdaStatement :: Parser LambdaStatement
lambdaStatement = LambdaStatement <$> nameOrNumber

lambdaParam :: Parser LambdaParam
lambdaParam = LambdaParam <$> nameOrNumber

lambdaParams :: Parser [LambdaParam]
lambdaParams = do
    params <- sepBy1 (lexeme lambdaParam) (char ',')
    lexeme $ string "->"
    return params

lambda :: Parser Lambda
lambda = do
    lexeme $ char '{'
    params     <- option [] (try lambdaParams)
    statements <- sepBy (lexeme lambdaStatement) whitespaces
    lexeme $ char '}'
    return $ Lambda params statements

expressionNameOrNumber :: Parser Expression
expressionNameOrNumber = ExpressionNameOrNumber <$> nameOrNumber

expressionLambda :: Parser Expression
expressionLambda = ExpressionLambda <$> lambda

expression :: Parser Expression
expression = choice [expressionNameOrNumber, expressionLambda]

parameter :: Parser Parameter
parameter = Parameter <$> expression

functionWithParameters :: Parser Function
functionWithParameters = do
    e <- lexeme expression
    lexeme $ char '('
    ps <- sepBy (lexeme parameter) (char ',')
    lexeme $ char ')'
    ls <- many (lexeme lambda)
    return $ FunctionWithParameters e ps ls

functionWithoutParameters :: Parser Function
functionWithoutParameters = do
    e <- lexeme expression
    l <- lexeme lambda
    return $ FunctionWithoutParameters e l

function :: Parser Function
function = choice (try <$> [functionWithParameters, functionWithoutParameters]) <* eof

_____________________________________________________
module Transpiler where

import Data.List
import Text.ParserCombinators.Parsec

alpha = '_' : ['a'..'z'] ++ ['A'..'Z']
nums = ['0'..'9']
rest = alpha ++ ['0'..'9']

transpile s = conv $ parse finalParser "" s
  where
    conv (Left _) = Left "Hugh?"
    conv (Right x) = Right x

name = (:) <$> oneOf alpha <*> (many $ oneOf rest) <* spaces
num = (string "0" <|> (:) <$> oneOf ['1'..'9'] <*> (many $ oneOf nums)) <* spaces
lit = try name <|> try num
param = (intercalate ",") <$> sepBy expression (string "," <* spaces)
param1 = (intercalate ",") <$> sepBy1 expression (string "," <* spaces)
finalParser = spaces *> function <* eof
expression = try lit <|> lambda
lambdaShort = char '{' *> spaces *> ((\x -> "(){" ++ x ++ "}") <$> statement) <* char '}' <* spaces
lambda = try lambdaLong <|> try lambdaShort
statement = (concat . fmap (++ ";")) <$> sepBy lit spaces

function = try (long <$> expression <*> mid <*> optionMaybe lambda)
       <|> try (short <$> expression <*> lambda)
  where
    long e p Nothing = e ++ "(" ++ p ++ ")"
    long e [] (Just l) = e ++ "(" ++ l ++ ")"
    long e p (Just l) = e ++ "(" ++ p ++ "," ++ l ++ ")"
    short e l = e ++ "(" ++ l ++ ")"
    mid = char '(' *> spaces *> param <* char ')' <* spaces
    
lambdaLong = char '{' *> spaces *> content <* char '}' <* spaces
  where
    inner x y = "(" ++ x ++ "){" ++ y ++ "}"
    content = inner <$> (param1 <* string "->" <* spaces) <*> statement

_____________________________________________________
module Transpiler where

import Data.List
import Text.ParserCombinators.Parsec

alpha = '_' : ['a'..'z'] ++ ['A'..'Z']
nums = ['0'..'9']
rest = alpha ++ ['0'..'9']

transpile :: String -> Either String String
transpile s = conv $ parse finalParser "" s
  where
    conv (Left _) = Left "Hugh?"
    conv (Right x) = Right x

name :: Parser String
name = (:) <$> oneOf alpha <*> (many $ oneOf rest) <* spaces

num :: Parser String
num = (string "0" <|> (:) <$> oneOf ['1'..'9'] <*> (many $ oneOf nums)) <* spaces

lit :: Parser String
lit = try name <|> try num

param :: Parser String
param = (intercalate ",") <$> sepBy expression (string "," <* spaces)

param1 :: Parser String
param1 = (intercalate ",") <$> sepBy1 expression (string "," <* spaces)

finalParser :: Parser String
finalParser = spaces *> function <* eof

expression :: Parser String
expression = try lit <|> lambda

function :: Parser String
function = try (long <$> expression <*> mid <*> optionMaybe lambda)
       <|> try (short <$> expression <*> lambda)
  where
    long e p Nothing = e ++ "(" ++ p ++ ")"
    long e [] (Just l) = e ++ "(" ++ l ++ ")"
    long e p (Just l) = e ++ "(" ++ p ++ "," ++ l ++ ")"
    short e l = e ++ "(" ++ l ++ ")"
    mid = char '(' *> spaces *> param <* char ')' <* spaces
    
lambda :: Parser String
lambda = try lambdaLong <|> try lambdaShort
    
statement :: Parser String
statement = format <$> sepBy lit spaces
  where
    format = concat . fmap (++ ";")
    
lambdaLong :: Parser String
lambdaLong = char '{' *> spaces *> content <* char '}' <* spaces
  where
    inner x y = "(" ++ x ++ "){" ++ y ++ "}"
    content = inner <$> (param1 <* string "->" <* spaces) <*> statement

lambdaShort :: Parser String
lambdaShort = char '{' *> spaces *> ((\x -> "(){" ++ x ++ "}") <$> statement) <* char '}' <* spaces
