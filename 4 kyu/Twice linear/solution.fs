open System.Collections.Generic

let dblLinear (n: int) =
    let lst = SortedSet<int>()
    lst.Add(1) |> ignore

    let rec gen (lst : SortedSet<int>) = seq {
       let x = lst.Min;
       
       yield x

       lst.Remove(x) |> ignore
       lst.Add(2 * x + 1) |> ignore
       lst.Add(3 * x + 1) |> ignore

       yield! gen lst
    }
  
    (gen lst) |> Seq.item n
    
__________________________________________________
open System.Collections.Generic

let dblLinear (n: int) =
    let deque2 = new Queue<int>()
    let deque3 = new Queue<int>()
    let mutable cnt = 0
    let mutable h: int = 1
    let mutable cont = true
    while cont do
        if (cnt >= n) then 
            cont <- false
        else
            deque2.Enqueue(2 * h + 1); deque3.Enqueue(3 * h + 1)
            h <- min (deque2.Peek()) (deque3.Peek())
            if (h = deque2.Peek()) then
                deque2.Dequeue() |> ignore
            if (h = deque3.Peek()) then
                deque3.Dequeue() |> ignore
            cnt <- cnt + 1
    h
    
__________________________________________________
open System.Collections.Generic

let dblLinear (n: int) =
    let deque2 = new Queue<int>()
    let deque3 = new Queue<int>()
    let mutable cnt = 0
    let mutable h: int = 1
    let mutable cont = true
    while cont do
        if (cnt >= n) then 
            cont <- false
        else
            deque2.Enqueue(2 * h + 1); deque3.Enqueue(3 * h + 1)
            h <- min (deque2.Peek()) (deque3.Peek())
            if (h = deque2.Peek()) then
                deque2.Dequeue() |> ignore
            if (h = deque3.Peek()) then
                deque3.Dequeue() |> ignore
            cnt <- cnt + 1
    h
    
__________________________________________________
let dblLinear n =
  let rec dblLinearRec n set =
    let m = Set.minElement set
    if n=0 then m
    else dblLinearRec (n-1) (set.Remove(m).Add(m*2+1).Add(m*3+1))
  dblLinearRec n (Set.singleton(1))
