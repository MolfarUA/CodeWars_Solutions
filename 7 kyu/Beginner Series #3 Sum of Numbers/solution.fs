let getSum a b =
    [| min a b .. max a b |] |> Array.sum
    
_______________________________________
let getSum a b =
    match (a, b) with
    | (a, b) when a > b -> [b..a] |> List.sum
    | (a, b) when a < b -> [a..b] |> List.sum
    | _ -> a
    
_______________________________________
let getSum (a: int) (b: int) : int = 
    [ min a b .. max a b ] |> Seq.sum
    
_______________________________________
let getSum a b =
  if a > b then List.sum [b..a] else List.sum [a..b]
  
_______________________________________
let getSum a b = (a + b) * (abs(a - b) + 1) / 2

_______________________________________
let getSum a b = if a = b then a else [min a b .. max a b] |> List.sum
