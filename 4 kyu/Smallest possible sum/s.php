52f677797c461daaf7000740


function gcd(int $a, int $b): int {
  return $b === 0 ? $a : gcd($b, $a % $b);
}
function solution(array $a): int {
  return count($a) * array_reduce($a, gcd, 0);
}
_______________________________
function solution(array $numbers): int
{
    $gcd = array_reduce($numbers, 'gcd');
    return $gcd * count($numbers);
}

// Greatest common divisor
function gcd($a, $b)
{
    while ($b != 0) {
        list($a, $b) = [$b, $a % $b];
    }
    return $a;
}
_______________________________
function gcd($a,$b){ return $a%$b?gcd($b,$a%$b):$b; };
function solution(array $numbers): int {
  return count($numbers)*array_reduce($numbers,"gcd");
}
