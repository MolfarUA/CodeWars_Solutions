5842df8ccbd22792a4000245


function expanded_form(int $n): string {
    $split = str_split($n);
    $num_digits = count($split);
    $numbers_arr = [];
    foreach ($split as $digit) {
        if ($digit != 0) {
            $numbers_arr[] = $digit . str_repeat(0, $num_digits - 1);
        }
        $num_digits--;
    }
    return implode(' + ', $numbers_arr);
}
_________________________
function expanded_form(int $n): string {
  for($i = strlen($n), $a = []; $i > 0;)
  {
    $a[] = $n - ($j = $n % (10 ** (--$i)));
    $n   = $j;
  }
  return implode(' + ', array_filter($a));
}
_________________________
function expanded_form(int $n): string {
  $divisor = 1;
  $str = "";
  
  while ($divisor < $n) {
    $number = intdiv($n, $divisor) % 10 * $divisor;
    $divisor *= 10;
    
    if (! $number) continue;
    
    $str = $number . ' + ' . $str;
  }
  
  return trim($str, ' +');
}
