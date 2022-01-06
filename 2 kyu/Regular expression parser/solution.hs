module RegExpParser (RegExp(..), parseRegExp) where

import Control.Applicative (pure, empty, (<|>), (<*>), (<$>) , Applicative, Alternative)
import Control.Monad (ap, (>=>), guard)
import Control.Arrow ((&&&))

data RegExp = Normal Char | Any | ZeroOrMore RegExp | Or RegExp RegExp | Str [RegExp] deriving (Show, Eq)

newtype Parser a = Parser {runParser :: String -> Maybe (a, String)}

instance Monad Parser where
    return x = Parser (\s -> Just (x, s))
    (Parser f) >>= g = Parser (f >=> (\(x, s) -> runParser (g x) s))

instance Functor Parser where
    fmap f = ap (return f)

instance Applicative Parser where
    pure = return
    fa <*> xa = fa >>= \f -> xa >>= \x -> return (f x)

instance Alternative Parser where
    empty = Parser (const Nothing)
    (Parser f) <|> (Parser g) = Parser (uncurry (<|>) . (f &&& g))
    

liftToken :: (Char -> Maybe a) -> Parser a
liftToken f = Parser g
    where g [] = Nothing
          g (c:cs) = f c >>= (\x -> Just (x, cs))

eat :: Char -> Parser ()
eat t = liftToken (guard . (==t))

wrap :: Char -> Parser a -> Char -> Parser a
wrap l p r = eat l >> 
             p >>= 
             \x -> eat r >>
             return x 
            
parseList :: Parser a -> Parser [a]
parseList itemP = listP
    where listP = ((:) <$> itemP <*> listP) <|> return []

(~>) :: Char -> a -> Parser a
c ~> x = eat c >> return x

atomP :: Parser RegExp
atomP = liftToken isChar <|> ('.' ~> Any) <|> wrap '(' regExpP ')'
  where isChar c | c `elem` ".*|()" = Nothing
                 | otherwise        = Just (Normal c)

zeroOrMoreP :: Parser RegExp
zeroOrMoreP = (atomP >>= 
               \a -> eat '*' >> 
               return (ZeroOrMore a)) <|> atomP

seqP :: Parser RegExp
seqP = (zeroOrMoreP >>= 
        \a -> zeroOrMoreP >>= 
        \b -> parseList zeroOrMoreP >>= 
        \c -> return (Str (a:b:c))) <|> zeroOrMoreP
    
regExpP :: Parser RegExp
regExpP = (seqP >>=
           \l -> eat '|' >>
           seqP >>= 
           \r -> return (Or l r)) <|> seqP
    
parseRegExp :: String -> Maybe RegExp
parseRegExp s = case runParser regExpP s of Just (x, "") -> Just x
                                            _            -> Nothing
________________________________________
module RegExpParser
       ( RegExp(..)
       , parseRegExp
       ) where

import Text.ParserCombinators.ReadP
import Control.Monad
import Control.Applicative ((<$>),(<*>),(<*),(*>))

data RegExp = Normal Char       -- ^ A character that is not in "()*|."
            | Any               -- ^ Any character
            | ZeroOrMore RegExp -- ^ Zero or more occurances of the same regexp
            | Or RegExp RegExp  -- ^ A choice between 2 regexps
            | Str [RegExp]      -- ^ A sequence of regexps.
  deriving (Show, Eq)


parseRegExp :: String -> Maybe RegExp
parseRegExp s = helper $ readP_to_S regExp s
  where
    helper rs = case [a | (a,"") <- rs] of
      []    -> Nothing
      (a:_) -> Just a

regExp :: ReadP RegExp
regExp = strExp +++ (Or <$> (strExp <* char '|') <*> strExp)

strExp :: ReadP RegExp
strExp = charExp
     +++ (Str <$> many1 charExp)

charExp :: ReadP RegExp
charExp = atom +++ (ZeroOrMore <$> atom <* char '*')

atom :: ReadP RegExp
atom = (Normal <$> satisfy (not . flip elem "()*|."))
   +++ (char '.' *> return Any)
   +++ (char '(' *> regExp <* char ')')
________________________________________
module RegExpParser
( RegExp(..)
, parseRegExp
) where

    import Control.Applicative
    import Data.Char

    newtype Parser a = Parser (String -> Maybe (a, String))
    
    parse :: Parser a -> String -> Maybe (a, String)
    parse (Parser parser) = parser

    item :: Parser Char
    item = Parser (\ st -> case st of 
                            [] -> Nothing
                            (x : xs) -> Just (x , xs))

    instance Functor Parser where
        -- fmap :: (a -> b) -> Parser a -> Parser b
        fmap f p = Parser (\ st -> case parse p st of
                                        Nothing -> Nothing
                                        Just (v, out) -> Just (f v, out))

    instance Applicative Parser where

        -- pure :: a -> Parser a
        pure v = Parser (\ st -> Just (v, st))

        -- (<*>) :: Parser (a -> b) -> Parser a -> Parser b
        pab <*> pa = Parser (\ st -> case parse pab st of
            Nothing -> Nothing
            Just (v, out) -> parse (fmap v pa) out)

    instance Monad Parser where

        -- (>>=) :: Parser a -> (a -> Parser b) -> Parser b
        pa >>= apb = Parser (\ st -> case parse pa st of
            Nothing -> Nothing
            Just (a, out) -> parse (apb a) out)

    instance Alternative Parser where

        -- empty :: Parser a
        empty = Parser $ const Nothing

        -- <|> :: Parser a -> Parser a -> Parser a
        pa <|> pa2 = Parser (\ st -> case parse pa st of
            Nothing -> parse pa2 st
            Just x -> Just x)

    data RegExp = Normal Char       -- ^ A character that is not in "()*|."
        | Any               -- ^ Any charater
        | ZeroOrMore RegExp -- ^ Zero or more occurances of the same regexp
        | Or RegExp RegExp  -- ^ A choice between 2 regexps
        | Str [RegExp]      -- ^ A sequence of regexps.
        deriving (Show, Eq)

    failure :: Parser a
    failure = Parser $ const Nothing

    sat :: (Char -> Bool) -> Parser Char
    sat f = do 
        x <- item
        if f x then return x else failure

    digit :: Parser Char
    digit = sat isDigit

    lower :: Parser Char
    lower = sat isLower

    upper :: Parser Char
    upper = sat isUpper

    letter :: Parser Char
    letter = sat isLetter

    alphanum :: Parser Char
    alphanum = sat isAlphaNum

    char :: Char -> Parser Char
    char x = sat (==x)

    oneOf :: String -> Parser Char
    oneOf "" = failure
    oneOf [x] = char x
    oneOf (x : xs) = char x <|> oneOf xs

    noneOf :: String -> Parser Char
    noneOf "" = item
    noneOf str = Parser (\ st -> if (st == "") || head st `elem` str then Nothing
        else Just (head st, tail st))

    parseSimple :: Parser RegExp
    parseSimple = do
        c <- noneOf "()*|."
        return $ Normal c
        <|> do
            _ <- char '.'
            return Any
            <|> do
                _ <- char '('
                x <- parseOr
                _ <- char ')'
                return x

    parseStr :: Parser RegExp
    parseStr = do
        x <- parseMulti
        xs <- some parseMulti
        return $ Str (x : xs)
        <|> parseMulti

    parseMulti :: Parser RegExp
    parseMulti = do
        x <- parseSimple
        _ <- char '*'
        return $ ZeroOrMore x
        <|> parseSimple

    parseOr :: Parser RegExp
    parseOr = do
        x <- parseStr
        _ <- char '|'
        y <- parseStr
        return $ Or x y
        <|> parseStr

    parseRegExp :: String -> Maybe RegExp
    parseRegExp s = case parse parseOr s of
        Just (x , []) -> Just x
        _ -> Nothing
        
________________________________________
module RegExpParser
  ( RegExp (..),
    parseRegExp,
  )
where

import Data.Functor (($>))
import Text.Parsec
import Text.Parsec.String

data RegExp
  = -- | A character that is not in "()*|."
    Normal Char
  | -- | Any charater
    Any
  | -- | Zero or more occurances of the same regexp
    ZeroOrMore RegExp
  | -- | A choice between 2 regexps
    Or RegExp RegExp
  | -- | A sequence of regexps.
    Str [RegExp]
  deriving (Show, Eq)

res = "()*|."

pAny :: Parser RegExp
pAny = char '.' $> Any

pNormal :: Parser RegExp
pNormal = Normal <$> noneOf res

parens = between (char '(') (char ')')

pFactor = parens pExpr <|> pNormal <|> pAny

pExpr = chainl1 (toStr <$> many1 pTerm) (char '|' $> Or)

pTerm = do
  f <- pFactor
  p <- try (char '*' $> ZeroOrMore) <|> return id
  return $ p f

toStr [x] = x
toStr xs = Str xs

parseRegExp :: String -> Maybe RegExp
parseRegExp s = case parse (pExpr <* eof) "RegExp" s of
  Left _ -> Nothing
  Right x -> Just x
________________________________________
module RegExpParser
       ( RegExp(..)
       , parseRegExp
       ) where
       
import Text.ParserCombinators.ReadP
import Data.List (nub)

data RegExp = Normal Char       -- ^ A character that is not in "()*|."
            | Any               -- ^ Any charater
            | ZeroOrMore RegExp -- ^ Zero or more occurances of the same regexp
            | Or RegExp RegExp  -- ^ A choice between 2 regexps
            | Str [RegExp]      -- ^ A sequence of regexps.
  deriving (Show, Eq)

metacharacters = "()*|."

char' :: ReadP RegExp
char' = Normal <$> satisfy (`notElem` metacharacters)

any' :: ReadP RegExp
any' = char '.' >> return Any

group :: ReadP RegExp
group = do char '('
           e <- expression
           char ')'
           return e

atom :: ReadP RegExp
atom = group +++ any' +++ char'

star :: ReadP RegExp
star = do e <- atom
          char '*'
          return $ ZeroOrMore e

factor :: ReadP RegExp
factor = star <++ atom

manyFactor :: ReadP RegExp
manyFactor = do e <- factor
                es <- many1 factor
                return $ Str (e:es)

term :: ReadP RegExp
term = star +++ (manyFactor) +++ factor

union :: ReadP RegExp
union = do e1 <- term
           char '|'
           e2 <- expression
           return (Or e1 e2)

expression :: ReadP RegExp
expression = union +++ term


parseRegExp :: String -> Maybe RegExp
parseRegExp s = case readP_to_S expression s of
                  [] -> Nothing
                  xs -> case nub $ filter ((==) "" . snd) xs of
                    [(a, _)] -> Just a
                    _ -> Nothing
________________________________________
module RegExpParser
       ( RegExp(..)
       , parseRegExp
       ) where

data RegExp = Normal Char       -- ^ A character that is not in "()*|."
            | Any               -- ^ Any charater
            | ZeroOrMore RegExp -- ^ Zero or more occurances of the same regexp
            | Or RegExp RegExp  -- ^ A choice between 2 regexps
            | Str [RegExp]      -- ^ A sequence of regexps.
  deriving (Show, Eq)

getRegExpList :: RegExp -> Maybe [RegExp]
getRegExpList (Str sx) = Just sx
getRegExpList _ = Nothing

data Token = TChar Char
           | TBracketBegin
           | TBracketEnd
           | TAny
           | TOr
           | TZeroOrMore
           | TEOF

parseRegExp :: String -> Maybe RegExp
parseRegExp = grammarize . tokenize

data TokenKind = KChar
               | KBracketBegin
               | KBracketEnd
               | KAny
               | KOr
               | KZeroOrMore
               | KEOF
               deriving (Eq)

kind :: Token -> TokenKind
kind (TChar _)       = KChar
kind (TBracketBegin) = KBracketBegin
kind (TBracketEnd)   = KBracketEnd
kind (TAny)          = KAny
kind (TOr)           = KOr
kind (TZeroOrMore)   = KZeroOrMore
kind (TEOF)          = KEOF

isKind :: Token -> TokenKind -> Bool
isKind = (==) . kind

-- Lexical

-- TChar         ::= ~["(",")",".","|","*"]
-- TBracketBegin ::= "("
-- TBracketEnd   ::= ")"
-- TAny          ::= "."
-- TOr           ::= "|"
-- TZeroOrMore   ::= "*"
-- TEOF          ::= ""

tokenize :: String -> [Token]
tokenize [] = [TEOF]
tokenize (x:sx) = (case x of '(' -> TBracketBegin
                             ')' -> TBracketEnd
                             '.' -> TAny
                             '|' -> TOr
                             '*' -> TZeroOrMore
                             _ -> TChar x) : tokenize sx
-- Grammar

-- TopLevel       ::= RegExpList() (Or())? < EOF >
-- Or             ::= < TOr > RegExpList()
-- RegExpList     ::= RegExp() (RegExpListTail())?
-- RegExpListTail ::= (RegExp())+
-- RegExp         ::= (Normal() | Any() | CapturingGroup()) (ZeroOrMore())?
-- Normal         ::= < TChar >
-- Any            ::= < TAny >
-- ZeroOrMore     ::= < TZeroOrMore >
-- CapturingGroup ::= < TBracketBegin > RegExpList() (Or())? < TBracketEnd >

grammarize :: [Token] -> Maybe RegExp
grammarize = snd . compileTopLevel

checkRegExp :: ([Token], Maybe RegExp) -> ([Token], Maybe RegExp) -> ([Token], Maybe RegExp)
checkRegExp previous@(_, Nothing) next = previous
checkRegExp previous@(_, Just _) next = next

compileTopLevel :: [Token] -> ([Token], Maybe RegExp)
compileTopLevel tokens = checkRegExp result $ case kind $ head tokens' of {
    KOr  -> let {
      result'@(tokens''', rightRegExpList) = compileOr tokens';
      tokens'''' = tail tokens''';
    } in checkRegExp result' $ case kind $ head tokens''' of {
        KEOF -> (tokens'''', pure Or <*> leftRegExpList <*> rightRegExpList);
        _    -> (tokens''', Nothing);
      };
    KEOF -> (tokens'', leftRegExpList);
    _    -> (tokens', Nothing);
  }
  where
    result@(tokens', leftRegExpList) = compileRegExpList tokens
    tokens'' = tail tokens'

compileOr :: [Token] -> ([Token], Maybe RegExp)
compileOr tokens = case kind $ head tokens of {
    KOr -> compileRegExpList tokens';
    _   -> (tokens, Nothing);
  }
  where
    tokens' = tail tokens

compileRegExpList :: [Token] -> ([Token], Maybe RegExp)
compileRegExpList tokens = checkRegExp result $ case kind $ head tokens' of {
    x | (x == KChar)         ||
        (x == KBracketBegin) ||
        (x == KAny)             -> let {
          result'@(tokens'', regExpListTail) = compileRegExpListTail tokens'
        } in checkRegExp result' $ (tokens'', pure Str <*> (pure (:) <*> regExp <*> (regExpListTail >>= getRegExpList)));
    _                           -> (tokens', regExp)
  }
  where
    result@(tokens', regExp) = compileRegExp tokens

compileRegExpListTail :: [Token] -> ([Token], Maybe RegExp)
compileRegExpListTail tokens = checkRegExp result $ case kind $ head tokens' of {
    x | (x == KChar)         ||
        (x == KBracketBegin) ||
        (x == KAny)             -> let {
          result'@(tokens'', regExpListTail) = compileRegExpListTail tokens'
        } in checkRegExp result' $ (tokens'', pure Str <*> (pure (:) <*> regExp <*> (regExpListTail >>= getRegExpList)));
    _                           -> (tokens', pure (Str . (:[])) <*> regExp)
  }
  where
    result@(tokens', regExp) = compileRegExp tokens

compileRegExp :: [Token] -> ([Token], Maybe RegExp)
compileRegExp tokens = let {
    result@(tokens', regExp) = case kind $ head tokens of {
      KChar         -> compileNormal tokens;
      KAny          -> compileAny tokens;
      KBracketBegin -> compileCapturingGroup tokens;
      _             -> (tokens, Nothing);
    };
    tokens'' = tail tokens'
  } in checkRegExp result $ case kind $ head tokens' of {
      KZeroOrMore -> (tokens'', pure ZeroOrMore <*> regExp);
      _           -> (tokens', regExp);
    }

compileNormal :: [Token] -> ([Token], Maybe RegExp)
compileNormal tokens = case head tokens of {
    TChar c -> (tail tokens, Just $ Normal c);
    _       -> (tokens, Nothing);
  }

compileAny :: [Token] -> ([Token], Maybe RegExp)
compileAny tokens = case kind $ head tokens of {
    KAny -> (tail tokens, Just Any);
    _    -> (tokens, Nothing);
  }

compileCapturingGroup :: [Token] -> ([Token], Maybe RegExp)
compileCapturingGroup tokens = case kind $ head tokens of {
    KBracketBegin -> let {
      result@(tokens'', leftRegExpList) = compileRegExpList tokens'
    } in checkRegExp result $ let {
        result''@(tokens'''', capturingGroup) = case kind $ head tokens'' of {
          KOr -> let {
            result'@(tokens''', rightRegExpList) = compileOr tokens''
          } in (tokens''', pure Or <*> leftRegExpList <*> rightRegExpList);
          _   -> (tokens'', leftRegExpList);
        };
        tokens''''' = tail tokens'''';
      } in checkRegExp result'' $ case kind $ head tokens'''' of {
          KBracketEnd -> (tokens''''', capturingGroup);
          _           -> (tokens'''', Nothing);
        };
    _             -> (tokens, Nothing);
  }
  where
    tokens' = tail tokens
