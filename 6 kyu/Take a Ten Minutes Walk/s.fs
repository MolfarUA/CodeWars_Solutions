let step (x, y) = function
    | 'n' -> x, y + 1
    | 's' -> x, y - 1
    | 'e' -> x + 1, y
    | 'w' -> x - 1, y
    | _ -> invalidArg "direction" "Must be one of n, s, e, w."

let isValidWalk walk =
    List.length walk = 10 &&
    let origin = (0, 0)
    List.fold step origin walk = origin
__________________________________________
let isValidWalk walk = 
    let getCharCount c = walk |> List.filter(fun x -> x = c) |> List.length   
    if List.length walk <> 10 then false
    elif getCharCount 'n' = getCharCount 's' && getCharCount 'w' = getCharCount 'e' then true 
    else false
__________________________________________
let isValidWalk walk = 
    let n = walk |> List.filter (fun i -> i='n') |> List.length
    let s = walk |> List.filter (fun i -> i='s') |> List.length
    let e = walk |> List.filter (fun i -> i='e') |> List.length
    let w = walk |> List.filter (fun i -> i='w') |> List.length
    n=s && e=w && walk.Length=10
__________________________________________
open FSharp.Collections

let isValidWalk walk =
    let move (x, y, t) = function
        | 'n' -> (x - 1, y, t + 1)
        | 's' -> (x + 1, y, t + 1)
        | 'e' -> (x, y - 1, t + 1)
        | 'w' -> (x, y + 1, t + 1)
        | _ -> (0, 0, 1)
    let isValid = function
        | (0, 0, 10) -> true
        | _ -> false
    isValid <| List.fold move (0, 0, 0) walk
__________________________________________
let isValidWalk walk =
  (walk |> List.length) = 10 && (
    let dir2vec dir =
      match dir with
      | 'n' -> (0,1)
      | 's' -> (0,-1)
      | 'e' -> (1,0)
      | 'w' -> (-1,0)
      | _ -> invalidArg "dir" "dir must be one of ['n';'s';'e';'w']"

    let move pos dir =
      match pos, dir with
      | ((px,py), (dx,dy)) -> (px + dx, py + dy)
  
    (0,0) = (walk |> List.map dir2vec |> List.reduce move))
