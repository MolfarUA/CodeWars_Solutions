module Haskell.Codewars.DivisibleBy7 where

solution :: String
solution = "^(0|(10((0|11)(1|00))*(10|(0|11)01)|11)(01*0(0|101|1(1|00)((0|11)(1|00))*(10|(0|11)01)))*1)+$"

_____________________________
module Haskell.Codewars.DivisibleBy7 where

-- 1 1 0 1 1 1 0 1 1 0 1 0 1 0 1 0 1 0 1 1 0 0 0 1 0 0 0 1 0
solution :: String
solution = "^(0|111|10101|(110|10100)(1|000)*001|(100|1011|(110|10100)(1|000)*01)((00|1)0|(00|1)11|(010|(00|1)100)(1|000)*01)*(011|(00|1)101|(010|(00|1)100)(1|000)*001))+$"

_______________________
module Haskell.Codewars.DivisibleBy7 where

solution :: String
solution = "^(0+|0*1(0(01|1(001*0)*11)*00|0(01|1(001*0)*11)*1(001*0)*010*1|0(01|1(001*0)*11)*1(001*0)*10|1(01*0(1(10)*11)*0)*01*0(1(10)*11)*1(10)*0|1(01*0(1(10)*11)*0)*10*1)*(0(01|1(001*0)*11)*1(001*0)*010*|1(01*0(1(10)*11)*0)*10*))$"
