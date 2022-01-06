module InfiniteDigitalString where

findPosition :: String -> Integer
findPosition str = minimum (i1 ++ i2 ++ [index str])
  where n = length str
        i1 = map (\(i,j) -> (flip (-) $ fromIntegral i).index.take j.drop i $ str) $
          filter check1 [(i,j) | i<-[0..n-1], j<-[1..n-i]]
        check1 (i,j) = c1==s1 && c2==s2 && str !! i /= '0'
          where s1 = take i str
                s2 = drop (i+j) str
                x = read.take j.drop i $ str
                c1 = reverse.take (length s1).reverse.concat.map show $ [max (x-length s1) 1..x-1]
                c2 = take (length s2).concat.map show $ [x+1..]
        i2 = map (\(s1,s2) -> if (\s -> (null $ s) || (not.null.filter (/='9') $ s)) $ s1 then reduce1 s1 s2 else reduce2 s1 s2).filter ((/='0').head.snd) $ [(take i str,drop i str) | i<-[1..n-1]]
        reduce1 s1' s2 = index (s2 ++ drop r s1) - (fromIntegral.length $ s1)
          where s1 = (\s -> replicate (length s1' - length s) '0' ++ s).show $ read s1' + 1
                Just r = if read s1'==0 then Just 0 else maximum.filter (\(Just i) -> check (s2 ++ drop i s1) (length s2 - i)).filter (not.null) $ [if take i s1 == drop (length s2 - i) s2 then Just i else Nothing| i<-[0..length s1]]
                check s k = and.zipWith (==) str $ drop k ((show $ read s -1) ++ s)
        reduce2 s1 s2' = index (s2 ++ drop r s1) + (fromIntegral.length $ s2) - fromIntegral r
          where s2 = (\s -> replicate (length s2' - length s) '0' ++ s).show $ read s2' - 1
                Just r = maximum.filter (\(Just i) -> check (s2 ++ drop i s1) (length s2 - i)).filter (not.null) $ [if take i s1 == drop (length s2 - i) s2 then Just i else Nothing| i<-[0..length s1]]
                check s k = and.zipWith (==) str $ drop k (s ++ (show $ read s + 1))
        index s | head s /= '0' = let n = fromIntegral.length $ s in (1-10^n) `div` 9 + n * read s
                | True = index ('1':s) + 1
___________________________________________________
module InfiniteDigitalString where

import Control.Monad (guard)
import Data.List
import Data.Maybe (maybeToList, fromJust, isNothing)

findPosition :: [Char] -> Integer
findPosition str = minimum $ map position $ generateCandidates str

position :: [String] -> Integer
position [pre, suf] = let next = if all (=='9') pre then '0' <$ pre else show $ read pre + 1
                          succ = replicate (length pre - length next) '0' ++ next
                          common = fromJust $ find (\g -> g `isPrefixOf` succ && g /= succ && g /= suf) $ tails suf
                          stripSuffix s ss = reverse <$> stripPrefix (reverse s) (reverse ss)
                          num = read (fromJust (stripSuffix common suf) ++ succ)
                      in positionOfNumber num - genericLength pre
position candidate = let offset = genericLength $ head candidate
                         num = read $ candidate!!1 :: Integer
                     in positionOfNumber num - offset

positionOfNumber :: Integer -> Integer
positionOfNumber num = let digitsPerNumber = map (\x -> 9*10^x) [0..]
                           digNum = (genericLength $ show num) :: Integer
                       in sum (zipWith (*) [1..] (genericTake (digNum-1) digitsPerNumber)) + (digNum * (num - 10^(digNum-1)))
    
generateCandidates :: String -> [[String]]
generateCandidates str = do
    prelength <- [0..length str]
    let (prefix, v) = splitAt prelength str
    suflength <- [0.. length v]
    let (mid, suffix) = splitAt suflength v
    let optionMiddle = do
            midlength <- [1.. length mid]
            mids <- maybeToList $ checkMiddle mid midlength
            guard $ checkIxes prefix mids suffix
            return $ prefix : map show mids ++ [suffix]
        optionIxes = do
            guard $ null mid
            guard $ prefix /= "" 
            if all (=='0') prefix && null suffix 
                then return [prefix,"1"]
                else guard (suffix /= "" && isNothing (stripPrefix "0" suffix)) >> return [prefix,suffix]
    optionMiddle ++ maybeToList optionIxes
    
checkMiddle :: String -> Int -> Maybe [Integer]
checkMiddle str start = let (h,t) = splitAt (fromIntegral start) str 
                            res = read h : unfoldr (\(last,rest) -> stripPrefix (show $ last +1) rest >>= \rest2 -> return (last+1, (last+1, rest2))) (read h,t)
                        in guard (concatMap show res == str && read h /= 0) >> return res

checkIxes :: String -> [Integer] -> String -> Bool
checkIxes prefix mid suffix = let (p,n) = (show $ head mid - 1, show $ last mid + 1)
                              in prefix `isSuffixOf` p && suffix `isPrefixOf` n && p /= "0"
___________________________________________________
module InfiniteDigitalString where

import Data.Maybe

findPosition :: [Char] -> Integer
findPosition str 
    | all (=='0') str = (1+) . getPos . (10^) . length $ str
    | otherwise = 
       getPos'
     . head
     . filter isJust
     . map (tryParse str) $ [1..]

getPos :: Integer -> Integer 
getPos num = case lookup (fromIntegral (n-1)) digits2pos of 
    Just acc -> acc + (num - l) * fromIntegral n
    Nothing  -> 0
  where 
    n = length $ show num
    l = 10^(n-1) 

getPos' :: Maybe (Integer, Int) -> Integer 
getPos' (Just (num, pos)) = getPos num + fromIntegral pos - 1

digits2num :: [(Integer, Integer)]
digits2num = [(d, 9 * 10^(d-1)) | d <- [1..]]

digits2pos :: [(Integer, Integer)]
digits2pos = (0,0):[(d, f $ fromIntegral d) | d <- [1..]]
  where 
    f d = foldr (\(d,n) acc -> acc + d * n) 0 $ take d digits2num

tryParse
    :: [Char]               -- ^ number string
    -> Int                  -- ^ length of the first number
    -> Maybe (Integer, Int) -- ^ (the first number, digit of it)
tryParse str n = case filter isJust $ [tryParse' str n d | d <- [1..n]] of 
    [] -> Nothing 
    as -> foldl1 (\m1 m2 -> if getPos' m1 < getPos' m2 then m1 else m2) as

tryParse'
    :: [Char]
    -> Int
    -> Int
    -> Maybe (Integer, Int)
tryParse' str n d
    | length (show first) /= n = Nothing 
    | first == 0 = Nothing 
    | go (first+1) $ drop (n-d+1) str = Just (first, d)
    | otherwise = Nothing
  where
    firstT  = take (n - d + 1) str
    secondH = take n . drop (n - d + 1) $ str
    firstH  = if d > 1 && firstT == replicate (n-d+1) '9'
              then let tmp = show . (\x -> x-1) . read $ take (d-1) secondH
                   in if   length tmp < d-1 || all (=='0') tmp
                      then replicate (d-1) '9'
                      else tmp
              else take (d-1) secondH
    first = read (firstH ++ firstT) :: Integer
    go _ [] = True
    go num ns = all (uncurry (==)) (zip (show num) (take n' ns)) && go (num+1) (drop n' ns)
      where n' = length . show $ num 
___________________________________________________
module InfiniteDigitalString where
import Debug.Trace

findPosition :: String -> Integer
findPosition = lun 1

lun width str = if rowBest >= 0 then rowBest else lun (width+1) str
    where rowBest = foldr (\off acc -> case geneS width off str of 
                                         (num, True) -> if (traceShow num acc) < 0 then num else min acc num
                                         _ -> acc) (-1) [0 .. width-1] 

geneS :: Int -> Int -> String -> (Integer, Bool)
geneS width offset str 
  | all (=='0') str = (1 + calIndex (read $ '1':str) 0, True) 
  | otherwise = (calIndex (head nums) (toInteger offset), genS == str)
    where numlen = toInteger $ len `div` width + 1
          len = length str
          pregap = width - offset
          tailgap = width + offset - len 
          gapdiff = len - width
          frontnum = take width $ drop offset str
          tailnum = replicate (max 0 (tailgap - length pretail)) '0' ++ pretail
                   where pretail = (reverse . take tailgap . reverse) $ show $ 1 + (read $ take tailgap $ drop gapdiff str::Integer)
          start 
            | offset > 0 = prestart - 1
            | otherwise = prestart
            where prestart = read (frontnum ++ tailnum)
          nums = [start .. start + numlen]
          headnum = head nums
          genS 
            | offset == 0 = take (fromIntegral len) . concatMap show $ nums
            | otherwise = take (fromIntegral len) . drop (fromIntegral $ (toInteger . length . show) headnum - toInteger offset) . concatMap show $ nums


calIndex n offset 
    | offset == 0 = calhelper len + (n - 10 ^ len) * (len + 1)
    | otherwise = calhelper len + (n - 10 ^ len) * (len + 1) + width - offset
        where len = toInteger $ length (show n) - 1 
              width = len + 1

calhelper :: Integer -> Integer
calhelper 0 = 0
calhelper 1 = 9 
calhelper k = (10 ^ k - 10 ^ (k-1)) * k + calhelper (k - 1)
___________________________________________________
module InfiniteDigitalString where
import Control.Applicative
import Control.Monad
import Control.Arrow ((&&&))
import Data.List (foldl', isPrefixOf, inits, tails)
import Data.Char (ord)
import Data.Maybe (catMaybes)
import Debug.Trace

numDigits :: Integer -> Int
numDigits = length . takeWhile (>0) . iterate (`div` 10) 

position :: Integer -> Int -> Integer
position n overlap = (go n) - (fromIntegral overlap)
  where
    go :: Integer -> Integer
    go 0 = 0
    go x =
     let l = fromIntegral $ numDigits x in
     let p10 = 10^(l - 1) in
     (x - p10 + 1) * l + go (p10 - 1)

s2i :: String -> Maybe Integer
s2i str
   | "0" `isPrefixOf` str = Nothing
   | otherwise = Just $ foldl' (\x y -> x * 10 + y) 0 $ map (\x -> toInteger $ ord x - ord '0') str

twoNumber :: Int -> Int -> String -> Maybe Integer
twoNumber overlap l1 str = do
  let (s1, s2) = (take l1 &&& drop l1) str
  let l2 = length s2
  n1 <- s2i ('1':s1)
  n2 <- s2i s2
  let n1' = succ n1
  let p10 = 10 ^ (l1 - overlap)
  let n2' = n2 * p10 + (n1' `mod` p10)
  guard $ n2' > 1
  let lp = numDigits $ n2' - 1
  let s = take (l1 + l2) . drop (lp - l1) . concat . map show $ [n2' - 1, n2']
  guard $ s == str
  return $ position (n2' - 1) l1
  
midNumber :: Int -> Int -> String -> Maybe Integer
midNumber p q str = do
  v <- s2i . take q . drop p $ str
  let (start, overlap) = if p == 0 then (v, q) else (v - 1, p)
  guard $ start > 0
  let offset = (numDigits start) - overlap
  let l = length str
  let s = take l . drop offset . concat .  map show $ [start..]
  guard $ s == str
  return $ position start overlap

findPosition :: [Char] -> Integer
findPosition str = minimum . catMaybes $ [singleNumber] ++ twoNumbers ++ midNumbers ++ [position <$> (s2i $ '1':str) <*> pure l]
  where
    l = length str
    singleNumber = position <$> s2i str <*> pure l
    twoNumbers = [twoNumber overlap p str | p <- [1..l-1], overlap <- [0..min p (l-p)]]
    midNumbers = [midNumber p q str | p <- [0..l], p + p < l, q <- [p+1..l-p]]
