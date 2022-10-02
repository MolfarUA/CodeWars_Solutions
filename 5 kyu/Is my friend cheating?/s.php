5547cc7dcad755e480000004


function removeNb($n) {
    $sum = $n * ($n + 1) / 2; $result = array();
    for ($a = 1; $a < $n; $a++) {
        if (($sum - $a) % ($a + 1) == 0) {
            $b = ($sum - $a) / ($a + 1);
            if ($b < $n) {
                array_push($result, array($a, $b));
            }
        }
    }return $result;
}
______________________________
function removeNb($n) {
  $sum = array_sum(range(1, $n));
  $res = [];
  foreach(range(1, $n) as $num){
    $num2 = ($sum - $num) / ($num + 1);
    if(is_int($num2) && $num2 <= $n){
      $res[] = [$num, $num2];
    }
  }
  return $res; 
}
______________________________
function removeNb($n)
{
    $result = [];
    $sum = (1 + $n) * $n / 2;
    for ($a = 1; $a < $n; $a++) {
        $b = ($sum - $a) / ($a + 1);
        if (round($b) == $b && $b <= $n) {
            $result[] = [$a, $b];
        };
    }
    return $result;
}
______________________________
/**
 * f(n) = n(n+1)/2 - a - b - ab = 0 is a two-sheeted hyperboloid.
 * The boundary is at n = (3+sqrt(17))/2.
 * Since n is an integer use ceil((3+sqrt(17))/2) = 4
 */
define('N_BOUNDARY', 4);

/**
 * Get the minimum value of "a" given "n".
 *
 * (n^2-n)/(2(n+1)) <= a <= n
 */
function calculateMinimumA(int $n): int {
  return floor(($n**2 - $n) / (2*$n + 2));
}

/**
 * Get "b" given "a" and "n".
 *
 * g(a,n) = (-2a+n^2+n)/(2(a+1))
 */
function calculateB(int $a, int $n) {
  return (-2*$a + $n**2 + $n) / (2*$a + 2);
}

/**
 * Solve for a and b integer solutions given n:
 *   f(n) = n(n+1)/2 - a - b - ab = 0
 */
function removeNb(int $n): array {
  if ($n <= N_BOUNDARY) {
    return [];
  }

  $solutions = [];
  $lowerA = calculateMinimumA($n);
  for ($ai = $lowerA; $ai <= $n; $ai++) {
    $bi = calculateB($ai, $n);
    if (is_int($bi)) {
      $solutions[] = [$ai, $bi];
    }
  }
  
  return $solutions;
}
