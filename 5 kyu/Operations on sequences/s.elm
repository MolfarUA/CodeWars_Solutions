module Kata exposing (solve)

import List.Extra

getList nth list =
    list |> List.drop (nth - 1) |> List.head |> Maybe.withDefault 0
solve : List Int -> (Int, Int)
solve a =
    let
        (xx, yy) = List.Extra.splitAt 4 a
        a0 = getList 1 xx
        a1 = getList 2 xx
        a2 = getList 3 xx
        a3 = getList 4 xx
        t1 = abs(a0 * a2 - a1 * a3)
        t2 = abs(a0 * a3 + a1 * a2)
    in
        if List.length a == 4 then (t1, t2)
        else solve(t1 :: t2 :: yy)
