55466989aeecab5aac00003e


let squaresInRect lng wdth =
    let rec loop x y =
        if (x * y = 0) then []
        else 
            let k = min x y
            let mx = max x y
            k :: (loop k (mx - k))
    if (lng = wdth) then None
    else Some(loop lng wdth) 
______________________________
let squaresInRect lng wdth =
    let rec loop x y =
        if (x * y = 0) then []
        else 
            let k = min x y
            let mx = max x y
            k :: (loop k (mx - k))
    if (lng = wdth) then None
    else Some(loop lng wdth) 
______________________________
let squaresInRect length width =
    let rec realSquaresInRect (length:int) (width:int) : int list =
        if length < width then realSquaresInRect width length
        elif length % width = 0 then List.init (length/width) (fun _ -> width)
        else width :: realSquaresInRect width (length-width)
    if length <> width then Some(realSquaresInRect length width) else None
