open System

let iterPi epsilon = 

    let myPi, _, iterations = Seq.initInfinite(fun idx -> idx + 1)
                              |> Seq.map(fun idx -> (idx * 2) - 1)
                              |> Seq.scan(fun (pi, sign, _) idx -> 
                                    (pi + sign * (1. / float(idx)), sign * -1., idx)) (0., 1., 0)
                              |> Seq.skipWhile(fun (pi, _, idx) -> Math.Abs(Math.PI - (pi*4.)) >= epsilon)
                              |> Seq.take 1
                              |> Seq.head
    ((iterations + 1) / 2, myPi * 4.)
________________________________________
open System

let iterPi epsilon =
    let rec piExpansion (idx:int) (s:int) (t:double) = seq {
        let t_new = t + 4.0 / (double (idx * 2 - 1) * double s)
        yield (idx, t_new)
        yield! piExpansion (idx+1) -s t_new
    }
    piExpansion 1 1 0.0 |> Seq.skipWhile (fun (_, x) -> Math.Abs(x - Math.PI) >= epsilon) |> Seq.head
________________________________________
let iterPi epsilon =
  let mutable pi, n, sgn, i  =  1.0,  3.0,  1.,  1
  let a, b  =  (System.Math.PI - epsilon)/4. , (System.Math.PI + epsilon)/4.
  while not (a < pi && pi < b) do
      sgn <- sgn * -1.
      pi  <- pi + sgn / n
      n   <- n+2.
      i   <- i+1
  (i, pi*4.)
________________________________________
let PI = System.Math.PI
let iterPi epsilon =

    let mutable pi = 4.0
    let mutable i = 3.0
    let mutable sign = -4.0
    while abs (PI - pi) > epsilon do
        pi <- pi + sign / i
        sign <- -sign
        i <- i + 2.0
    
    (int i / 2, pi)
________________________________________
open System

let iterPi epsilon = 
    let trunc10Dble (d: double) = double(uint64(d * 1e10)) * 1e-10
    let rec loop (i: int) (value: double) =
        if (abs (Math.PI - value) <= epsilon) then (i, trunc10Dble value)
        else
            loop (i + 1) (value + 4.0 * Math.Pow(-1.0, double(i)) / (2.0 * double(i) + 1.0))
    loop 1 4.0
________________________________________
let iterPi e =
    let generate (v, n, s) = Some((n, v), ((v + 4.0 * s / (1.0 + 2.0 * float n)), (n + 1), (-s)))
    let closeEnough (n, v) = abs (System.Math.PI - v) < e
    Seq.unfold generate (0.0, 0, 1.0) |> Seq.find closeEnough
