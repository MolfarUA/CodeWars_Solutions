// fast permutation snippet
module List =
    let rec permutations = function
        | [] -> seq [List.empty]
        | x :: xs -> Seq.collect (insertions x) (permutations xs)
    and insertions x = function
        | [] -> [[x]]
        | (y :: ys) as xs -> (x::xs)::(List.map (fun x -> y::x) (insertions x ys))

// ---

[<AutoOpen>]
type RowCol = Rows | Cols
    with member x.rotate with get() = if x = Rows then Cols else Rows

let solvePuzzle (clues: int[]) =     
    let size = clues.Length / 4

    let allVs = [1..size] |> List.permutations |> set
    let range = [0..size - 1]

    let rowVs = Array.create size allVs
    let colVs = Array.create size allVs
    let vsMap = [ Rows, rowVs; Cols, colVs ] |> Map.ofList

    let foldedRows = Array.create size (Array.create size (set [1..size]))
    let foldedCols = Array.create size (Array.create size (set [1..size]))
    let foldedMap = [ Rows, foldedRows; Cols, foldedCols ] |> Map.ofList

    let processClues size clues = 
        let clueRanges = [0 .. Array.length clues - 1] |> List.chunkBySize size
        let clue (b, e) = Array.item b clues, Array.item e clues
        List.zip clueRanges.[0] (List.rev clueRanges.[2]) |> List.map clue,
        List.zip (List.rev clueRanges.[3]) clueRanges.[1] |> List.map clue

    let applyClue vs (b, e) =
         let vis = Seq.scan max 0 >> Seq.skip 1 >> Seq.distinct >> Seq.length
         let matching v = (b = 0 || vis v = b) && (e = 0 || vis (Seq.rev v) = e)
         vs |> Set.filter matching

    let col a i = a |> Seq.map (Seq.item i)
    let cols (a: int list seq) = range |> Seq.map (col a)

    let fold = cols >> Seq.map set >> Seq.toArray

    let isFixed a = a |> Set.count <= 1

    let fixedOf = Seq.mapi(fun i v -> i, v) >> Seq.filter( fun (i, v) -> isFixed v)

    let rec fix i rc =
        foldedMap.[rc].[i] <- fold vsMap.[rc].[i]
        for j, x in fixedOf foldedMap.[rc].[i] do
            if not (isFixed foldedMap.[rc.rotate].[j].[i]) then
                vsMap.[rc.rotate].[j] 
                    <- vsMap.[rc.rotate].[j] |> Set.filter (fun v -> x.Contains v.[i])
                fix j rc.rotate

    let intersect i rc =
        vsMap.[rc].[i]
        |> Set.filter( fun v ->
            range 
            |> Seq.forall (fun j -> foldedMap.[rc.rotate].[j].[i].Contains v.[j])
        )

    let rec search vs n =
        let noDupesInColumns = 
            cols vs |> Seq.forall (fun v -> v |> Seq.distinct |> Seq.length = n )
        let columnsMatchClues = 
            cols >> Seq.zip colVs >> Seq.forall( fun (xs, x) -> xs.Contains (List.ofSeq x))
        match noDupesInColumns with
        | true when n = size && columnsMatchClues vs -> Some vs
        | true when n < size -> 
            rowVs |> Array.rev |> Array.item n |> Seq.tryPick (fun v -> search (v::vs) (n + 1))
        | _ -> None

    let colClues, rowClues = processClues size clues

    for i in range do
        rowVs.[i] <- applyClue rowVs.[i] rowClues.[i]
        fix i Rows
        colVs.[i] <- applyClue colVs.[i] colClues.[i]
        fix i Cols

    let rec pass prev =
        for i in range do
            for rc in [Rows; Cols] do
                vsMap.[rc].[i] <- intersect i rc
                fix i rc
        let m  = Seq.append rowVs colVs |> Seq.sumBy Set.count
        if m > size * 2 then
            if m < prev then pass m
            else search [] 0 |> Option.get |> Array.ofList |> Array.map Array.ofList
        else
            rowVs |> Array.map (Set.minElement >> Array.ofList)

    pass (allVs.Count * size * 2)
    
______________________________________________
// fast permutation snippet
module List =
    let rec permutations = function
        | [] -> seq [List.empty]
        | x :: xs -> Seq.collect (insertions x) (permutations xs)
    and insertions x = function
        | [] -> [[x]]
        | (y :: ys) as xs -> (x::xs)::(List.map (fun x -> y::x) (insertions x ys))

// ---

[<AutoOpen>]
type RowCol = Rows | Cols
    with member x.rotate with get() = if x = Rows then Cols else Rows

let solvePuzzle (clues: int[]) =     
    let size = clues.Length / 4

    let allVs = [1..size] |> List.permutations |> set
    let range = [0..size - 1]

    let rowVs = Array.create size allVs
    let colVs = Array.create size allVs
    let vsMap = [ Rows, rowVs; Cols, colVs ] |> Map.ofList

    let foldedRows = Array.create size (Array.create size (set [1..size]))
    let foldedCols = Array.create size (Array.create size (set [1..size]))
    let foldedMap = [ Rows, foldedRows; Cols, foldedCols ] |> Map.ofList

    let processClues size clues = 
        let clueRanges = [0 .. Array.length clues - 1] |> List.chunkBySize size
        let clue (b, e) = Array.item b clues, Array.item e clues
        List.zip clueRanges.[0] (List.rev clueRanges.[2]) |> List.map clue,
        List.zip (List.rev clueRanges.[3]) clueRanges.[1] |> List.map clue

    let applyClue vs (b, e) =
         let vis = Seq.scan max 0 >> Seq.skip 1 >> Seq.distinct >> Seq.length
         let matching v = (b = 0 || vis v = b) && (e = 0 || vis (Seq.rev v) = e)
         vs |> Set.filter matching


    let col a i = a |> Seq.map (Seq.item i)
    let cols a = range |> Seq.map (col a)

    let fold = cols >> Seq.map (Seq.distinct >> set) >> Seq.toArray

    let isFixed a = a |> Set.count <= 1

    let fixedOf = Seq.mapi(fun i v -> i, v) >> Seq.filter( fun (i, v) -> isFixed v)

    let rec fix i rc =
        foldedMap.[rc].[i] <- fold vsMap.[rc].[i]
        for j, x in fixedOf foldedMap.[rc].[i] do
            if not (isFixed foldedMap.[rc.rotate].[j].[i]) then
                vsMap.[rc.rotate].[j] 
                    <- vsMap.[rc.rotate].[j] |> Set.filter (fun v -> x.Contains v.[i])
                fix j rc.rotate

    let intersect i rc =
        vsMap.[rc].[i]
        |> Set.filter( fun v ->
            range 
            |> Seq.forall (fun j -> foldedMap.[rc.rotate].[j].[i].Contains v.[j])
        )

    let rec search vs n =
        let noDupesInColumns = 
            cols vs |> Seq.forall (fun v -> v |> Seq.distinct |> Seq.length = n )
        let columnsMatchClues = 
            cols >> Seq.zip colVs >> Seq.forall( fun (xs, x) -> xs.Contains (List.ofSeq x))
        match noDupesInColumns with
        | true when n = size && columnsMatchClues vs -> Some vs
        | true when n < size -> 
            rowVs |> Array.rev |> Array.item n |> Seq.tryPick (fun v -> search (v::vs) (n + 1))
        | _ -> None

    let colClues, rowClues = processClues size clues

    for i = 0 to size - 1 do
        rowVs.[i] <- applyClue rowVs.[i] rowClues.[i]
        fix i Rows
        colVs.[i] <- applyClue colVs.[i] colClues.[i]
        fix i Cols

    let rec pass prev =
        for i in range do
            for rc in [Rows; Cols] do
                vsMap.[rc].[i] <- intersect i rc
                fix i rc
        let m  = Seq.append rowVs colVs |> Seq.sumBy Set.count
        if m > size * 2 then
            if m < prev then pass m
            else search [] 0 |> Option.get |> Array.ofList |> Array.map Array.ofList
        else
            rowVs |> Array.map (Set.minElement >> Array.ofList)

    pass (allVs.Count * size * 2)
    
____________________________________________
// fast permutation snippet
module List =
    let rec permutations = function
        | [] -> seq [List.empty]
        | x :: xs -> Seq.collect (insertions x) (permutations xs)
    and insertions x = function
        | [] -> [[x]]
        | (y :: ys) as xs -> (x::xs)::(List.map (fun x -> y::x) (insertions x ys))

// ---

[<AutoOpen>]
type RowCol = Rows | Cols
    with member x.rotate with get() = if x = Rows then Cols else Rows

let solvePuzzle (clues: int[]) =     
    let size = clues.Length / 4

    let allVs = [1..size] |> List.permutations |> set
    let range = [0..size - 1]

    let rowVs = Array.create size allVs
    let colVs = Array.create size allVs
    let vsMap = [ Rows, rowVs; Cols, colVs ] |> Map.ofList

    let foldedRows = Array.create size (Array.create size (set [1..size]))
    let foldedCols = Array.create size (Array.create size (set [1..size]))
    let foldedMap = [ Rows, foldedRows; Cols, foldedCols ] |> Map.ofList

    let processClues size clues = 
        let clueRanges = [0 .. Array.length clues - 1] |> List.chunkBySize size
        let clue (b, e) = Array.item b clues, Array.item e clues
        List.zip clueRanges.[0] (List.rev clueRanges.[2]) |> List.map clue,
        List.zip (List.rev clueRanges.[3]) clueRanges.[1] |> List.map clue

    let applyClue vs (b, e) =
         let vis = Seq.scan max 0 >> Seq.skip 1 >> Seq.distinct >> Seq.length
         let matching v = (b = 0 || vis v = b) && (e = 0 || vis (Seq.rev v) = e)
         vs |> Set.filter matching

    let fold vs =
        (Array.create size (set []), vs) 
        ||> Seq.fold ( fun s v ->
            v |> List.iteri (fun i x -> s.[i] <- s.[i].Add x)
            s
        )

    let isFixed a = a |> Set.count <= 1

    let fixedOf (a: _[]) =
        set [ for i = 0 to size - 1 do if isFixed a.[i] then yield i, a.[i] ]

    let rec fix i rc =
        foldedMap.[rc].[i] <- fold vsMap.[rc].[i]
        for j, x in fixedOf foldedMap.[rc].[i] do
            if not (isFixed foldedMap.[rc.rotate].[j].[i]) then
                vsMap.[rc.rotate].[j] <- vsMap.[rc.rotate].[j] |> Set.filter (fun v -> x.Contains v.[i])
                fix j rc.rotate

    let intersect i rc =
        vsMap.[rc].[i]
        |> Set.filter( fun v ->
            range 
            |> Seq.forall (fun j -> foldedMap.[rc.rotate].[j].[i].Contains v.[j])
        )

    let rec search vs n =
        let good = range |> Seq.forall (fun i -> 
                vs |> List.map (List.item i) |> List.distinct |> List.length = n)
        match good with
        | true when n = size -> Some vs
        | true -> rowVs |> Array.rev |> Array.item n |> Seq.tryPick (fun v -> search (v::vs) (n + 1))
        | _ -> None

    let colClues, rowClues = processClues size clues

    for i = 0 to size - 1 do
        rowVs.[i] <- applyClue rowVs.[i] rowClues.[i]
        fix i Rows
        colVs.[i] <- applyClue colVs.[i] colClues.[i]
        fix i Cols

    let rec pass prev =
        for i in range do
            for rc in [Rows; Cols] do
                vsMap.[rc].[i] <- intersect i rc
                fix i rc
        let m  = Seq.append rowVs colVs |> Seq.sumBy Set.count
        if m > size * 2 then
            if m < prev then pass m
            else search [] 0 |> Option.get |> Array.ofList |> Array.map Array.ofList
        else
            rowVs |> Array.map (Set.minElement >> Array.ofList)

    pass (allVs.Count * size * 2)
    
____________________________________________
let rec permutations = function
   | []      -> seq [List.empty]
   | x :: xs -> Seq.collect (insertions x) (permutations xs)
and insertions x = function
   | []             -> [[x]]
   | (y :: ys) as xs -> (x::xs)::(List.map (fun x -> y::x) (insertions x ys))

let permutes numSkyscrapersPerLine = (permutations [1..numSkyscrapersPerLine]) |> Seq.map (fun x -> List.toArray x) |> Seq.toArray

let skycrapersSeen ls =
    ls
    |> Array.fold (fun (numSeen, biggestSeen) skyscraper -> 
        if skyscraper > biggestSeen then (numSeen + 1, skyscraper) else (numSeen, biggestSeen)) (0,0)
    |> fst

let allSkyscraperPermutations numSkyscrapersPerLine numberToSee =
    permutes numSkyscrapersPerLine
    |> Array.filter (skycrapersSeen >> ((=) numberToSee))

let equals (ls : int[]) (ls2: int[]) =
    let mutable count = 0
    while (count < Array.length ls && ls.[count] = ls2.[count]) do
        count <- count + 1
    count = Array.length ls

let applyAt i array func =
    array |> Array.mapi (fun j element -> if i = j then func element else element)

let union ls ls2 =
    ls
    |> Array.filter (fun element -> (ls2 |> Array.exists (fun element2 -> equals element element2)))

let applyClue numSkyscrapersPerLine (clue : int) (shouldReverse : bool) (current : int[][]) =
    if (clue = 0) then
        current
    else
        let allowedPosibilities =
            match shouldReverse with
            | true -> allSkyscraperPermutations numSkyscrapersPerLine clue |> Array.map Array.rev
            | false -> allSkyscraperPermutations numSkyscrapersPerLine clue
        union allowedPosibilities current

let applyClueOnRow num numSkyscrapersPerLine clue shouldReverse i (rows, columns) = 
    let newRows = applyAt i rows (applyClue numSkyscrapersPerLine clue shouldReverse)
    (newRows, columns)

let applyClueOnColumn num numSkyscrapersPerLine clue shouldReverse i (rows, columns) = 
    let newColumns = applyAt i columns (applyClue numSkyscrapersPerLine clue shouldReverse)
    (rows, newColumns)

let applyClueIndex numSkyscrapersPerLine rowsAndColumns (clueIndex, clue) =
    match clueIndex with
    | c when numSkyscrapersPerLine * 0 <= c && c < numSkyscrapersPerLine * 1 -> applyClueOnColumn false numSkyscrapersPerLine clue false c rowsAndColumns
    | c when numSkyscrapersPerLine * 1 <= c && c < numSkyscrapersPerLine * 2 -> applyClueOnRow false numSkyscrapersPerLine clue true (c - numSkyscrapersPerLine) rowsAndColumns
    | c when numSkyscrapersPerLine * 2 <= c && c < numSkyscrapersPerLine * 3 -> applyClueOnColumn false numSkyscrapersPerLine clue true (abs (c - numSkyscrapersPerLine * 3) - 1) rowsAndColumns
    | c when numSkyscrapersPerLine * 3 <= c && c < numSkyscrapersPerLine * 4 -> applyClueOnRow false numSkyscrapersPerLine clue false (abs (c - numSkyscrapersPerLine * 4) - 1) rowsAndColumns
    | _ -> invalidArg "clueIndex" (sprintf "Incorrent clue index: %d" clueIndex)

let applyClues numSkyscrapersPerLine (clues : int []) (rowsAndColumns : int [][][] * int [][][]) : int [][][] * int [][][] =
    clues
    |> Array.mapi (fun i x -> (i, x))
    |> Array.rev
    |> Array.fold (applyClueIndex numSkyscrapersPerLine) rowsAndColumns

let removeSubArraysMatchingElementsAt i illigalElements (array : int[][]) = 
    array |> Array.filter (fun possibility -> not (illigalElements |> Set.contains possibility.[i]))

let getDistinctPosibilities i j (array : int [][][]) =
    array.[i] |> Array.map (fun array -> array.[j]) |> Array.distinct

let removeSkypscraperUnionRowAndColumn (rows : int [][][], columns : int [][][]) (i, j) = 
    let skyscraperPosibilitiesFromRow = getDistinctPosibilities i j rows// rows.[i] |> Array.map (fun row -> row.[j]) |> Array.distinct
    let skyscraperPosibilitiesFromColumn =  getDistinctPosibilities j i columns//columns.[j] |> Array.map (fun column -> column.[i]) |> Array.distinct
    let removeSkyscrapersFromRow = Set.ofArray skyscraperPosibilitiesFromRow - (Set.ofArray skyscraperPosibilitiesFromColumn)
    let removeSkyscrapersFromColumn = Set.ofArray skyscraperPosibilitiesFromColumn - (Set.ofArray skyscraperPosibilitiesFromRow)
    let updatedColumns = applyAt j columns (removeSubArraysMatchingElementsAt i removeSkyscrapersFromColumn)
    let updatedRows = applyAt i rows (removeSubArraysMatchingElementsAt j removeSkyscrapersFromRow)
    (updatedRows, updatedColumns)

let removeSkyscrapersUnionAllRowsAndColumns numSkyscrapersPerLine rowsAndColumns = 
    [|0..numSkyscrapersPerLine - 1|]
    |> Array.map (fun i -> [|0..numSkyscrapersPerLine - 1|]
                           |> Array.map (fun j -> (i, j)))
    |> Array.concat
    |> Array.fold (removeSkypscraperUnionRowAndColumn) rowsAndColumns

let isSolved (rows, _) = 
    rows
    |> Array.map (fun row -> Seq.length row = 1)
    |> Array.reduce (&&)

let hasSameNumberOfPossibilities (rows, columns) (updatedRows, updatedColumns) =
    rows
    |> Array.map2 (fun arr arr2 -> Array.length arr = Array.length arr2) updatedRows
    |> Array.reduce (&&)
    &&
    columns
    |> Array.map2 (fun arr arr2 -> Array.length arr = Array.length arr2) updatedColumns
    |> Array.reduce (&&)

let rec applyUnionRule numSkyscrapersPerLine rowsAndColumns = 
    match isSolved rowsAndColumns with
    | true -> rowsAndColumns
    | false -> 
        let updatedRowsAndColumns = (removeSkyscrapersUnionAllRowsAndColumns numSkyscrapersPerLine rowsAndColumns)
        match hasSameNumberOfPossibilities rowsAndColumns updatedRowsAndColumns with
        | true -> updatedRowsAndColumns
        | false -> applyUnionRule numSkyscrapersPerLine updatedRowsAndColumns

let rec findFieldWithMoreOptions i j rows =
    let distinctPosibilities = getDistinctPosibilities i j rows
    let numPosibilities = Array.length distinctPosibilities
    match numPosibilities with
    | 1 -> findFieldWithMoreOptions i (j + 1) rows
    | _ -> ((i, j), distinctPosibilities)

let setFieldInRow i j value (rows : int[][][])  = 
    applyAt i rows (fun row -> row |> Array.filter (fun option -> option.[j] = value))

let hasNoSolution (rows : int[][][], _) =
    rows.[0] |> Array.isEmpty

let rec guess numSkyscrapersPerLine i j (possibilities : int []) pos (row, column) = 
    let updatedRow = setFieldInRow i j possibilities.[pos] row
    let updatedRC = removeSkyscrapersUnionAllRowsAndColumns numSkyscrapersPerLine (applyUnionRule numSkyscrapersPerLine (updatedRow, column))
    match hasNoSolution updatedRC with
    | true  -> guess numSkyscrapersPerLine i j possibilities (pos + 1) (row, column)
    | false -> updatedRC

let rec guessing numSkyscrapersPerLine (row, column) = 
    let ((i, j), possibilities) = findFieldWithMoreOptions 0 0 row
    let updatedRC = guess numSkyscrapersPerLine i j possibilities 0 (row, column)
    match isSolved updatedRC with
    | true  -> updatedRC
    | false -> guessing numSkyscrapersPerLine updatedRC

let solvePuzzle (clues : int[]) =
    let numSkyscrapersPerLine = 7
    let rowsAllPosibilities = [|1..numSkyscrapersPerLine|] |> Array.map (fun _ -> permutes numSkyscrapersPerLine)
    let columnsAllPosibilities = [|1..numSkyscrapersPerLine|] |> Array.map (fun _ -> permutes numSkyscrapersPerLine)

    let cluesApplied = applyClues numSkyscrapersPerLine clues (rowsAllPosibilities, columnsAllPosibilities)

    let unionApplied = applyUnionRule numSkyscrapersPerLine cluesApplied

    let (finalRows, _) =
        match isSolved unionApplied with
        | true -> unionApplied
        | false -> guessing numSkyscrapersPerLine unionApplied
    finalRows |> Array.concat
    
____________________________________________
// This solution is quite different and more correct than one that passes 4x4 and 6x6
// It can solve puzzle where guessing is inevitable (MedVed test)
// and is also relies on Arrays rather than List and Seq to squeeze extra performance and pass the tests suite

let N = 7

let rec combinations acc fits range remains = seq {
    if remains = 0
    then yield acc
    else
        for candidate in range do
            if fits acc candidate
            then yield! combinations (candidate :: acc) fits range (remains - 1) }

let permutations =
    combinations [] (fun acc x -> acc |> List.forall ((<>) x)) [1 .. N] N
    |> Seq.map Array.ofList
    |> Array.ofSeq

let visibleCount =
    fst << Seq.fold (fun (count, lastMax) cur -> if cur > lastMax then (count + 1, cur) else (count, lastMax)) (0, 0)

let optionsByVisibleCount : Map<int, int[][]> =
    let ps = permutations
    ps
    |> Array.groupBy visibleCount
    |> Seq.append [| (0, ps) |] // all permutations for zero clue
    |> Map.ofSeq

let optionsToMask (options : int[][]) =
    [| 0 .. N - 1 |]
    |> Array.map ((fun i -> options |> Seq.map (fun opt -> opt.[i])) >> Set.ofSeq)

let indexed field = 
    [
        for y in 0 .. (Array2D.length1 field) - 1 do
            for x in 0 .. (Array2D.length2 field) - 1 do
                yield y, x, field.[y, x]
    ]

let isSolved = indexed >> List.forall(fun (_, _, vs) -> (Set.count vs) = 1)

let rec refine recLevel (clues : int[]) lastField =

    // some local statefulness
    let currentField = Array2D.copy lastField

    let refineFieldSlice clueIdx (y0, x0) (dy, dx) =
        let optionFitsFieldSlice =
            Array.mapi (fun i v -> currentField.[y0 + i * dy, x0 + i * dx] |> Set.contains v)
            >> Array.forall id          
        let refinedSlice =
          optionsByVisibleCount
          |> Map.find clues.[clueIdx]
          |> Array.filter optionFitsFieldSlice
          |> optionsToMask         
        // set new mask
        refinedSlice |>
        Array.iteri(fun i m -> currentField.[y0 + i * dy, x0 + i * dx] <- m)

    for i in 0 .. N-1 do
        refineFieldSlice i (0, i) (1, 0)     
        refineFieldSlice (i + N) (i, N-1) (0, -1)
        refineFieldSlice (i + 2*N) (N-1, N-1-i) (-1, 0)
        refineFieldSlice (i + 3*N) (N-1-i, 0) (0, 1)
    
    if currentField <> lastField
    then
        // something refined, carry on...
        refine (recLevel + 1) clues currentField
    else
        // nothing refined, check if already solved
        if isSolved currentField
        then
            // solved
            currentField
        else
            // not solved
            let maybeSolution =
                // take first uncertain cell, with minimum count of options (usually 2 by this time)
                let (y, x, vs) =
                    currentField |> indexed
                    |> Seq.filter (fun (_, _, vs) -> (Set.count vs) <> 1)
                    |> Seq.sortBy (fun (_, _, vs) -> Set.count vs)
                    |> Seq.head

                // in this uncertain cell, knock every option one by one...
                vs
                |> Seq.map (
                    fun knock ->
                        let currentFieldCopy = Array2D.copy currentField
                        currentFieldCopy.[y, x] <- Set.remove knock vs
                        refine (recLevel + 1) clues currentFieldCopy)
                // ... until puzzle solved or options exhausted
                |> Seq.filter isSolved |> Seq.tryHead

            match maybeSolution with
            | Some s -> s
            // if all options exhausted - fall back to previous field
            | None -> currentField

let solveRaw (clues : int[]) =
    List.replicate N (Set.ofList [1 .. N] |> List.replicate N) |> array2D
    |> refine 0 clues

let solvePuzzle (clues : int[]) : int[][] =   
    // start guessing with full uncertainty
    let initialGuess = List.replicate N (Set.ofList [1 .. N] |> List.replicate N) |> array2D
    let solution = 
        initialGuess
        |> refine 0 clues 
        |> Array2D.map Seq.exactlyOne       
    // convert to jagged array to satisfy test suite
    [| for i in 0 .. (Array2D.length1 solution) - 1 do yield solution.[i, *] |]
