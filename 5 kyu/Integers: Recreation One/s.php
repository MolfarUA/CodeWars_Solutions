55aa075506463dac6600010d


function sumSquaredFactors($num) {
    $n_factors = [];
    for ($i = 1; $i <= floor(sqrt($num)); $i++)
      if ($num % $i == 0) {
         array_push($n_factors, $i * $i);
         $c = $num / $i;
         if ($c != $i)
            array_push($n_factors, $c * $c);
      }
   return array_sum($n_factors);
}
function listSquared($m, $n) {
    $res = [];
    for ($i = $m; $i <= $n; $i++) {
        $sm = sumSquaredFactors($i); $rac = (int)sqrt($sm);
        if ($rac * $rac == $sm) {
            array_push($res, [$i, $sm]);
        }
    }
    return $res;
}
________________________________
function listSquared($m, $n) {
  $result = array();
  foreach (range($m, $n) as $p) {
    $divisor_sum = 0;
    for ($i = 1; $i < sqrt($p); $i++)
      if ($p % $i === 0)
        $divisor_sum += $i * $i + intdiv($p, $i) * intdiv($p, $i);
    if (intval(sqrt($p)) * intval(sqrt($p)) === $p)
      $divisor_sum += $p;
    if (intval(sqrt($divisor_sum)) * intval(sqrt($divisor_sum)) === $divisor_sum)
      array_push($result, array($p, $divisor_sum));
  }
  return $result;
}
________________________________
function listSquared($m, $n) {
    $result = [];
    for($divisor = $m; $divisor <= $n; $divisor++){
      $divisors = getDivisors($divisor);
      $num = sumDivisorsSquared($divisors);
      if(isSquared($num)){
          $result[] = [$divisor, $num];
      }
    }
    return $result;
}

function isSquared(int $num) : bool
{
  $num_square = sqrt($num);
  return (round($num_square) == $num_square);
}

function sumDivisorsSquared(array $divisors) : int
{
  $sum_divisors = array_map(function($d){  return pow($d,2); }, $divisors);
  return array_sum($sum_divisors);
}

function getDivisors(int $num_divisor) : array
{
  $num = 0;
  $divisors = [];
  for($i = 1; $i <= sqrt($num_divisor); $i ++) {
      if ($num_divisor % $i == 0) {
        $divisors[] = $i;
        $divisors[] = $num_divisor/$i;
      }
  }
  return array_unique($divisors);
}
