module ListOps where
import Prelude hiding (head, tail, init, last)

head :: [a] -> a
head (x:_) = x

tail :: [a] -> [a]
tail (_:xs) = xs

init :: [a] -> [a]
init [x] = []
init (x:xs) = x : init xs

last :: [a] -> a
last [x] = x
last (_:xs) = last xs
_____________________________
module ListOps where
import Prelude hiding (head, tail, init, last)

head = (!! 0)
tail = drop 1
init = (reverse . tail . reverse)
last = (head . reverse)
_____________________________
module ListOps where
import Prelude hiding (head, tail, init, last)

head :: [a] -> a
head [] = error "empty list has no head"
head (x:_) = x

tail :: [a] -> [a]
tail (_:xs) = xs

init :: [a] -> [a]
init [x] = []
init (x:xs) = x:(init xs)

last :: [a] -> a
last [x] = x
last (_:xs) = last xs
_____________________________
module ListOps where
import Prelude hiding (head, tail, init, last)

head :: [a] -> a
head (x:_) = x

tail :: [a] -> [a]
tail (_:xs) = xs

last :: [a] -> a
last (x:[]) = x
last (_:xs) = last xs

init :: [a] -> [a]
init (_:[]) = []
init (x:xs) = x : init xs
