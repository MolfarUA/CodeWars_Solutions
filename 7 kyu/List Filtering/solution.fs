let GetIntegersFromList (xs : obj list) = xs |> List.choose tryUnbox<int>

_____________________________________________
open System
let GetIntegersFromList : (obj list -> int list) =
  List.filter (function | :? int as n -> true | _ -> false) >> List.map unbox

_____________________________________________
open System
let GetIntegersFromList = List.filter (fun (x: obj) -> x :? int) >> List.map (fun x -> x :?> int)

_____________________________________________
open System
let GetIntegersFromList (listOfItems: Object list):int list=
  let isInt x = box x :? int
  listOfItems |> List.filter isInt 
              |> List.map (fun x -> x :?> int)
              
_____________________________________________
let GetIntegersFromList (listOfItems: obj list) =
    [for item in listOfItems do if item :? int then yield item :?> int]
