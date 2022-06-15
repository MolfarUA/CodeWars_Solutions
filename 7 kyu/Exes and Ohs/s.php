function XO($s) {
  $lower = strtolower($s);
  return substr_count($lower, 'x') === substr_count($lower, 'o');
}
__________________________________
function XO(string $s):bool {
  $s = strtolower($s);
  return substr_count($s, 'x') == substr_count($s, 'o');
}
__________________________________
function XO($s) {
  $str = strtolower($s);

  $x = substr_count($str, 'x');
  $o = substr_count($str, 'o');

  return $x == $o;
}
__________________________________
function XO($s) {
  $xCount = substr_count(strtolower($s), 'x');
  $oCount = substr_count(strtolower($s), 'o');
  return $xCount === $oCount;
}
__________________________________
function XO($s) {
  $res = array_count_values(str_split(strtolower($s)));
  return $res['x'] == $res['o'] ? true : false;
}
