604f8591bf2f020007e5d23d



module NextMultipleOfFive (nextMultipleOfFive) where

nextMultipleOfFive :: Int -> Int
nextMultipleOfFive 0 = 5
nextMultipleOfFive n = case n `mod` 5 of 0 -> 2 * n
                                         1 -> 4 * n + 1
                                         2 -> 2 * n + 1
                                         3 -> 4 * n + 3
                                         4 -> 8 * n + 3
_______________________________
module NextMultipleOfFive (nextMultipleOfFive) where

-- q[n] goes to q[n+1] and spans q{0,1,2,3,4}
-- each time q transitions i->2i or i->2i+1 based on the bit
-- the modulus of the new value determines the new state
-- this defines graph a maximum of either 1, 2, 3 transitions away depending on q
-- you can draw the transition diagram to identify the specifics paths 
-- these specific paths become an equation which if satifisfied reveals the nearest digit
-- this is comprised of a path length multiplacand and an added number identifying the bit path

nextMultipleOfFive :: Int -> Int
nextMultipleOfFive 0 = 5
nextMultipleOfFive n | (2*n) `mod` 5 == 0 = (2*n)
                     | (2*n) `mod` 5 == 4 = (2*n)+1
                     | (4*n) `mod` 5 == 4 = (4*n)+1
                     | (4*n) `mod` 5 == 2 = (4*n)+3
                     | (8*n) `mod` 5 == 2 = (8*n)+3
                     | otherwise = n
_______________________________
module NextMultipleOfFive (nextMultipleOfFive) where

nextMultipleOfFive :: Int -> Int
nextMultipleOfFive n | n == 0 = 5
                     | otherwise = f (decToBin n) [[1],[0]]

f :: [Int] -> [[Int]] -> Int
f b a | e = binToDec (b ++ (head $ filter(\e -> mod (binToDec (b++e)) 5 == 0) a))
      | otherwise = f b (concat $ map(\e -> [[1]++e,[0]++e]) a)
        where e = any(\e -> mod (binToDec (b++e)) 5 == 0) a

binToDec :: [Int] -> Int
binToDec a | null a = 0
           | otherwise = (last a) + 2 * (binToDec $ init a) 

decToBin :: Int -> [Int]
decToBin n | n < 2     = [n]
           | otherwise = (decToBin q) ++ [r] where (q,r) = divMod n 2
