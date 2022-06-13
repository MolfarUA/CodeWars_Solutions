let createPhoneNumber (n: int list): string =
  sprintf "(%d%d%d) %d%d%d-%d%d%d%d" n.[0] n.[1] n.[2] n.[3] n.[4] n.[5] n.[6] n.[7] n.[8] n.[9]
_______________________________
let createPhoneNumber (numbers: int list) =
  let group i j = numbers.[i..j] |> List.map string |> String.concat ""
  sprintf "(%s) %s-%s" (group 0 2) (group 3 5) (group 6 9)
_______________________________
let createPhoneNumber [a; b; c; d; e; f; g; h; i; j] =
  sprintf "(%d%d%d) %d%d%d-%d%d%d%d" a b c d e f g h i j
_______________________________
let createPhoneNumber numbers =
  numbers
  |> List.mapi (fun i x ->
    match i with
    | 0 -> sprintf "(%i" x
    | 2 -> sprintf "%i) " x
    | 5 -> sprintf "%i-" x
    | _ -> sprintf "%i" x
    )
  |> System.String.Concat
