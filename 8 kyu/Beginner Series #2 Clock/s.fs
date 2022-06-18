55f9bca8ecaa9eac7100004a


let past h m s = 
  (h * 60 * 60 + m * 60 + s) * 1000
__________________________
let past h m s = 
     h 
     |> (*) 60
     |> (+) m
     |> (*) 60
     |> (+) s
     |> (*) 1000
__________________________
let hourToMinutes x = x * 60
let minutesToSeconds x y = (x + y) * 60
let secondsToMilli x y = (x + y) * 1000

let past h m s = 
    hourToMinutes h |> minutesToSeconds m |> secondsToMilli s
__________________________
let past h m s = 
    let total = [|h*60*60*1000 ; m * 60 * 1000 ; s *1000|]
    let result = 
      total
      |> Array.sum
    result
__________________________
let past h m s = 
    1000*(h*60*60 + m*60 + s)
__________________________
let past h m s = s * 1000 + m * 60000 + h * 60 * 60000
__________________________
let past h m s = 
  let result = 3600000 * h + 60000 * m + 1000 * s
  result
