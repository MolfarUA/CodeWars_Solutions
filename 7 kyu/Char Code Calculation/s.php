57f75cc397d62fc93d000059


function calc($s) {
   return substr_count(join(array_map('ord', str_split($s))), '7') * 6;
}
__________________________________
function calc($s) {
  $total1 = implode(array_map(fn(string $s) => ord($s), str_split($s)));
  $total2 = str_replace('7', '1', $total1);
  
  return array_sum(str_split($total1)) - array_sum(str_split($total2));
}
__________________________________
function calc($s) {
  $array   = implode(array_map(function($n){ return ord($n); }, str_split($s)));
  
  $array_n = strtr($array, '7', '1');
  //print_r( array_sum(str_split($array)));
  return array_sum(str_split($array)) - array_sum(str_split($array_n));
}
__________________________________
function calc($s) {
  return array_sum(str_split(join(array_map('ord',str_split($s)))))-array_sum(str_split(str_replace('7','1',join(array_map('ord',str_split($s))))));
}
