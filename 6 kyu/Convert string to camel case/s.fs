let toCamelCase (text : string) =
    text.Split('-', '_')
    |> Seq.mapi (fun i s -> if i > 0 then s.[0..0].ToUpper() + s.[1..] else s)
    |> String.concat ""
________________________
open System

let toCamelCase (text : string) =
  let rec transform (acc: char list) = function
    | '-' :: x :: rest 
    | '_' :: x :: rest -> transform ((Char.ToUpper x) :: acc) rest
    | x :: rest -> transform (x :: acc) rest
    | [] -> acc |> Array.ofList |> Array.rev 

  let chars = text.ToCharArray() |> List.ofArray

  new string(transform [] chars)
________________________
open System.Text.RegularExpressions

let toCamelCase (text : string) =
  let evaluator = MatchEvaluator(fun x -> x.Groups.[1].Value.ToUpper())
  Regex.Replace(text, @"[_-](\w)", evaluator)
________________________
open System

let toCamelCase (text : string) =
    let rec change (condition : char -> bool) list =
        match list with
        | fch :: sch :: rest when condition fch -> Char.ToUpper sch :: change condition rest
        | fch :: rest -> fch :: change condition rest
        | rest -> rest
  
    text
    |> List.ofSeq
    |> change (fun ch -> ch = '_' || ch = '-')
    |> List.toArray
    |> String.Concat
________________________
open System

let capitalizeFirst (str : string) =
    str
    |> Seq.mapi (fun idx c -> if idx = 0 then Char.ToUpper c else c)
    |> String.Concat

let toCamelCase (text : string) =
    text.Split('-', '_')
    |> Seq.mapi (fun idx str -> if idx = 0 then str else capitalizeFirst str)
    |> String.Concat
