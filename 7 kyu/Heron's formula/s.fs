57aa218e72292d98d500240f


let heron a b c =
    let s = (a + b + c) / 2.
    sqrt <| s * (s - a) * (s - b) * (s - c)
________________________
let heron a b c =
  let s = (a + b + c) / 2.0
  sqrt (s * (s - a) * (s - b) * (s - c))
________________________
let heron (a : float) (b : float) (c : float) : float =
    let s =  (a + b + c) / 2.0
    (s * (s - a) * (s - b) * (s - c)) ** (1.0 / 2.0)
