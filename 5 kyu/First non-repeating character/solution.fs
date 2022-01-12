let firstNonRepeatingLetter str =
    str
    |> Seq.groupBy (fun e -> (string e).ToLower())
    |> Seq.tryFind (fun e -> snd e |> Seq.length = 1)
    |> Option.map  (snd >> Seq.head >> string)
    |> Option.defaultValue ""
_______________________________________________
let firstNonRepeatingLetter (str: string) = 
    str
    |> Seq.countBy System.Char.ToLower
    |> Seq.tryPick (fun (key, count) -> if count = 1 then Some (key.ToString()) else None)
    |> Option.defaultValue ""
_______________________________________________
open System

let firstNonRepeatingLetter str =
    let occursOnceInString ch =
        str |> Seq.filter (fun c -> Char.ToLower(c) = Char.ToLower(ch)) |> Seq.length |> (=) 1
    match Seq.tryFind occursOnceInString str with
    | Some s -> string s
    | None -> ""
_______________________________________________
let firstNonRepeatingLetter (str : string) = 
    let s = str.ToLower ()
    s
    |> Seq.tryFindIndex (fun c -> s.IndexOf c = s.LastIndexOf c)
    |> Option.bind (fun i -> Some (string str.[i]))
    |> Option.defaultValue ""
_______________________________________________
let firstNonRepeatingLetter str =
  let counts = Map(Seq.countBy (fun c -> System.Char.ToUpper c) str)
  let maybeChar = Seq.tryFind (fun c -> counts.[System.Char.ToUpper c] = 1) str
  match maybeChar with
  | Some(char) -> System.Char.ToString char
  | None -> ""
