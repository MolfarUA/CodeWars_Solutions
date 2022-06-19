544aed4c4a30184e960010f4


function divisors($integer) {
  $divisors = [];
  for($i = 2; $i < $integer; $i++)
    if(!($integer % $i))
      $divisors[] = $i;
  return $divisors ?: $integer . ' is prime';
}
__________________________________
function divisors($integer) {
    for ($i = 2; $i <= floor($integer / 2); $i++) {
        if ($integer % $i === 0) {
            $numbers[] = $i;
        }
    }
    return empty($numbers) ? $integer . ' is prime' : $numbers;
}
__________________________________
function divisors($integer) {
  $dividers = array_values(array_filter(range(2, $integer-1), function($value) use ($integer) {
      return !($integer % $value);
  }));
  return (empty($dividers) or ($integer === 2 )) ? $integer.' is prime' : $dividers;
}
__________________________________
function divisors(int $i) {
    return array_values(array_filter(range(1, $i-1), fn($x) => $x > 1 && $i % $x === 0)) ?: "{$i} is prime";
}
__________________________________
function divisors(int $integer) { 
  return array_values(array_filter(range(2, $integer), fn ($n) => ($integer % $n == 0 && $n != $integer))) ?: "$integer is prime";
}
