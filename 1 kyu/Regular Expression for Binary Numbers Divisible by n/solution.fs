open System

let regexDivisibleBy (n : int) : string =
    if (n = 1) then
        "^[01]*$"
    else
        let graphs = Array2D.create n n "-1"
        for i in 0 .. (n - 1) do
             graphs.[i, (2 * i) % n] <- "0"
             graphs.[i, (2 * i + 1) % n] <- "1"
        for k in (n - 1) .. -1 .. 0 do
            let mutable loop = ""
            if (graphs.[k, k] <> "-1") then
                loop <- String.Format("{0}*", graphs.[k, k])
            else
                loop <- loop
            for i in 0 .. (k - 1) do
                if (graphs.[i, k] = "-1") then
                    loop <- loop
                else
                    for j in 0 .. (k - 1) do
                        if (graphs.[k, j] = "-1") then
                            loop <- loop
                        else
                            let mutable s = ""
                            if (graphs.[i, j] <> "-1") then
                                s <- String.Format("{0}|", graphs.[i, j])
                            else
                                s <- s
                            graphs.[i, j] <- String.Format("(?:{0}{1}{2}{3})", s, graphs.[i, k], loop, graphs.[k, j])
        String.Format("^{0}*$", graphs.[0, 0])
___________________________________________________________
type EdgeKey = { source : int; target : int }

type Edge = | NoEdge | Regex of string

let maybeEdgeValue = function | NoEdge -> None | Regex str -> Some str

let initialEdges n =
    [0 .. n-1]
    |> List.collect (
        fun i -> [
            ({ source = i; target = i * 2 % n }, Regex "0");
            ({ source = i; target = (i * 2 + 1) % n }, Regex "1")])
    |> Map.ofList

let mergeEdges sep (edges : Edge list) =
    let es = edges |> List.choose maybeEdgeValue
    if List.length es = 1
    then
        List.head es |> Regex
    else
        es
        |> List.map(fun e -> if e.Contains("|") then sprintf "(?:%s)" e else e)
        |> String.concat sep
        |> Regex

let choiceOfTwoEdges e1 e2 = mergeEdges "|" [e1; e2]

let sequenceOfEdges (edges : Edge list) = mergeEdges "" edges

let edgeValue source target =
    Map.tryFind { source = source; target = target }
    >> Option.defaultValue NoEdge

let removeEdge source target =
    Map.remove { source = source; target = target }

let edgeReducer (edges : Map<EdgeKey, Edge>, this) (prev, next) =
    
    let prevToNext = edges |> edgeValue prev next
    let prevToThis = edges |> edgeValue prev this
    let thisToNext = edges |> edgeValue this next

    let thisLoopEdge =
        match edges |> edgeValue this this with
        | Regex s -> 
            Regex <|
                if s.Length > 1 
                then sprintf "(?:%s)*" s
                else sprintf "%s*" s
        | NoEdge -> NoEdge

    let prevToNextViaThis = sequenceOfEdges [prevToThis; thisLoopEdge; thisToNext]

    let mergedPrevToNextEdge =
        choiceOfTwoEdges prevToNext prevToNextViaThis

    let updatedEdges =
        edges
        |> removeEdge prev next
        |> Map.add { source = prev; target = next } mergedPrevToNextEdge

    (updatedEdges, this)

let nodeReducer edges _ =
    // find least connected node and reduce it
    let this = 
        edges 
        |> Map.toSeq
        |> Seq.map fst
        |> Seq.collect (fun { source = src; target = trg } -> [src; trg])
        |> Seq.filter ((<>) 0)
        |> Seq.countBy id
        |> Seq.sortBy snd
        |> Seq.head
        |> fst

    let keys = edges |> Map.toList |> List.map fst
    let prevs = keys |> List.filter (fun { source = src; target = trg } -> trg = this && src <> this) |> List.map (fun { source = src } -> src)
    let nexts = keys |> List.filter (fun { source = src; target = trg } -> src = this && trg <> this) |> List.map (fun { target = trg } -> trg)

    let updatedEdges =
        [ for prev in prevs do
            for next in nexts do
                yield prev, next ]
        |> List.fold edgeReducer (edges, this)
        |> fst

    // eliminate self-loop and prev and next links to avoid extra calculations
    let reducedEdges = updatedEdges |> removeEdge this this
    let reducedEdges = prevs |> List.fold (fun e prev -> e |> removeEdge prev this) reducedEdges
    let reducedEdges = nexts |> List.fold (fun e next -> e |> removeEdge this next) reducedEdges
    reducedEdges

let regexDivisibleBy (n : int) : string =
    if n = 1
    then
        "^(?:0|1)+$"
    else
        let edges = initialEdges n
        let zeroToZeroEdgeValue = 
            [1 .. n-1]
            |> List.fold nodeReducer edges
            |> Map.find { source = 0; target = 0 }
            |> maybeEdgeValue
            // unsafe get
            |> Option.get
        sprintf @"^(?:%s)+$" zeroToZeroEdgeValue
___________________________________________________________
type state(index :int) =
  member this.index = index
  member val pred :int list = List.empty with get, set
  member val succ :int list = List.empty with get, set

let add (states :state[]) (arches :string[,]) (a :int) (b :int) (s :string) :unit =
  if a <> b then (
    states.[a].succ <- states.[a].succ @ [b]
    states.[b].pred <- states.[b].pred @ [a]
  )
  Array2D.set arches a b s

let delete (state :state) (pred :bool) (index :int) :unit =
  let xs = if pred then state.pred else state.succ
  match List.tryFindIndex ((=) index) xs with
  | Some i ->
    let updated = List.take i xs @ List.skip (i+1) xs
    if pred then state.pred <- updated else state.succ <- updated
  | None -> ()

let init (n :int) :(state[] * string[,]) =
  let n' = n-1
  let arches = Array2D.create n n ""
  let states = [| for i in 0 .. n' -> new state(i) |]
  for i = 0 to n' do
    add states arches i (2 * i % n) "0"
    add states arches i ((2 * i + 1) % n) "1"
  (states, arches)

let join (sep :string) (expr :string list) :string =
  if expr.Length = 1
    then List.exactlyOne expr
    else expr
         |> List.toSeq
         |> Seq.map (fun s -> if Seq.contains '|' s then sprintf "(?:%s)" s else s)
         |> String.concat sep

let reduce (states :state[]) (arches :string[,]) (st :state) :unit =
  let add' (a :string) (b :string) :string =
    (List.filter (fun (s :string) -> 0 < s.Length && s <> "~") >> join "|") [ a; b ]
  for k in st.pred do
    for m in st.succ do
      let q = states.[k]
      let p = states.[m]
      let s' =
        let s = arches.[st.index,st.index]
        match s.Length with
        | 0 -> "~"
        | 1 -> s + "*"
        | _ -> sprintf "(?:%s)*" s
      let ss =
        let args = [ arches.[k,st.index]; s'; arches.[st.index,m] ]
        (
          if List.exists (fun (s :string) -> s.Length = 0) args
            then ""
            else (List.filter ((<>) "~") >> join "") args
        )
      delete q false p.index
      delete p true q.index
      add states arches q.index p.index (add' arches.[k,m] ss)
      delete q false st.index
      delete p true st.index

let regexDivisibleBy (n :int) :string =
  if n = 1 then "^[01]+$" else (
    let (states, arches) = init n
    for s in states.[1..] do
      reduce states arches s
    "^(?:" + arches.[0,0] + ")+$"
  )
