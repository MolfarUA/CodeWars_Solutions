566fc12495810954b1000030


function nbDig(int $n, int $d) : int {
    $count = 0;
    for ($i = 0; $i <= $n; $i++) {
        $count += substr_count((string)(pow($i, 2)), (string)$d);
    }
    return $count;
}
____________________________
function nbDig($n, $d) {
  $string = "";
  for ($x=0; $x <= $n; $string .= ($x++)**2);
  return substr_count($string,$d);
}
____________________________
function nbDig($n, $d): int {
  return substr_count(implode('', array_map(function($num){return $num**2;},range(0, $n))), $d);
}
