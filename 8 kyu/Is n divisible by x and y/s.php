5545f109004975ea66000086


function is_divisible(int $n, int $x, int $y): bool {
  return $n % $x == 0 && $n % $y == 0;
}
_____________________
function is_divisible($n, $x, $y) {
  return ($n > 0 && (($n % $x) === 0) && ($n % $y) === 0) ? true : false;
}
_____________________
function is_divisible($n, $x, $y) {
  return $n % $x == 0 and $n % $y == 0 ? true : false;
}
