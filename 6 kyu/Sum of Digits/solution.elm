module Kata exposing (digitalRoot)

digitalRoot : Int -> Int
digitalRoot n = remainderBy 9 (n - 1) + 1

________________________________
module Kata exposing (digitalRoot)


digitalRoot : Int -> Int
digitalRoot input =
  let
    sum =
      input
        |> digits
        |> List.sum
  in
  if sum > 9 then
    digitalRoot sum
  else
    sum


digits : Int -> List Int
digits =
  String.fromInt
    >> String.split ""
    >> List.filterMap String.toInt
    
________________________________
module Kata exposing (digitalRoot)


digitalRoot : Int -> Int
digitalRoot input = 
    if input < 10 then
        input
    else
        input
            |> String.fromInt
            |> String.split ""
            |> List.map (String.toInt >> Maybe.withDefault 0)
            |> List.sum
            |> digitalRoot
            
________________________________
module Kata exposing (digitalRoot)


digitalRoot : Int -> Int
digitalRoot input = 
  if input < 10 then
    input
  else
    digitalRoot (modBy 10 input + digitalRoot (input // 10))
    
