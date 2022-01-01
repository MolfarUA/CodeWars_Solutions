{-# language FlexibleContexts #-}
module SimpleInteractiveInterpreter (input, newInterpreter) where
import qualified Data.Map as M
import Data.Fixed (mod')
import Control.Monad.State
import Text.Parsec
import Text.Parsec.Combinator

data Interpreter = Interp (M.Map Name Expr) deriving (Show)
type Result = Maybe Double
type Name = String

data Expr =
    FunDec Name [Name] Expr
  | VarDec Name Expr
  | BinOp Char Expr Expr
  | Var Name
  | Lit Double
  | App Name [Expr]
  | Pass
  deriving (Show, Eq)

isFunDec :: Expr -> Bool
isFunDec e = case e of FunDec _ _ _ -> True; _ -> False

arity :: Expr -> Int
arity e = case e of FunDec _ vargs _ -> length vargs; _ -> 0

--------------------------- parser ---------------------------

type Parser a = Parsec String Interpreter a

sp s = string s <* spaces
sp' s = string s <* space <* spaces
op s = BinOp . head <$> sp s
(<||>) p q = try p <|> q
infixr 1 <||>

pInput = spaces *> (pStatement <|> (Pass <$ eof)) <* spaces <* eof <?> "pInput"
pStatement = pFunDec <||> pExpr <?> "pStatement"
pFunDec = FunDec <$> (sp' "fn" *> pName) <*> many pName <* sp "=>" <*> pTerm <?> "pFunDec"
pExpr = pVarDec <||> pTerm <?> "pExpr"
pVarDec = VarDec <$> pName <* sp "=" <*> pExpr <?> "pVarDec"
pTerm = pFactor `chainl1` (op "+" <|> op "-") <?> "pTerm"
pFactor = pApp `chainl1` (op "*" <|> op "/" <|> op "%") <?> "pFactor"
pApp = (do
  (Interp mp) <- getState
  fname <- pName
  case M.lookup fname mp of
    Nothing -> fail ("fname not found: " ++ fname)
    Just dec -> do
      args <- count (arity dec) (pApp <* spaces)
      pure (App fname args)
  ) <||> pAtom <?> "pApp"

pAtom = pVar <|> pLit <|> (sp "(" *> spaces *> pExpr <* spaces <* sp ")" <* spaces)
pVar = Var <$> pName
pLit = Lit . read <$> ((\a b -> a ++ maybe "" id b) <$> many1 digit <*> optionMaybe ((:) <$> char '.' <*> many1 digit)) <* spaces <?> "pLit"
pName = ((:) <$> letter <*> many (alphaNum <|> char '_')) <* spaces <?> "pName"

----------------------------- eval -----------------------------

type EvalResult = Either String
type Eval = StateT Interpreter EvalResult

lookupDec :: Name -> Eval (Maybe Expr)
lookupDec name = get >>= \(Interp mp) -> pure (M.lookup name mp)

lookupVar :: Name -> Eval Expr
lookupVar name = lookupDec name >>= \mr -> case mr of
  Nothing -> lift (Left $ "variable not found: " ++ name)
  Just expr -> pure expr

eval :: Expr -> Eval Result
eval dec@(FunDec fname vargs body) = do
  (Interp mp) <- get
  mdec <- lookupDec fname
  case maybe True isFunDec mdec of
    True -> do
      put $ Interp (M.fromList (zip vargs (repeat (Lit 0))))
      mr <- eval body
      put $ Interp (M.insert fname dec mp)
      lift (Right Nothing)
    False -> do
      lift (Left $ "there exists another variable declaration of: " ++ fname)
eval dec@(VarDec name expr) = do
  (Interp mp) <- get
  mdec <- lookupDec name
  case maybe False isFunDec mdec of
    False -> do
      mr <- eval expr
      (Interp mp') <- get
      put $ Interp (M.insert name (Lit (maybe undefined id mr)) mp')
      return mr
    True -> do
      lift (Left $ "there exists another function declaration of: " ++ name)
eval (Var name) = do
  expr <- lookupVar name
  r <- eval expr
  return r
eval (Lit x) = do
  return (Just x)
eval (BinOp op ex ey) = do
  mx <- eval ex
  my <- eval ey
  let (x, y) = (maybe undefined id mx, maybe undefined id my)
  case op of
    '+' -> return (Just (x + y))
    '-' -> return (Just (x - y))
    '*' -> return (Just (x * y))
    '/' -> return (Just (x / y))
    '%' -> return (Just (x `mod'` y))
eval (App fname args) = do
  dec <- lookupVar fname
  case dec of
    (FunDec fname vargs body) -> do
      interp@(Interp mp) <- get
      case (length vargs == length args) of
        True -> do
          argvals <- forM args eval
          put $ Interp (M.union (M.fromList (zip vargs (map (Lit . maybe undefined id) argvals))) mp)
          r <- eval body
          put interp
          return r
        False -> lift . Left $ "fn call with bad argnum: " ++ fname ++ " (arity: " ++ show (length vargs) ++ ", given: " ++ show (length args) ++ ")"
    (Lit x) -> pure (Just x)
    other -> lift . Left $ "bad dec case: " ++ show other
eval Pass = return Nothing

-------------------------- exports -----------------------------

newInterpreter :: Interpreter
newInterpreter = Interp (M.empty)

input :: String -> Interpreter -> EvalResult (Result, Interpreter)
input s interp = do
  expr <- either (Left . show) Right (runParser pInput interp "input" s)
  res <- runStateT (eval expr) interp
  return res

------------------------ test helpers --------------------------

pars :: Parser a -> String -> EvalResult a
pars p s = either (Left . show) Right (runParser p newInterpreter "input" s)

t s = do
  inputs <- pars (many (satisfy (/=';')) `sepBy` sp ";") s
  r <- runStateT (forM inputs (StateT . input)) newInterpreter
  return r

t0 = "fn add x y => x + y ; add 1 2"
t1 = "fn add x y => x + y ; add 1 2 3"
t2 = "fn add x y => x + y ; add = 1; add"
t3 = ""
t4 = "4 / 2 * 3"
t5 = "x = y = 123; y"
t6 = "fn add x y => x + z"
t7 = "z = 1; fn add x y => x + z"
t8 = "fn one => 1; one"
t9 = "fn avg x y => (x + y) / 2; fn echo x => x; avg echo 4 echo 2"

___________________________________________________________________________
{-# LANGUAGE NamedFieldPuns, TupleSections #-}
module SimpleInteractiveInterpreter where

import qualified Data.Map as M
import Data.Fixed (mod')
import Text.Parsec
import Text.Parsec.Language
import Text.Parsec.Expr
import qualified Text.Parsec.Token as P
import Control.Monad.State
import Control.Monad.Trans.Except

data Value = Dbl Double
           | Fun Fn
           
data Fn = Fn [String] Expr
          
type Interpreter = M.Map String Value
  
type Result = Maybe Double

data Expr = Binop (Double -> Double -> Double) Expr Expr
          | Number Double
          | Assign String Expr
          | Var String
          | Call Fn [Expr]

data Cmd = Defn String Fn
         | Expr Expr
         
type Parser = Parsec String Interpreter

P.TokenParser { P.identifier
              , P.reserved
              , P.naturalOrFloat
              , P.symbol
              , P.whiteSpace
              } = P.makeTokenParser emptyDef

cmdp :: Parser (Maybe Cmd)
cmdp = Just <$> (Defn <$  reserved "fn" <*> identifier <*> fn)
   <|> Just <$> (Expr <$> expr)
   <|> pure Nothing

fn :: Parser Fn
fn = do
  formals <- many identifier
  symbol "=>"
  setState . M.fromList $ map (, Dbl undefined) formals
  Fn formals <$> expr

expr :: Parser Expr
expr = buildExpressionParser table term

table = [ [ binary "*" (*), binary "/" (/), binary "%" mod' ]
        , [ binary "+" (+), binary "-" (-) ]
        ]

binary name fn = Infix (Binop fn <$ symbol name) AssocLeft

term :: Parser Expr
term = Number . either fromIntegral id <$> naturalOrFloat
   <|> ident
   <|> symbol "(" *> expr <* symbol ")"

ident :: Parser Expr
ident = do
  name <- identifier
  def <- M.lookup name <$> getState
  rhs <- optionMaybe (symbol "=" *> expr)
  case (def, rhs) of
    (Nothing, Nothing) -> fail $ name ++ " is not defined"
    (Just (Fun _), Just _) -> fail $ name ++ " is not a variable"
    (_, Just rhs) -> return $ Assign name rhs
    (Just (Fun fn@(Fn formals _)), Nothing) -> Call fn <$> count (length formals) expr
    (Just (Dbl _), Nothing) -> return $ Var name

newInterpreter :: Interpreter
newInterpreter = M.empty

input :: String -> Interpreter -> Either String (Result, Interpreter)
input s i = runExcept $ runStateT st i where
  st = do
    cmd <- lift . withExcept show . except $ runParser (whiteSpace *> cmdp <* eof) i "" s
    maybe (pure Nothing) exec cmd

exec :: Cmd -> StateT Interpreter (Except String) Result
exec (Defn name fn) = do
  def <- gets $ M.lookup name
  case def of
    Just (Dbl _) -> lift . throwE $ "cannot define function over variable " ++ name
    _ -> do
      modify $ M.insert name (Fun fn)
      pure Nothing
exec (Expr e) = Just <$> eval e

eval :: Expr -> StateT Interpreter (Except String) Double
eval (Number n) = return n
eval (Binop f el er) = f <$> eval el <*> eval er
eval (Var name) = do
  def <- gets $ M.lookup name
  case def of
    Just (Dbl d) -> return d
    _ -> lift . throwE $ name ++ " is not a variable"
eval (Assign name e) = do
  d <- eval e
  def <- gets $ M.lookup name
  case def of
    Just (Fun _) -> lift . throwE $ name ++ " is not a variable"
    _ -> modify $ M.insert name (Dbl d)
  return d
eval (Call (Fn formals body) actuals) = do
  env <- M.fromList . zip formals <$> mapM (fmap Dbl . eval) actuals
  withStateT (const env) $ eval body

___________________________________________________________________________
module SimpleInteractiveInterpreter where

import           Control.Applicative          (Alternative ((<|>)))
import           Control.Monad                (foldM)
import           Data.Char                    (isAlpha, isAlphaNum, isDigit)
import           Data.Either                  (isRight)
import           Data.Fixed                   (mod')
import           Data.Foldable                (find)
import qualified Data.Map.Strict              as Map
import           Data.Maybe                   (fromMaybe)
import           Data.Text                    (pack, strip, unpack)
import           Text.ParserCombinators.ReadP (ReadP, chainl1, char, choice, eof, munch, munch1,
                                               option, readP_to_S, satisfy, sepBy, skipSpaces,
                                               string)

type Interpreter = Map.Map String Binding
type Result = Maybe Double

data Binding = Variable Double | Fn [String] Expr

newInterpreter :: Interpreter
newInterpreter = Map.empty

input :: String -> Interpreter -> Either String (Result, Interpreter)
-- input s i = undefined
input s i = fromMaybe (Left "Bad input") (find isRight results)
  where trim = unpack . strip . pack
        parses = readP_to_S parse (trim s)
        results = map (eval i . fst) (filter (null . snd) parses)

eval :: Interpreter -> Input -> Either String (Result, Interpreter)
eval i Blank         = Right (Nothing, i)
eval i (FnInput f)   = evalFn i f
eval i (ExprInput e) = evalExpr i e

evalFn :: Interpreter -> Function -> Either String (Result, Interpreter)
evalFn i (Function name params expr) =
  let nameValid = case Map.lookup name i of
        Just (Variable _) -> Left $ "variable with name " ++ name ++ " already exists"
        _                 -> Right ()
      i' = Map.fromList (zip params (repeat (Variable 1)))
      paramsValid = evalExpr i' expr
   in nameValid >> paramsValid >> Right (Nothing, Map.insert name (Fn params expr) i)

evalExpr :: Interpreter -> Expr -> Either String (Result, Interpreter)
evalExpr i (Literal n) = Right (Just n, i)
evalExpr i (Identifier s) = case Map.lookup s i of
  Just (Variable n) -> Right (Just n, i)
  Just (Fn _ _)     -> Left "its a function, not a var"
  _                 -> Left $ "undefined variable " ++ s
evalExpr i (Nested e) = evalExpr i e
evalExpr i (Assignment s e) = do
  _ <- case Map.lookup s i of
        Just (Fn _ _) -> Left $ "function with name " ++ s ++ " already exists"
        _             -> Right ()
  (v, i') <- evalExpr i e
  case v of
    Just n -> return (v, Map.insert s (Variable n) i')
    _      -> Left "bad expression"
evalExpr int (FnCall fn es) = applyFn validate
  where
    validate = case Map.lookup fn int of
      Just f@(Fn ps _) -> if length es == length ps then Just f else Nothing
      _                -> Nothing
    combine i (s, e) = case evalExpr int e of
      Right (Just r, _) -> Just $ Map.insert s (Variable r) i
      _                 -> Nothing
    applyFn (Just (Fn ps e)) = maybe (Left "applyFn failed") (`evalExpr` e) int'
      where int' = foldM combine newInterpreter (zip ps es)
    applyFn _ = Left "not a function"
evalExpr i (Binary o l r) = do
  (l', i') <- evalExpr i l
  (r', i'') <- evalExpr i' r
  return (o <$> l' <*> r', i'')

data Input = ExprInput Expr | FnInput Function | Blank

data Function = Function String [String] Expr

data Expr
  = Literal Double
  | Identifier String
  | Nested Expr
  | Assignment String Expr
  | FnCall String [Expr]
  | Binary (Double -> Double -> Double) Expr Expr

parse :: ReadP Input
parse = (ExprInput <$> expr <|> FnInput <$> fn <|> Blank <$ skipSpaces) <* eof

fn :: ReadP Function
fn = Function <$ string "fn" <* skipSpaces <*> name <*> sepBy name skipSpaces <* string "=>" <* skipSpaces <*> expr

expr :: ReadP Expr
expr = term `chainl1` op
  where op = choice $ map mkOp [('+', (+)), ('-', (-))]

term :: ReadP Expr
term = factor `chainl1` op
  where op = choice $ map mkOp [('*', (*)), ('/', (/)), ('%', mod')]

factor :: ReadP Expr
factor = Nested <$ char '(' <* skipSpaces <*> expr <* char ')' <* skipSpaces
  <|> Literal <$> number
  <|> Identifier <$> name
  <|> Assignment <$> name <* char '=' <* skipSpaces <*> expr
  <|> FnCall <$> name <*> sepBy expr skipSpaces

mkOp :: (Char, Double -> Double -> Double) -> ReadP (Expr -> Expr -> Expr)
mkOp (c, o) = Binary o <$ char c <* skipSpaces

name :: ReadP String
name = (:) <$> (satisfy isAlpha <|> char '_') <*> munch (\c -> isAlphaNum c || c == '_') <* skipSpaces

number :: ReadP Double
number = read <$> ((++) <$> munch1 isDigit <*> option "" ((:) <$> char '.' <*> munch1 isDigit)) <* skipSpaces


___________________________________________________________________________
module SimpleInteractiveInterpreter where

import Data.Map (Map)
import qualified Data.Map as Map
import Data.Fixed (mod')
import Data.Maybe (fromJust)

data Token
  = FN | FNOP | LP | RP | OPE
  | OPA Char
  | OPM Char
  | ID String
  | NUM Double
  deriving (Eq, Show)
  
isId :: Token -> Bool
isId (ID _) = True
isID _      = False

letters = ['a'..'z'] ++ ['A'..'Z']
digits = ['0'..'9']
idstart = '_':letters
idchars = idstart ++ digits
numstart = '.':digits

scan :: String -> Either String [Token]
scan []           = Right []
scan ('f':'n':cs) = fmap (FN:)   $ scan cs
scan ('=':'>':cs) = fmap (FNOP:) $ scan cs
scan ('(':cs)     = fmap (LP:)   $ scan cs
scan (')':cs)     = fmap (RP:)   $ scan cs
scan ('=':cs)     = fmap (OPE:)  $ scan cs
scan s@(c:cs)
  | c `elem` " \t\n"  = scan cs
  | c `elem` "+-"     = fmap (OPA c:) $ scan cs
  | c `elem` "*/%"    = fmap (OPM c:) $ scan cs
  | c `elem` idstart  = scanId s
  | c `elem` numstart = scanNum s
  | otherwise         = Left $ "Scan error starting with '" ++ [c] ++ "'"
        
scanId :: String -> Either String [Token]
scanId s = fmap (ID name:) $ scan cs
  where (name, cs) = span (`elem` idchars) s
  
scanNum :: String -> Either String [Token]
scanNum s
  | last numst == '.' = Left "Scan error: number ends with ."
  | otherwise         = fmap (NUM (read ('0':numst)) :) $ scan cs
  where
    (prefix, afterpre) = span (`elem` digits) s
    (suffix,cs) = case afterpre of
      ('.':afterdot) -> let (fractional, cs) = span (`elem` digits) afterdot in ('.':fractional, cs)
      cs -> ("", cs)
    numst = prefix ++ suffix

data Exp
  = Asn String Exp
  | Oper (Double->Double->Double) Exp Exp
  | Literal Double
  | Var String
  | Funcall String [Exp]
  
getOper :: Char -> (Double -> Double -> Double)
getOper '+' = (+)
getOper '-' = (-)
getOper '*' = (*)
getOper '/' = (/)
getOper '%' = mod'

type Func = ([String], Exp)

type Ftable = Map String Func
type Vtable = Map String Double
type Interpreter = (Ftable, Vtable)

type Result = Maybe Double

type Arities = Map String Int
arities :: Ftable -> Arities
arities = Map.map (length . fst) 

newInterpreter :: Interpreter
newInterpreter = (Map.empty, Map.empty)

input :: String -> Interpreter -> Either String (Result, Interpreter)
input line state = scan line >>= parse state

parse :: Interpreter -> [Token] -> Either String (Result, Interpreter)
parse state [] = Right (Nothing, state)
parse (funs, vars) (FN : ID fname : rest)
  = if Map.member fname vars
    then Left $ "Can't reuse variable name '" ++ fname ++ "' for function"
    else (\func -> (Nothing, (Map.insert fname func funs, vars)))
           <$> parseFunc fname (arities funs) rest
parse (funs, vars) toks = finish <$> (parseExp (arities funs) toks >>= evalExp funs vars)
  where
    finish :: (Vtable, Double) -> (Result, Interpreter)
    finish (vars', x) = (Just x, (funs, vars'))

{- top-down grammar
exp -> ID OPE exp | sum
sum -> term stail
stail -> OPA term stail | e
term -> factor ttail
ttail -> OPM factor ttail | e
factor -> NUM | ID {exp} | LP exp RP
-}

parseExp :: Arities -> [Token] -> Either String Exp
parseExp fnarity ts = exp ts >>= finish
  where
    finish :: ([Token], Exp) -> Either String Exp
    finish ([],  e) = Right e
    finish (t:_, _) = Left $ "Parse error: extra tokens starting with " ++ show t
    
    exp :: [Token] -> Either String ([Token], Exp)
    exp (ID vname : OPE : ts) =
      if Map.member vname fnarity
      then Left $ "Can't use function name '" ++ vname ++ "' as a variable"
      else fmap (fmap $ Asn vname) (exp ts)
    exp ts = sum ts
    
    sum :: [Token] -> Either String ([Token], Exp)
    sum ts = term ts >>= stail
    
    stail :: ([Token], Exp) -> Either String ([Token], Exp)
    stail (OPA op : ts, lhs) = term ts >>= stail . fmap (Oper (getOper op) lhs)
    stail x = Right x
    
    term :: [Token] -> Either String ([Token], Exp)
    term ts = factor ts >>= ttail
    
    ttail :: ([Token], Exp) -> Either String ([Token], Exp)
    ttail (OPM op : ts, lhs) = factor ts >>= ttail . fmap (Oper (getOper op) lhs)
    ttail x = Right x
    
    factor :: [Token] -> Either String ([Token], Exp)
    factor (NUM x : ts) = Right (ts, Literal x)
    factor (LP : ts) = exp ts >>= checkRp
    factor (ID name : ts)
      = case Map.lookup name fnarity of
          Nothing    -> Right (ts, Var name)
          Just nargs -> fmap (Funcall name) <$> getArgs nargs ts
    factor ts = Left $ "Parse error: expected factor, saw " ++ show (take 3 ts)
    
    getArgs :: Int -> [Token] -> Either String ([Token], [Exp])
    getArgs 0 ts = Right (ts, [])
    getArgs n ts = exp ts >>= (\(ts', arg) -> fmap (arg:) <$> getArgs (pred n) ts')
    
checkRp :: ([Token], Exp) -> Either String ([Token], Exp)
checkRp (RP:ts, e) = Right (ts, e)
checkRp _ = Left "Parse error: missing right paren"

evalExp :: Ftable -> Vtable -> Exp -> Either String (Vtable, Double)
evalExp funs = ev
  where
    ev :: Vtable -> Exp -> Either String (Vtable, Double)
    ev vars (Asn name rhs) = (\(vars', x) -> (Map.insert name x vars', x)) <$> ev vars rhs
    ev vars (Oper f lhs rhs) = ev vars lhs >>= (\(vars',x) -> fmap (f x) <$> ev vars' rhs)
    ev vars (Literal x) = Right (vars, x)
    ev vars (Var name) = case Map.lookup name vars of
                           Just x  -> Right (vars, x)
                           Nothing -> Left $ "Undefined variable '" ++ name ++ "'"
    ev vars (Funcall fname args) = evSeq vars args >>= apply
      where 
        (params, body) = fromJust $ Map.lookup fname funs
        apply :: (Vtable, [Double]) -> Either String (Vtable, Double)
        apply (vars', xs) = (((,) vars') . snd) <$> evalExp funs (Map.fromList $ zip params xs) body
    
    evSeq :: Vtable -> [Exp] -> Either String (Vtable, [Double])
    evSeq vars [] = Right (vars, [])
    evSeq vars (exp:exps) = ev vars exp >>= (\(vars', x) -> fmap (x:) <$> evSeq vars' exps)

parseFunc :: String -> Arities -> [Token] -> Either String Func
parseFunc fname fnarity toks = getParams toks >>= parseFunc'
  where
    parseFunc' :: ([String], [Token]) -> Either String Func
    parseFunc' (params, ts) = parseExp (Map.insert fname (length params) fnarity) ts
                              >>= checkParams params

checkParams :: [String] -> Exp -> Either String Func
checkParams params exp
  = case filter (not . (`elem` params)) (allVars exp) of
      []       -> Right (params, exp)
      (name:_) -> Left $ "Invalid identifier '" ++ name ++ "' in function body."

allVars :: Exp -> [String]
allVars (Asn name exp)   = name : allVars exp
allVars (Oper _ lhs rhs) = allVars lhs ++ allVars rhs
allVars (Literal _)      = []
allVars (Var name)       = [name]
allVars (Funcall _ exps) = foldl (++) [] $ fmap allVars exps

getParams :: [Token] -> Either String ([String], [Token])
getParams [] = Left "Parse error: missing => in function def"
getParams (ID name : ts) = fmap (\(ps, ts') -> (name:ps, ts')) $ getParams ts
getParams (FNOP:ts) = Right ([], ts)
getParams (t:_) = Left $ "Parse error: unexpected token '" ++ show t ++ "' in parameter list"


___________________________________________________________________________
module SimpleInteractiveInterpreter where

import           Control.Monad                  ( guard )
import           Data.List                      ( nub )
import qualified Data.Map                      as M
import           Data.Maybe                     ( fromJust
                                                , isJust
                                                , isNothing
                                                )
import           Text.Parsec                    ( (<|>)
                                                , ParseError
                                                , char
                                                , choice
                                                , digit
                                                , eof
                                                , letter
                                                , many
                                                , many1
                                                , oneOf
                                                , parse
                                                , string
                                                , try
                                                )
import           Text.Parsec.String             ( Parser )

data Interpreter = Interpreter
    { getFunctions :: Functions
    , getVariables :: Variables
    }
    deriving Eq

data InputRow = IExpression Expression
              | IFunction Function
              deriving Show

type Result = Maybe Double

type VariableName = Identifier
type FunctionName = Identifier
type VariableValue = Double

type Variables = M.Map VariableName Double
type Functions = M.Map FunctionName Function

type Whitespaces = String

data Operator = Eq | Add | Sub | Mul | Div | Mod | Const deriving (Eq, Ord)
newtype Number = Number Double deriving (Eq, Ord)
newtype Identifier = Identifier String deriving (Eq, Ord)

data SyntaxError = MismatchedParens
                 | InvalidOperator Operator
                 | InvalidToken Token
                 deriving Eq

data Error = InvalidInputError String
           | SyntaxError SyntaxError
           | InvalidExpressionError Expression
           | UnknownIdentifierError VariableName
           | VariableNotFoundInHeaderError VariableName
           | VariableNameConflictError VariableName
           | FunctionNameConflictError FunctionName
           | UnknownError Expression
           deriving Eq

type Expression = [Token]
type PostfixExpression = Expression

data Function = Function
    { functionName :: FunctionName
    , functionArgs :: [Identifier]
    , functionBody :: Expression
    }
    deriving (Eq, Show)

data Token = TOpenParen
            | TCloseParen
            | TNumber Number
            | TIdentifier Identifier
            | TOperator Operator
            deriving (Eq, Ord)

instance Show Interpreter where
    show (Interpreter fs vs) = concat ["Functions: ", show fs, "\nVariables: ", show vs]

instance Show Number where
    show (Number n) = show n

instance Show Identifier where
    show (Identifier i) = i

instance Show Operator where
    show Eq    = "="
    show Add   = "+"
    show Sub   = "-"
    show Mul   = "*"
    show Div   = "/"
    show Mod   = "%"
    show Const = "~"

instance Show Token where
    show TOpenParen      = "("
    show TCloseParen     = ")"
    show (TNumber     n) = show n
    show (TIdentifier i) = show i
    show (TOperator   o) = show o

instance Show SyntaxError where
    show MismatchedParens    = "SyntaxError: Mismatched parentheses"
    show (InvalidOperator o) = concat ["SyntaxError: Invalid operator '", show o, "'"]
    show (InvalidToken    t) = concat ["SyntaxError: Invalid token '", show t, "'"]

instance Show Error where
    show (InvalidInputError             s ) = concat ["InvalidInputError: '", s, "'"]
    show (SyntaxError                   se) = show se
    show (InvalidExpressionError        e ) = concat ["InvalidExpressionError: Invalid expression '", show e, "'"]
    show (UnknownIdentifierError        v ) = concat ["UnknownIdentifierError: Unknown identifier '", show v, "'"]
    show (VariableNotFoundInHeaderError v ) = concat
        [ "VariableNotFoundInHeaderError: Invalid identifier. No variable with name '"
        , show v
        , "' was found in function header"
        ]
    show (VariableNameConflictError v) =
        concat ["VariableNameConflictError: Function with the same name '", show v, "' already exists"]
    show (FunctionNameConflictError v) =
        concat ["FunctionNameConflictError: Variable with the same name '", show v, "' already exists"]
    show (UnknownError e) = concat ["UnknownError: Unknown error in expression '", show e, "'"]

newInterpreter :: Interpreter
newInterpreter = Interpreter M.empty M.empty

input :: String -> Interpreter -> Either String (Result, Interpreter)
input s i = case parseInterpreter s of
    Right r ->
        let ev = eval i r
        in  case ev of
                Right res -> Right res
                Left  err -> Left $ show err
    Left err -> Left $ show (InvalidInputError s)

parseInterpreter :: String -> Either ParseError InputRow
parseInterpreter = parse pInputRow ""

eval :: Interpreter -> InputRow -> Either Error (Result, Interpreter)
eval i@(Interpreter fs vs) (IFunction f) = do
    checkErrorsFunction i f
    convertExpressionToPostfix fs vs (functionBody f)
    return (Nothing, saveFunction i f)
eval i@(Interpreter fs vs) (IExpression e) = do
    checkErrorsExpression i e
    pe <- convertExpressionToPostfix fs vs e
    let as = getAssignmentsFromInfix e
    res <- evalExpression i as pe
    vs' <- getNewVariables fs vs as pe
    return (res, Interpreter fs (M.union vs' vs))

evalExpression :: Interpreter -> [Identifier] -> PostfixExpression -> Either Error Result
evalExpression (Interpreter fs vs) as e = evalPostfix fs vs as e []

checkErrorsFunction :: Interpreter -> Function -> Either Error ()
checkErrorsFunction (Interpreter fs vs) f@(Function fn is e) = getErrors checks
    where checks = [checkFunctionNameConflict vs fn, checkVariableNotFoundInHeader fs f]

checkErrorsExpression :: Interpreter -> Expression -> Either Error ()
checkErrorsExpression (Interpreter fs vs) e = getErrors checks
    where checks = [checkVariableNameConflict fs e, checkUnknownIdentifier fs vs e]

getMissingIdentifier :: [Identifier] -> [Identifier] -> Maybe Identifier
getMissingIdentifier is []       = Nothing
getMissingIdentifier is (v : vs) = if v `notElem` is then Just v else getMissingIdentifier is vs

getOddIdentifier :: [Identifier] -> [Identifier] -> Maybe Identifier
getOddIdentifier is []       = Nothing
getOddIdentifier is (v : vs) = if v `elem` is then Just v else getOddIdentifier is vs

checkFunctionNameConflict :: Variables -> FunctionName -> Maybe Error
checkFunctionNameConflict vs fn = FunctionNameConflictError <$> getOddIdentifier xs ys
  where
    xs = M.keys vs
    ys = [fn]

checkVariableNameConflict :: Functions -> Expression -> Maybe Error
checkVariableNameConflict fs e = VariableNameConflictError <$> getOddIdentifier xs ys
  where
    xs = getAssignmentsFromInfix e
    ys = M.keys fs

checkVariableNotFoundInHeader :: Functions -> Function -> Maybe Error
checkVariableNotFoundInHeader fs (Function fn is e) = VariableNotFoundInHeaderError <$> getMissingIdentifier xs ys
  where
    xs = is
    ys = getExtrasFromExpression (M.keys fs) e

checkUnknownIdentifier :: Functions -> Variables -> Expression -> Maybe Error
checkUnknownIdentifier fs vs e = UnknownIdentifierError <$> getMissingIdentifier xs ys
  where
    as = getAssignmentsFromInfix e
    xs = M.keys fs ++ M.keys vs ++ as
    ys = filterIdentifiers e

getErrors :: [Maybe Error] -> Either Error ()
getErrors checks | all isNothing checks = Right ()
                 | otherwise            = Left $ fromJust $ head $ filter isJust checks

saveFunction :: Interpreter -> Function -> Interpreter
saveFunction (Interpreter fs vs) f = Interpreter fs' vs where fs' = M.insert (functionName f) f fs

filterIdentifiers :: Expression -> [Identifier]
filterIdentifiers []                   = []
filterIdentifiers (TIdentifier i : ts) = i : filterIdentifiers ts
filterIdentifiers (t             : ts) = filterIdentifiers ts

getAssignmentsFromInfix :: Expression -> [Identifier]
getAssignmentsFromInfix [] = []
getAssignmentsFromInfix (TIdentifier i : TOperator Eq : ts) = i : getAssignmentsFromInfix ts
getAssignmentsFromInfix (t : ts) = getAssignmentsFromInfix ts

getNewVariables :: Functions -> Variables -> [Identifier] -> PostfixExpression -> Either Error Variables
getNewVariables fs vs as pe = saveVariablesPostfix fs vs as pe [] M.empty

getExtrasFromExpression :: [Identifier] -> Expression -> [Identifier]
getExtrasFromExpression is []       = []
getExtrasFromExpression is (TIdentifier i : ts) | i `notElem` is = i : getExtrasFromExpression is ts
getExtrasFromExpression is (t : ts) = getExtrasFromExpression is ts

convertExpressionToPostfix :: Functions -> Variables -> Expression -> Either Error PostfixExpression
convertExpressionToPostfix fs vs e = substituteFunctions fs vs e [] >>= toPostfix fs vs [] []

applyOperator :: Operator -> Double -> Double -> Double
applyOperator Eq    = const
applyOperator Add   = (+)
applyOperator Sub   = flip (-)
applyOperator Mul   = (*)
applyOperator Div   = flip (/)
applyOperator Mod   = \a b -> fromIntegral $ round b `mod` round a
applyOperator Const = const

evalPostfix :: Functions -> Variables -> [Identifier] -> PostfixExpression -> [Double] -> Either Error Result
evalPostfix fs vs as []                        []                 = Right Nothing
evalPostfix fs vs as []                        [v]                = Right $ Just v
evalPostfix fs vs as []                        st                 = Left $ InvalidExpressionError []
evalPostfix fs vs as (TNumber (Number n) : ts) st                 = evalPostfix fs vs as ts (n : st)
evalPostfix fs vs as (TIdentifier i : ts) st | i `elem` as        = evalPostfix fs vs as ts st
evalPostfix fs vs as pe@(TIdentifier i : ts) st | i `M.member` vs = case M.lookup i vs of
    Just v  -> evalPostfix fs vs as ts (v : st)
    Nothing -> Left $ InvalidExpressionError pe
evalPostfix fs vs as (TIdentifier i  : ts) st             = evalPostfix fs vs as ts st
evalPostfix fs vs as (TOperator   Eq : ts) st             = evalPostfix fs vs as ts st
evalPostfix fs vs as (TOperator   o  : ts) (v1 : v2 : st) = evalPostfix fs vs as ts (applyOperator o v1 v2 : st)
evalPostfix fs vs as ts                    st             = Left $ InvalidExpressionError ts

saveVariablesPostfix :: Functions
                     -> Variables
                     -> [Identifier]
                     -> PostfixExpression
                     -> PostfixExpression
                     -> Variables
                     -> Either Error Variables
saveVariablesPostfix fs vs as [] []  xs = Right xs
saveVariablesPostfix fs vs as [] [v] xs = Right xs
saveVariablesPostfix fs vs as [] ts  xs = Left $ InvalidExpressionError []
saveVariablesPostfix fs vs as (TNumber (Number n) : ts) st xs =
    saveVariablesPostfix fs vs as ts (TNumber (Number n) : st) xs
saveVariablesPostfix fs vs as (TIdentifier i : ts) st xs = if i `M.member` vs && i `notElem` as
    then saveVariablesPostfix fs vs as ts (TNumber (Number (vs M.! i)) : st) xs
    else saveVariablesPostfix fs vs as ts (TIdentifier i : st) xs
saveVariablesPostfix fs vs as (TOperator Eq : ts) (v1 : (TIdentifier i) : st) xs = case getNumberFromIdentifier v1 of
    Right v   -> saveVariablesPostfix fs vs as ts (v1 : st) (M.insert i v xs)
    Left  err -> Left err
saveVariablesPostfix fs vs as ts'@(TOperator Eq : ts) st             xs = Left $ InvalidExpressionError ts'
saveVariablesPostfix fs vs as (    TOperator o  : ts) (v1 : v2 : st) xs = do
    v1' <- getNumberFromIdentifier v1
    v2' <- getNumberFromIdentifier v2
    saveVariablesPostfix fs vs as ts (TNumber (Number $ applyOperator o v1' v2') : st) xs
saveVariablesPostfix fs vs as ts st xs = Left $ InvalidExpressionError ts

getNumberFromIdentifier :: Token -> Either Error Double
getNumberFromIdentifier i = case i of
    TNumber (Number n) -> Right n
    v                  -> Left $ SyntaxError $ InvalidToken v

toPostfix :: Functions -> Variables -> Expression -> Expression -> Expression -> Either Error PostfixExpression
toPostfix fs vs out stack []                           = Right $ reverse out ++ stack
toPostfix fs vs out stack (    t@(TNumber     n) : ts) = toPostfix fs vs (t : out) stack ts
toPostfix fs vs out stack ts'@(t@(TIdentifier i) : ts) = case i of
    i | i `M.member` fs -> Left $ UnknownError ts'
    i                   -> toPostfix fs vs (t : out) stack ts
toPostfix fs vs out stack (t@(TOperator op) : ts) = toPostfix fs vs out' stack' ts
    where (out', stack') = handleOperator out stack op
toPostfix fs vs out stack (TOpenParen  : ts) = toPostfix fs vs out (TOpenParen : stack) ts
toPostfix fs vs out stack (TCloseParen : ts) = case handleCloseParen out stack of
    Right (out', stack') -> toPostfix fs vs out' stack' ts
    Left  err            -> Left err

substituteFunctions :: Functions -> Variables -> Expression -> Expression -> Either Error Expression
substituteFunctions fs vs [] out = if hasFunctions fs vs out' then substituteFunctions fs vs out' [] else Right out'
    where out' = reverse out
substituteFunctions fs vs e@(TIdentifier i : ts) out | i `M.member` fs =
    let parsedArgs = getFunctionArgs fs vs i ts
    in  case parsedArgs of
            Right Nothing             -> Left $ UnknownError e
            Right (Just (args, rest)) -> case substituteFunction fs vs i args of
                Right f   -> substituteFunctions fs vs rest (reverse (encloseWithParens f) ++ out)
                Left  err -> Left err
            Left err -> Left err
substituteFunctions fs vs (t : ts) out = substituteFunctions fs vs ts (t : out)

substituteFunction :: Functions -> Variables -> Identifier -> [Expression] -> Either Error Expression
substituteFunction fs vs fn args = case fn `M.lookup` fs of
    Just f ->
        let body    = functionBody f
            argsMap = zip (TIdentifier <$> functionArgs f) args
        in  Right $ foldl (\acc (tn, as) -> replaceTokens tn as acc []) body argsMap
    Nothing -> Left $ UnknownIdentifierError fn

hasFunctions :: Functions -> Variables -> Expression -> Bool
hasFunctions fs vs []       = False
hasFunctions fs vs (TIdentifier i : ts) | i `M.member` fs = True
hasFunctions fs vs (_ : ts) = hasFunctions fs vs ts

encloseWithParens :: Expression -> Expression
encloseWithParens ts = [TOpenParen] ++ ts ++ [TCloseParen]

replaceTokens :: Token -> Expression -> Expression -> Expression -> Expression
replaceTokens tn rs [] out                 = reverse out
replaceTokens tn rs (t : ts) out | t == tn = replaceTokens tn rs ts (reverse (encloseWithParens rs) ++ out)
replaceTokens tn rs (t : ts) out           = replaceTokens tn rs ts (t : out)

getFunctionArgs :: Functions -> Variables -> Identifier -> Expression -> Either Error (Maybe ([Expression], Expression))
getFunctionArgs fs vs fn ts = do
    ar <- getArity fs fn
    getFunctionArgs' fs vs ar ts [] []

getFunctionArgs' :: Functions
                 -> Variables
                 -> Int
                 -> Expression
                 -> Expression
                 -> [Expression]
                 -> Either Error (Maybe ([Expression], Expression))
getFunctionArgs' fs vs 0 ts st acc = Right $ Just (reverse acc, ts)
getFunctionArgs' fs vs ar ts st acc | isValidExpression fs vs st == Right True =
    getFunctionArgs' fs vs (ar - 1) ts [] (st : acc)
getFunctionArgs' fs vs ar (t : ts) st acc = getFunctionArgs' fs vs ar ts (st ++ [t]) acc
getFunctionArgs' fs vs ar []       st acc = Right Nothing

getArity :: Functions -> Identifier -> Either Error Int
getArity fs fn = case fn `M.lookup` fs of
    Nothing -> Left $ UnknownIdentifierError fn
    Just f  -> Right $ length $ functionArgs f

isValidExpression :: Functions -> Variables -> Expression -> Either Error Bool
isValidExpression fs vs []                                     = Right False
isValidExpression fs vs [TNumber _]                            = Right True
isValidExpression fs vs [TIdentifier i] | i `M.member` vs      = Right True
isValidExpression fs vs [TIdentifier i] | i `M.member` fs      = Right False
isValidExpression fs vs (TIdentifier i : ts) | i `M.member` fs = do
    parsedArgs <- getFunctionArgs fs vs i ts
    return $ case parsedArgs of
        Nothing -> False
        Just (args, rest) ->
            let noTail       = null rest
                completeArgs = allRight (== True) (isValidExpression fs vs <$> args)
            in  noTail && completeArgs
isValidExpression fs vs (TNumber n : TOperator _ : ts')                       = isValidExpression fs vs ts'
isValidExpression fs vs (TNumber n : _) = Left $ SyntaxError (InvalidToken (TNumber n))
isValidExpression fs vs (TIdentifier i : TOperator _ : ts') | i `M.member` vs = isValidExpression fs vs ts'
isValidExpression fs vs (   TIdentifier i : TOperator Eq : ts')               = isValidExpression fs vs ts'
isValidExpression fs vs (TIdentifier i : _) = Left $ SyntaxError (InvalidToken (TIdentifier i))
isValidExpression fs vs [   TOpenParen                        ]               = Right False
isValidExpression fs vs ts@(TOpenParen : ts'                  )               = do
    b <- isValidExpression fs vs (init ts')
    return $ last ts == TCloseParen && b
isValidExpression fs vs (TCloseParen : _) = Left $ SyntaxError MismatchedParens
isValidExpression fs vs (TOperator o : _) = Left $ SyntaxError (InvalidOperator o)

allRight :: (t -> Bool) -> [Either a t] -> Bool
allRight f []             = True
allRight f (Right x : xs) = f x && allRight f xs
allRight f (Left  x : xs) = False

handleOperator :: Expression -> Expression -> Operator -> (Expression, Expression)
handleOperator out []       op = (out, [TOperator op])
handleOperator out (t : ts) op = case t of
    TOperator o | o >= op && op /= Eq -> handleOperator (t : out) ts op
    _ -> (out, TOperator op : t : ts)

handleCloseParen :: Expression -> Expression -> Either Error (Expression, Expression)
handleCloseParen out []                = Left $ SyntaxError MismatchedParens
handleCloseParen out (TOpenParen : ts) = Right (out, ts)
handleCloseParen out (t          : ts) = handleCloseParen (t : out) ts

pWhitespaces :: Parser Whitespaces
pWhitespaces = many $ oneOf " \n\t"

pLexeme :: Parser a -> Parser a
pLexeme p = do
    pWhitespaces
    x <- p
    pWhitespaces
    return x

pNumber :: Parser Number
pNumber = do
    n <-
        choice
        $   try
        .   pLexeme
        <$> [ do
                d1 <- many1 digit
                char '.'
                d2 <- many1 digit
                return $ d1 ++ "." ++ d2
            , many1 digit
            ]
    return $ Number $ read n

pIdentifier :: Parser Identifier
pIdentifier = do
    hd <- letter <|> char '_'
    tl <- many (letter <|> digit <|> char '_')
    let s = hd : tl
    guard $ s /= "fn"
    return $ Identifier $ hd : tl

pOperator :: Parser Operator
pOperator = do
    o <- pLexeme $ oneOf "=+-*/%"
    case o of
        '+' -> return Add
        '-' -> return Sub
        '*' -> return Mul
        '/' -> return Div
        '%' -> return Mod
        '=' -> return Eq
        _   -> return Const

pTokens :: Parser Expression
pTokens = do
    cs <- many
        (   choice
        $   try
        .   pLexeme
        <$> [ char '(' >> return TOpenParen
            , char ')' >> return TCloseParen
            , TNumber <$> pLexeme pNumber
            , TOperator <$> pLexeme pOperator
            , TIdentifier <$> pLexeme pIdentifier
            ]
        )
    eof
    return cs

pExpression :: Parser Expression
pExpression = pTokens

pFunction :: Parser Function
pFunction = do
    pLexeme $ string "fn"
    fn   <- pLexeme pIdentifier
    args <- many $ pLexeme pIdentifier
    pLexeme $ string "=>"
    e <- pLexeme pExpression
    guard $ args == nub args
    return $ Function fn args e

pInputRow :: Parser InputRow
pInputRow = do
    r <- choice $ try . pLexeme <$> [IFunction <$> pFunction, IExpression <$> pExpression]
    eof
    return r

interpreterIteration :: Interpreter -> IO ()
interpreterIteration i = do
    putStr "> "
    s <- getLine
    let res = input s i
    case res of
        Right res'@(r, i') -> do
            putStrLn $ concat [show r, "\n", show i']
            interpreterIteration i'
        Left err -> do
            print err
            interpreterIteration i

main :: IO ()
main = do
    interpreterIteration newInterpreter
