let stockSummary(lstOfArt: string[]) (lstOf1stLetter: string[]): string =
    let format (x,y) =
        "(" + string(x) + " : " + string(y) + ")"
    
    if lstOfArt.Length = 0 || lstOf1stLetter.Length = 0 then 
        ""
    else
        let getBooks c = 
            lstOfArt 
                |> Array.filter(fun x -> x.StartsWith c)
                |> Array.map(fun x -> x.Split(' ').[1] |> int)
                |> Array.sum
        lstOf1stLetter
            |> Array.map (fun x -> format(x, getBooks x))
            |> String.concat " - "
________________________________________
let stockSummary(lstOfArt: string[]) (lstOf1stLetter: string[]): string =
    let (|Art|) (item : string) =
        match item.Split(' ') with
        | [| category; quantity |] -> string category.[0], int quantity
        | _ -> failwith "bad input"
    let art = lstOfArt |> Seq.map (|Art|) |> Seq.cache
    if art |> Seq.isEmpty |> not then
        let sumQuantity code =
            sprintf "(%s : %d)" code (Seq.sumBy (fun (category, quantity) -> if category = code then quantity else 0) art)
        lstOf1stLetter |> Seq.map sumQuantity |> String.concat " - "
    else
        ""
________________________________________
let artToStock (art: string []) (category: string) : int =
    art
    |> Array.filter (fun item -> item.StartsWith(category))
    |> Array.sumBy (fun a -> a.Split(' ').[1] |> int)

let stockSummary (art: string []) (categories: string []) : string =
    match art.Length with
    | 0 -> ""
    | _ ->
        categories
        |> Array.map
            (fun category ->
                "("
                + category
                + " : "
                + (artToStock art category).ToString()
                + ")")
        |> String.concat " - "
________________________________________
open System

let parseStockItem (stockItem : string) =
    let category = string <| stockItem.[0]
    let index = stockItem.IndexOf(' ')
    let quantity = int <| stockItem.Substring(index + 1)
    category, quantity

let formatSummary summary =
    summary
    |> Seq.map (fun (k, v) -> sprintf "(%s : %d)" k v)
    |> String.concat " - "

let stockSummary' stock categories =
    let stockByCategory =
        stock
        |> Seq.map parseStockItem
        |> Seq.groupBy fst
        |> Seq.map (fun (k, vs) -> k, vs |> Seq.sumBy snd)
        |> Map.ofSeq

    let getCategoryItem category =
        let quantity =
            Map.tryFind category stockByCategory
            |> Option.defaultValue 0
        category, quantity

    categories
    |> Seq.map getCategoryItem
    |> formatSummary

let stockSummary stock categories =
    match stock, categories with
    | [||], _
    | _ , [||] -> String.Empty
    | _ -> stockSummary' stock categories
