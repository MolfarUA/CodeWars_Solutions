55c6126177c9441a570000cc


function orderWeight($str) {
  $nums = explode(" ", $str);
  
  usort($nums, function ($a, $b) {
    $sumA = array_sum(str_split((string) $a));
    $sumB = array_sum(str_split((string) $b));
    
    if ($sumA === $sumB) return strcmp($a, $b);
    
    return $sumA > $sumB;
  });
  
  
  return implode(' ', $nums);
}
______________________________
function orderWeight($str) {
  $nums = explode(" ", $str);
  usort($nums, function($a, $b) {
    $s = (array_sum(str_split($a)) <=> array_sum(str_split($b)));
    return ($s !== 0) ? $s : strcmp($a, $b);
  });
  return implode(' ', $nums);
}
______________________________
function orderWeight($str) {
  $nums = explode(' ', $str);
  usort($nums, function($a, $b) {return (array_sum(str_split($a)) <=> array_sum(str_split($b))) ?: strcmp($a, $b);});
  return implode(' ', $nums);
}
