let scoreItem count faceValue =
    match faceValue, count with
    | 1, c -> 1000 * (c / 3) + 100 * (c % 3)
    | 5, c -> 500 * (c / 3) + 50 * (c % 3)
    | _, c -> 100 * faceValue * (c / 3)

let score dice =
    dice
    |> Seq.countBy id
    |> Seq.map (fun (faceValue, count) -> scoreItem count faceValue)
    |> Seq.sum
_____________________________________________
type Multiple = | Single | Tripple

let scorer = function
    | Tripple, 1 -> 1000
    | Tripple, faceValue -> faceValue * 100
    | Single, 1 -> 100
    | Single, 5 -> 50
    | _ -> 0

let decompose ((number, count): int * int) =
    let trippleCount, singleCount = count / 3, count % 3

    [ trippleCount * (scorer (Tripple, number))
      singleCount * (scorer (Single, number)) ] |> List.sum

let score = List.countBy id >> List.sumBy decompose
_____________________________________________
let scores =
  [| 1000, 100
     200, 0
     300, 0
     400, 0
     500, 50
     600, 0 |]

let sideScore i s =
  let (three, one) = scores.[i]
  (s / 3 * three) + (s % 3 * one)

let score dice =
  let sides = Array.create 6 0

  for d in dice do
    sides.[d - 1] <- sides.[d - 1] + 1

  sides
  |> Array.mapi sideScore
  |> Array.sum
_____________________________________________
let rec scoring (a,b) =
    match a with 
    | 1 when b >= 3 -> 1000 + scoring (a, b-3)
    | 1 when b >= 1 -> 100 + scoring (a,b-1)
    | 5 when b >= 3 -> 500 + scoring (a,b-3) 
    | 5 when b >= 1 -> 50 + scoring (a,b-1) 
    | _ when b >= 3 -> a * 100
    | _ -> 0

let score = List.countBy id >> List.sumBy scoring
_____________________________________________
let score dice =
    List.sort dice
    |> List.unfold
        (function
        | 1 :: 1 :: 1 :: tail -> Some(1000, tail)
        | 6 :: 6 :: 6 :: tail -> Some(600, tail)
        | 5 :: 5 :: 5 :: tail -> Some(500, tail)
        | 4 :: 4 :: 4 :: tail -> Some(400, tail)
        | 3 :: 3 :: 3 :: tail -> Some(300, tail)
        | 2 :: 2 :: 2 :: tail -> Some(200, tail)
        | 1 :: tail -> Some(100, tail)
        | 5 :: tail -> Some(50, tail)
        | _ :: tail -> Some(0, tail)
        | [] -> None)
    |> List.sum
_____________________________________________
let score dice =
    let score' sum (faces: int * int list) : int =
        match faces with
        | (1, xs) when xs.Length >= 3 -> sum + 1000 + 100 * (xs.Length - 3)
        | (6, xs) when xs.Length >= 3 -> sum + 600
        | (5, xs) when xs.Length >= 3 -> sum + 500 + 50 * (xs.Length - 3)
        | (4, xs) when xs.Length >= 3 -> sum + 400
        | (3, xs) when xs.Length >= 3 -> sum + 300
        | (2, xs) when xs.Length >= 3 -> sum + 200
        | (1, xs)                     -> sum + 100 * xs.Length
        | (5, xs)                     -> sum + 50 * xs.Length
        | _                           -> sum
    
    dice |> List.groupBy id |> List.fold score' 0
