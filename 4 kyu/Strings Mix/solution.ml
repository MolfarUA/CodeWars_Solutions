let mk_pair sndx sndy =
  let m = max sndx sndy in
    if m > 1 then
      if m > sndx then [|m; 2|]
      else if m > sndy  then [|m; 1|]
      else [|m; 0|]
    else [|0;0|];;

let mk_string (a: int * int array): string =
  let c = fst a in
  let rep = (snd a).(0) and sy = (snd a).(1) in
  let sym = 
    if sy = 0 then
      "=:"
    else if sy = 1 then 
      "1:"
    else "2:"
  in
    sym ^ String.make rep (Char.chr c);;

let cmp (x: string) (y: string): int =
  let (c: int) = (String.length y) - (String.length x) in
    if c = 0 then 
      begin
        if x = y then 0
      else if x < y then -1
    else 1
      end
    else c;;

let mix (ss1: string) (ss2: string): string =
  let s1 = Str.split (Str.regexp "") ss1 in
  let s2 = Str.split (Str.regexp "") ss2 in
  let a1 = count_char_984 s1 in
  let a2 = count_char_984 s2 in
  let z = zip_984 a1 a2 in
  let a3 = List.map(fun x -> let a, b = x in (fst a, mk_pair (snd a) (snd b))) z in
  let a4 = List.filter(fun x -> let a, b = x in b.(0) != 0) a3 in
    List.map(fun x -> mk_string x) a4 |> List.sort cmp |> String.concat "/";;
    
_____________________________________________________
let mk_pair sndx sndy =
  let m = max sndx sndy in
    if m > 1 then
      if m > sndx then [|m; 2|]
      else if m > sndy  then [|m; 1|]
      else [|m; 0|]
    else [|0;0|];;

let mk_string (a: int * int array): string =
  let c = fst a in
  let rep = (snd a).(0) and sy = (snd a).(1) in
  let sym = 
    if sy = 0 then
      "=:"
    else if sy = 1 then 
      "1:"
    else "2:"
  in
    sym ^ String.make rep (Char.chr c);;

let cmp (x: string) (y: string): int =
  let (c: int) = (String.length y) - (String.length x) in
    if c = 0 then 
      begin
        if x = y then 0
      else if x < y then -1
    else 1
      end
    else c;;

let mix (ss1: string) (ss2: string): string =
  let s1 = Str.split (Str.regexp "") ss1 in
  let s2 = Str.split (Str.regexp "") ss2 in
  let a1 = count_char_984 s1 in
  let a2 = count_char_984 s2 in
  let z = zip_984 a1 a2 in
  let a3 = List.map(fun x -> let a, b = x in (fst a, mk_pair (snd a) (snd b))) z in
  let a4 = List.filter(fun x -> let a, b = x in b.(0) != 0) a3 in
    List.map(fun x -> mk_string x) a4 |> List.sort cmp |> String.concat "/";;
    
_____________________________________________________
let toInt s = 
  let t = Array.make 26 0 in
  for i=0 to String.length s -1 do
    if int_of_char(s.[i])>96 && int_of_char(s.[i])<123 then 
      (t.(int_of_char(s.[i]) - 97) <- t.(int_of_char(s.[i]) - 97)  +1 ) ; done;
  t;;
  
let texteur c1 c2 i =
  
  let rep = ref "" in
  if c1 > c2 then
    ( rep := (!rep) ^ "1:";
      for j = 1 to c1 do rep:= !rep ^ (String.make 1 (char_of_int(i+97))) ; done
    );
  if c1< c2 then 
    ( rep := (!rep) ^ "2:";
      for j = 1 to c2 do rep:= !rep ^ (String.make 1 (char_of_int(i+97))) ; done
    );
  if c1 = c2 then 
    ( rep := (!rep) ^ "=:";
      for j = 1 to c1 do rep:= !rep ^ (String.make 1 (char_of_int(i+97))) ; done
    );!rep
;;

let op x y= 
  if (String.length x = String.length y)then
    (x<y) 
  else
    String.length x > String.length y
;;

let comparateur t1 t2 =
  let ans = ref [] in
  let temp1 = ref 0 in
  let temp2 = ref 0 in
  for i =0 to 25 do 
    temp1 := t1.(i) ;
    temp2 := t2.(i) ;
    if (!temp1 > 1 || !temp2 > 1 ) then
      
      (ans :=  (texteur !temp1 !temp2 i) :: !ans) ; done;
  !ans ;; 

let rec fission q=match q with
  | [] | [_] -> q, []
  | x::y::p -> let a,b=fission p in x::a, y::b
;;
let rec fusion p1 p2 op=match p1, p2 with
  | [],_ -> p2
  | _, [] -> p1
  | x::q1, y::_ when op x y -> x::(fusion q1 p2 op)
  | _,x::q2 -> x::(fusion p1 q2 op)
;;

let rec tri_fusion p op=match p with
  | [] | [_] -> p
  | _ -> let a,b=fission p in fusion (tri_fusion a op) (tri_fusion b op) op
;;

let toStri t =
  let rec aux t ans = match t with
    |[]-> ""
    |[p] -> ans^p
    |p::q-> aux q (ans^p^"/")
  in
  aux t "";; 

let mix (ss1: string) (ss2: string): string =
  let titi = toInt ss1  in
  let toto = toInt ss2 in
  let test = comparateur titi toto in
  let rep =tri_fusion test op in
  toStri rep
;;
