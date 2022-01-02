function uniqueInOrder($iterable){ 
  $arr = is_string($iterable) ? str_split($iterable) : $iterable;
  $ret = array_reduce($arr, function($carry, $item) {
    if ($item != end($carry)) {
      $carry[] = $item;
    }
    return $carry;
  }, []);
  
  return $ret;
}
_____________________________________________
function uniqueInOrder($values) {
  $unique = [];
  
  if (is_string($values)) {
    $values = str_split($values, 1);
  }
  
  for ($i = 0; $i < count($values); $i++) {
    if ($values[$i] != $values[$i + 1]) {
      $unique[$i] = $values[$i];
    }
  }
  return array_values($unique);
}
_____________________________________________
function uniqueInOrder($i){
  return array_values(array_filter(
      !is_array($i) ? str_split($i) : $i, 
      function($v, $k) use ($i) {return ($v !== $i[$k-1]);}, 1
  ));
}
_____________________________________________
function uniqueInOrder($iterable){
  $iterable = is_array($iterable) ? implode("", $iterable) : $iterable;
  $ret = preg_replace('/(\w{1})\1+/', '$1', $iterable);
  return strlen($ret) ? str_split($ret) : [];
}
