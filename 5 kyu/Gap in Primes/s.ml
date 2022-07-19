561e9c843a2ef5a40c0000a4


let is_prime (n : int) : bool =
  let rec aux m =
    m * m > n || (n mod m != 0 && aux (m + 1))
  in
    n >= 2 && aux 2
  ;;
    
let gap (g: int) (m: int) (n: int): (int * int) option =
  let rec loop i a b =
    if i > n then None else
    if b - a == g then Some (a, b) else
    if is_prime i then loop (i + 1) b i else
    loop (i + 1) a b
  in loop m 0 0
  ;;
__________________________________
let is_prime p =
  let rec div_test k n =
    if k > n then true
    else if p mod k = 0 then false
    else div_test (k + 2) n in
  if p = 2 then true
  else if p <= 1 || p mod 2 = 0 then false
  else
    let n = int_of_float (sqrt (float_of_int p)) in
    div_test 3 n
    
let gap (g: int) (m: int) (n: int): (int * int) option =
  let rec loop prev k =
    if k > n then None
    else
      match prev, is_prime k with
      | _, false -> loop prev (k + 1)
      | None, true -> loop (Some k) (k + 1)
      | Some p, true -> 
        if k - p = g then Some (p, k)
        else loop (Some k) (k + 1) in
  loop None m
__________________________________
let rec range (a: int) (b: int): int list =
  if a > b then []
  else a :: range (a+1) b;;
let is_prime n =
  if n = 2 then true
  else if n < 2 || n mod 2 = 0 then false
  else
    let rec loop k =
      if k * k > n then true
      else if n mod k = 0 then false
      else loop (k + 2)
    in loop 3;;
let allp m n =
  List.filter (fun x -> is_prime x) (range m n);;
let rec zip lst1 lst2 = match lst1,lst2 with
  | [],_ -> []
  | _, []-> []
  | (x::xs),(y::ys) -> (x,y) :: (zip xs ys);;

let gap (g: int) (m: int) (n: int): (int * int) option =
  let u = allp m n in
  let z = zip u (List.tl u) in
  let r = List.filter (fun x -> fst x + g = snd x) z in
    if List.length r != 0 then Some(List.hd r)
    else None;;
__________________________________
let gap (g: int) (m: int) (n: int): (int * int) option =
  let is_prime (n : int) : bool =
    let rec aux m =
      m * m > n || (n mod m != 0 && aux (m + 1))
    in
      n >= 2 && aux 2
  in
  
  let rec find_gap prev i =
    if i > n then None
    else
      match prev, is_prime i with
      | _, false -> find_gap prev (i + 1)
      | None, true -> find_gap (Some i) (i + 1)
      | Some p, true ->
        if i - p = g then Some (p, i)
        else find_gap (Some i) (i + 1)
  in
  find_gap None m;;
