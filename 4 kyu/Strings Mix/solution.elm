module Kata exposing (mix)

fillAlpha : String -> List (String, Int)
fillAlpha s =
    let
        alpha = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        a = List.map (\c -> (c, List.length(List.filter (\ ch -> ch == c) (String.split "" s)))) alpha
    in a
mkPair : (String, (Int, Int)) -> (String, (Int, Int))
mkPair (a, (l1, l2)) =
    let m = max l1 l2
    in
        if m > 1 then
            if m > l1 then (a, (m, 2))
            else if m > l2 then (a, (m, 1))
            else (a, (m, 0))
        else ("", (0, 0))
comp : String -> String -> Order
comp x y =
    case compare (String.length x) (String.length y) of
        LT -> GT
        GT -> LT
        EQ -> if (x < y) then LT else GT
mkStr : (String, (Int, Int)) -> String
mkStr (a, (b, c)) =
    let s = String.repeat b a
    in case c of
        1 -> "1:" ++ s
        2 -> "2:" ++ s
        _ -> "=:" ++ s
mix : String -> String -> String
mix s1 s2 =
    let
        aa = fillAlpha s1
        cc = fillAlpha s2
        ee = List.map2 (\(a1, b1)(a2, b2) -> (a1, (b1, b2))) aa cc
        gg = List.map mkPair ee
        hh = List.filter (\(a, (b, c)) -> (a, (b, c)) /= ("", (b, c)) ) gg
        ii = List.map mkStr hh 
    in List.sortWith comp ii |> String.join "/"
