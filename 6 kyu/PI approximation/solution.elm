module Kata exposing (iterPi)

iterPiAux : Float -> Int -> Float -> (Int, Float)
iterPiAux eps cnt som =
    let
        sign = if (modBy 2 cnt == 0) then 1 else -1
        s = som + sign / (toFloat (2 * cnt + 1))
        r = abs(pi - 4 * s)
    in 
        if r < eps then (cnt+1, (toFloat (floor((4 * s * 1e10))) / 1e10))
        else iterPiAux eps (cnt + 1) s
iterPi : Float -> (Int, Float)
iterPi eps = iterPiAux eps 0 0
________________________________________
module Kata exposing (iterPi)

f : Float -> Int -> Float -> (Int, Float)
f e k m =
    let
        s = if (modBy 2 k == 0) then 1 else -1
        n = s / (toFloat (2 * k + 1)) + m
    in 
        if (abs(pi - 4 * n)) < e then (k + 1, (toFloat (floor((n * 4 * 1e10))) / 1e10))
        else f e (k + 1) n
        
iterPi : Float -> (Int, Float)
iterPi e = f e 0 0
