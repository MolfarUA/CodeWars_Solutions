open System

let mix (s1: string) (s2: string): string =
  
  let filter s n=s  |>List.ofSeq
                    |>Seq.filter(fun x-> System.Char.IsLetter(x))
                    |>Seq.groupBy(fun x -> x.ToString())
                    |>Seq.map(fun (x,y)->(x,y|>Seq.toArray,n))
                    |>Seq.filter(fun (x,y,z)->y.Length>1)
                    |>Seq.toArray
  
  let getCurrentData (data:seq<string*char[]*string>):string*char[]*string =         
         let max=data|>Seq.map(fun (x,y,z)->y.Length)|>Seq.max
         let zt=data|>Seq.filter(fun (x,y,z)->y.Length=max)|>Seq.toArray
         if zt.Length=1 then
             zt.[0]
         else
             zt.[0]|>fun (x,y,z)->(x,y,"=")              
 
  let z1= filter (s1) "1"
  let z2= filter (s2) "2"
  let z3= Array.append z1 z2
          |>Seq.groupBy(fun (x,_,_)->x)
          |>Seq.map(fun (_,y)-> getCurrentData(y))
          |>Seq.distinctBy(fun (x,y,z)->x.ToLowerInvariant())
          |>Seq.sortByDescending(fun(x,y,z)->y.Length)         
          |>Seq.sortBy(fun(x,y,z)->x)         
          
  let result = query {
        for (x,y,z) in z3 do
        sortByDescending y.Length
        thenBy (if z="=" then "z" else z) 
        thenBy x
    }    
  result  |>Seq.map(fun (x,y,z)->x+":"+ (y|>Seq.map(fun g->g.ToString())|>String.concat "") )
          |>Seq.map(fun x->x.ToLowerInvariant())
          |>String.concat ("/")
          
__________________________________________________
open System.Text.RegularExpressions

module String =
    let replace pattern replacement str =
        Regex.Replace(str, pattern = pattern, replacement = replacement)

    let split pattern input = Regex.Split(input, pattern = pattern)

    let toCharArray (string: string) = string.ToCharArray()

type Label = S1|S2|EQ
module Label =
    let toString =
        function
        |S1-> "1"
        |S2-> "2"
        |EQ-> "="

type StringsInfo =
    { Char: char
      Label: Label
      Count: int }
module StringsInfo =
    let toString info =
        sprintf "%s:%s" (Label.toString info.Label)
        <| String.replicate info.Count (string info.Char)


let analyze label str =
    str
    |> String.replace "[^a-z]" ""
    |> String.toCharArray
    |> Array.groupBy id
    |> Array.map
        (fun (char, subs) ->
            { Char = char
              Label = label
              Count = Array.length subs })

let mix (s1: string) (s2: string) : string =
    [ analyze S1 s1; analyze S2 s2 ]
    |> Array.concat
    |> Array.filter (fun s -> s.Count >= 2)
    |> Array.sortBy (fun s -> s.Char)
    |> Array.fold
        (fun acc elem ->
            match elem, acc with
            | _, [] -> [ elem ]
            | { Char = el }, { Char = al } :: _ when el <> al -> [ elem ] @ acc
            | { Count = ec }, { Count = ac } :: _ when ec < ac -> acc
            | { Count = ec }, { Count = ac } :: tail when ec = ac -> [ { elem with Label = EQ } ] @ tail
            | { Count = ec }, { Count = ac } :: tail when ec > ac -> [ elem ] @ tail
            | e -> invalidArg "e" "Invalid pattern")
        []
    |> List.sortBy (fun s -> (- s.Count),s.Label,s.Char)
    |> List.map StringsInfo.toString
    |> String.concat "/"
    
__________________________________________________
open System

type StringDeterminer = | S1 | S2 | E with
    member this.PrettyPrint() =
        match this with
        | S1 -> "1"
        | S2 -> "2"
        | E -> "="

type Candidate = {
    Character: char;
    Frequency: int;
    Determiner: StringDeterminer
} with
    member this.PrettyPrint() =
        sprintf "%s:%s" (this.Determiner.PrettyPrint()) (Seq.replicate this.Frequency this.Character |> String.Concat)

let parse (d: StringDeterminer) (s: string) =
    s.ToCharArray()
    |> Seq.countBy id
    |> Seq.filter (fun (c, n) -> c >= 'a' && c <= 'z' && n > 1)
    |> Seq.map (fun (c, n) -> { Character = c; Frequency = n; Determiner = d} )

let folder (st: Map<char, Candidate>) (item: Candidate) =
    let add c m = Map.add c.Character c m
    let replace c1 c2 m = m |> Map.remove c1.Character |> Map.add c2.Character c2

    match st.TryFind (item.Character) with
    | None -> add item st
    | Some c when c.Frequency < item.Frequency -> replace c item st
    | Some c when c.Frequency = item.Frequency -> replace c { item with Determiner = StringDeterminer.E } st
    | Some _ -> st

let mix (s1: string) (s2: string): string =
    let comparer = (fun (c: Candidate) -> -(c.Frequency), c.Determiner, c.Character)
    
    let state =
        parse StringDeterminer.S1 s1
        |> Seq.map (fun (c: Candidate) -> (c.Character, c))
        |> Map

    Seq.fold folder state (parse StringDeterminer.S2 s2)
    |> Map.toSeq
    |> Seq.map snd
    |> Seq.sortBy comparer
    |> Seq.map (fun c -> c.PrettyPrint())
    |> String.concat "/"

__________________________________________________
open System

let mix (s1: string) (s2: string) : string =
    let counterLowerCaseCharacters = Seq.filter Char.IsLower >> Seq.countBy id >> Map.ofSeq
    let c1, c2 = counterLowerCaseCharacters s1, counterLowerCaseCharacters s2
    let k1 = c1 |> Map.filter (fun _ v -> v > 1) |> Map.toSeq |> Seq.map fst |> Set.ofSeq
    let k2 = c2 |> Map.filter (fun _ v -> v > 1) |> Map.toSeq |> Seq.map fst |> Set.ofSeq
    let tokenGenerator s t =
        if Map.containsKey t c1 && not <| Map.containsKey t c2 then
            Map.add t ('1', Map.find t c1) s
        else if not <| Map.containsKey t c1 && Map.containsKey t c2 then
            Map.add t ('2', Map.find t c2) s
        else
            let token =
                match (Map.find t c1), (Map.find t c2) with
                | n1, n2 when n1 > n2 -> ('1', n1)
                | n1, n2 when n1 < n2 -> ('2', n2)
                | _ -> ('=', Map.find t c1)
            Map.add t token s
    Set.union k1 k2
    |> Seq.fold tokenGenerator Map.empty
    |> Map.toSeq
    |> Seq.sortBy (fun (k, (s, v)) -> -v, s, k)
    |> Seq.map (fun (k, (s, v)) -> sprintf "%c:%s" s (String.replicate v (string k)))
    |> String.concat "/"
