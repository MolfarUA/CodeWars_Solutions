module DnaToRna where 

dnaToRna :: String -> String 
dnaToRna = map (\c -> if c == 'T' then 'U' else c)

_____________________________
module DnaToRna where 

dnaToRna :: String -> String 
dnaToRna [] = []
dnaToRna ('T' : xs) = 'U' : dnaToRna xs
dnaToRna (x : xs) = x : dnaToRna xs

_____________________________
module DnaToRna where 

trans :: Char -> Char
trans 'T' = 'U'
trans  ch =  ch

dnaToRna :: String -> String 
dnaToRna = map trans

_____________________________
module DnaToRna where 

dnaToRna :: String -> String 
dnaToRna = map f
    where f 'T' = 'U'
          f c = c
          
_____________________________
module DnaToRna where 

dnaToRna :: String -> String 
dnaToRna = map $ \c -> if c == 'T' then 'U' else c

_____________________________
module DnaToRna where 

dnaToRna :: String -> String 
dnaToRna xs = map (\c -> if c == thymine then uracil else c) xs
  where thymine = 'T'
        uracil = 'U'
        
_____________________________
module DnaToRna where 

dnaToRna :: String -> String 
dnaToRna = map d2r
  where d2r 'T' = 'U'
        d2r  c  =  c
