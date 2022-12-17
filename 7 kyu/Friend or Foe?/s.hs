55b42574ff091733d900002f


module FriendOrFoe where

friend :: [String] -> [String]
friend = filter (\s -> length s == 4)
________________________________
module FriendOrFoe where

friend :: [String] -> [[Char]]
friend = filter $ (== 4) . length
________________________________
module FriendOrFoe where

friend :: [String] -> [String]
friend xs = [x | x <- xs, length x == 4]
