module EvaluateMathematicalExpression (calc) where

import Data.Either
import Text.Parsec.Expr
import Text.Parsec.Language (emptyDef)
import qualified Text.Parsec.Token as P
import Text.ParserCombinators.Parsec

lexer          = P.makeTokenParser emptyDef
naturalOrFloat = P.naturalOrFloat lexer
parens         = P.parens lexer
symbol         = P.symbol lexer
whiteSpace     = P.whiteSpace lexer

ops =
  [ [Prefix ((negate <$ symbol "-") `chainr1` pure (.))]
  , [Infix ((*) <$ symbol "*") AssocLeft, Infix ((/) <$ symbol "/") AssocLeft]
  , [Infix ((+) <$ symbol "+") AssocLeft, Infix ((-) <$ symbol "-") AssocLeft]
  ]

expr = buildExpressionParser ops term
term = parens expr <|> either fromInteger id <$> naturalOrFloat

calc = fromRight (error "parse error") . parse (whiteSpace *> expr <* eof) ""
____________________________________________
module EvaluateMathematicalExpression (calc) where

import Text.ParserCombinators.ReadP (ReadP,readP_to_S,skipSpaces,eof,(+++),chainl1,munch1,char,between)

calc :: String -> Double
calc xs | [(r,"")] <- readP_to_S (skipSpaces *> expr <* eof) xs = r

expr,unit,number :: ReadP Double
expr = unit `chainl1` (op (*) '*' +++ op (/) '/') `chainl1` (op (+) '+' +++ op (-) '-')
unit = number +++ paren'd expr +++ negative unit
number = read <$> munch1 (`elem` ".0123456789") <* skipSpaces

paren'd,negative :: ReadP Double -> ReadP Double
paren'd = between (char '(' <* skipSpaces) (char ')' <* skipSpaces)
negative = (negate <$ char '-' <*>) -- note no skipSpaces

op :: (Double -> Double -> Double) -> Char -> ReadP (Double -> Double -> Double)
op fn c = fn <$ char c <* skipSpaces
_____________________________________________
module EvaluateMathematicalExpression (calc) where

import Data.Function (on)
import Text.ParserCombinators.Parsec

symbol :: String -> Parser ()
symbol s = spaces >> string s >> spaces

expr :: (Fractional a, Read a) => Parser a
expr = spaces >> sum
  where
    sum = product `chainl1` op [("+", (+)), ("-", (-))]
    product = parens `chainl1` op [("*", (*)), ("/", (/))]
    parens = negative <|> (between `on` symbol) "(" ")" expr
    negative = (try $ symbol "-" >> negate <$> parens) <|> val
    val = (many1 $ oneOf "0123456789.") >>= return . read

op :: [(String, (a -> a -> a))] -> Parser (a -> a -> a)
op = foldl1 (<|>) . map (\(s,f) -> try $ symbol s >> return f)

calc :: String -> Double
calc = either (error . show) id . parse expr ""
______________________________________________
module EvaluateMathematicalExpression (calc) where

import Control.Monad.Combinators.Expr
import Data.Scientific
import Data.Void
import Text.Megaparsec
import Text.Megaparsec.Char
import qualified Text.Megaparsec.Char.Lexer as L

type Parser = Parsec Void String

calc :: String -> Double
calc = either (error . errorBundlePretty) id . parse (space *> expr <* eof) ""
  where
    expr :: Parser Double
    expr = makeExprParser term table

    term = parens expr <|> number
    table =
      [ [ prefix  "-"  negate ]
      , [ binary  "*"  (*)
        , binary  "/"  (/) ]
      , [ binary  "+"  (+)
        , binary  "-"  (-) ] ]

    binary name f = InfixL (f <$ symbol name)
    prefix name f = Prefix $ foldr1 (.) <$> some (f <$ symbol name)
    
    number = toRealFloat <$> lexeme L.scientific

    parens = between (symbol "(") (symbol ")")

    lexeme = (<* space)
    symbol = lexeme . string
___________________________________________________
module EvaluateMathematicalExpression (calc) where
import Data.Char
import Data.List
import Data.Tuple
import Debug.Trace

normalise :: String -> String
normalise = filter (\c -> not (isSpace c))

number :: String -> (Double, String)
number s = (read pre :: Double, post)
  where
    pre = takeWhile (\c -> (isDigit c) || c == '.') s
    post = drop (length pre) s 
    
expression :: String -> (Double, String)
expression s = 
  let num = term s
      in walk (fst num) (snd num)
        where 
          walk n [] = (n, [])
          walk n ('+':xs) = 
            let nxt = term xs
                in walk (n + (fst nxt)) (snd nxt)
          walk n ('-':xs) = 
            let nxt = term xs
                in walk (n - (fst nxt)) (snd nxt)
          walk n xs = (n, xs)

term :: String -> (Double, String)
term s = 
  let num = factor s
      in walk (fst num) (snd num)
        where 
          walk n [] = (n, [])
          walk n ('*':xs) = 
            let nxt = factor xs
                in walk (n * (fst nxt)) (snd nxt)
          walk n ('/':xs) = 
            let nxt = factor xs
                in walk (n / (fst nxt)) (snd nxt)
          walk n xs = (n, xs)
          
factor :: String -> (Double, String)
factor s
  | isDigit c = number s
  | c == '(' = 
    let num = expression (drop 1 s)
        in (fst num, drop 1 (snd num))
  | c == '-' =
    let num = factor (drop 1 s)
        in (- (fst num), snd num)
  | otherwise = (0, s)
  where
    c = s!!0

calc :: String -> Double
calc s | trace ("s:" ++ s ++ "\n\n\n") False = undefined
calc s = fst (expression (normalise s))
_________________________________________________
module EvaluateMathematicalExpression (calc) where

import Control.Applicative
import Data.Char (isNumber)
import Data.Maybe (fromJust)
import Data.Functor

calc :: String -> Double
calc s = case runParser expr . filter (`notElem` " \n\t") $ s of
              Just v -> v
              Nothing -> error s


newtype Parser a = Parser { parse :: String -> Maybe (a,String) }

instance Functor Parser where
    fmap f (Parser p) = Parser $ \s -> (\(a, b) -> (f a, b)) <$> p s

instance Applicative Parser where
    pure = return
    (Parser p1) <*> (Parser p2) = Parser $ \s -> do
        (f, s1) <- p1 s
        (a, s2) <- p2 s1
        return (f a, s2)

instance Monad Parser where
    return a = Parser $ \s -> Just (a,s)
    (>>=) p f  = Parser $ \s -> parse p s >>= \(a, s') -> parse (f a) s' 

instance Alternative Parser where
    empty = Parser $ const Nothing
    (Parser p1) <|> pp2 = Parser $ \s -> p1 s <|> parse pp2 s

runParser :: Parser a -> String -> Maybe a
runParser m s =
  case parse m s of
    Just (res, []) -> Just res
    Just (_, rs)   -> Nothing
    _           -> Nothing


check :: (Char -> Bool) -> Parser Char
check f = Parser $ \s -> case s of
  (x:xs) | f x -> Just (x, xs)
  _            -> Nothing


char :: Char -> Parser Char
char c = check (== c)

oneOf :: [Char] -> Parser Char
oneOf cs = check (\c -> elem c cs)

litteral :: Parser Char
litteral = check (`notElem` "().|*")

paren :: Parser a -> Parser a
paren p = do
    void $ char '('
    e <- p
    void $ char ')'
    return e


number :: Parser Double
number = read <$> some (check isNumber <|> char '.')

atom :: Parser Double
atom = do
    neg <- length <$> many (char '-')
    val <- number <|> paren expr
    return $ if even neg then val else -val

term :: Parser Double
term = do
    t1 <- atom
    loop t1
    where
        next t1 = do
            op <- oneOf "*/"
            t2 <- atom
            case op of
                '*' -> loop (t1 * t2)
                '/' -> loop (t1 / t2)
        loop t = next t <|> return t

expr :: Parser Double
expr = do
    t1 <- term
    loop t1
    where
        next t1 = do
            op <- oneOf "+-"
            t2 <- term
            case op of
                '+' -> loop (t1 + t2)
                '-' -> loop (t1 - t2)
        loop t = next t <|> return t
