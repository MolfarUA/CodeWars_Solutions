let averages numbers =
  match numbers with
  | Some xs -> 
    xs |> Seq.map float |> Seq.pairwise |> Seq.map (fun (a,b) -> (a+b)/2.0) |> Seq.toList
  | None -> []
____________________________
let averages (numbers : List<int> option) = 
   match numbers with
     | None -> []
     | Some [] -> []
     | Some [x] -> []
     | Some ls -> [for i in 0 .. ls.Length-2 do yield ((float ls.[i] + float ls.[i+1]) / 2.0) ]
____________________________
let averages = 
    Option.map (Seq.map float >> Seq.windowed 2 >> Seq.map Array.average >> Seq.toList)
    >> Option.defaultValue []
____________________________
let averages = function
| None | Some ([] | [_]) -> []
| Some (_ :: xs' as xs) ->
    xs'
    |> Seq.map2 (fun x x' -> (float x + float x') / 2.) xs
    |> Seq.toList
