55466989aeecab5aac00003e


module Kata exposing (squaresInRect)

squaresInRect : Int -> Int -> Maybe (List Int)
squaresInRect length width =
    if length == width then 
        Nothing
    else 
        Just <| squareHelp length width []

squareHelp length width squares =
    let 
        (smaller, larger) =
            (min length width, max length width)
    in
    if smaller == larger then
        List.reverse (smaller :: squares)
    else
        squareHelp smaller (larger - smaller) (smaller :: squares)
______________________________
module Kata exposing (squaresInRect)

walk : (List Int) -> Int -> Int -> (List Int)
walk arr a b =
  if (min a b) == 0 then (List.reverse arr)
  else walk ((min a b) :: arr) (min a b) ((max a b) - (min a b))

squaresInRect : Int -> Int -> Maybe (List Int)
squaresInRect lng wdth =
  if lng == wdth then Nothing
  else Just (walk [] lng wdth)
______________________________
module Kata exposing (squaresInRect)

squaresInRect : Int -> Int -> Maybe (List Int)
squaresInRect lng wdth =
    let 
        go x y = 
            if x * y == 0 then []
            else let k = min x y in k :: go k (max x y - k)
    in
        if lng == wdth then Nothing
        else Just (go lng wdth)
