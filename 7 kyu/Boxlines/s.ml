let f (x: int) (y: int) (z: int): int =
  let sides x y z = x * (y + 1) * (z + 1) in
  (sides x y z) + (sides y z x) + (sides z x y);;
_____________________________________
let f (x: int) (y: int) (z: int): int =
 z*(3*x*y+1+2*(x+y))+2*x*y+x+y
  ;;
_____________________________________
let f (x: int) (y: int) (z: int): int = 3*x*y*z + 2*(x*y + y*z + x*z) + x + y + z
_____________________________________
let f (x: int) (y: int) (z: int): int =
  x * (y + 1) * (z + 1) + (x + 1) * y * (z + 1) + (x + 1) * (y + 1) * z
  ;;
_____________________________________
let f (x: int) (y: int) (z: int): int =
  x * (y + 1) * (z + 1) + y * (z + 1) * (x + 1) + z * (x + 1) * (y + 1)
_____________________________________
let f (x: int) (y: int) (z: int): int = x * (y * (3 * z + 2) + 2 * z + 1) + y * (2 * z + 1) + z
