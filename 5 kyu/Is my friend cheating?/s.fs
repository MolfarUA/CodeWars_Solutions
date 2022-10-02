5547cc7dcad755e480000004


let removNb n =
    if n <= 3L
    then []
    else
    [
        let sum = n * (n + 1L) / 2L
        for i = n / 2L to n do
            let q, r = System.Math.DivRem(sum - i, i + 1L)
            if r = 0L && q <> i then
                yield i, q
    ]
______________________________
let removNb (n: int64) =
    let sum = n * (n + 1L) / 2L
    
    let numbers = seq {1L..n} |> Seq.filter (fun x -> (sum+1L)%(x+1L) = 0L)
    
    (numbers, numbers)
    ||> Seq.allPairs
    |> Seq.filter (fun (a, b) -> a * b + a + b = sum)
    |> Seq.toList
______________________________
let removNb (n: int64) =
    let rec removNbAux (n: int64) (s: int64) (i: int64) res =
        match i with
        | x when (x > n) -> res
        | _ ->
            let b = s - i
            let m = b / (i + 1L)
            if (b % (i + 1L) = 0L)  then removNbAux n s (i + 1L) (res @ [(i, m)])
            else removNbAux n s (i + 1L) res
    removNbAux n ((n * (n + 1L)) / 2L) (n / 2L) []
