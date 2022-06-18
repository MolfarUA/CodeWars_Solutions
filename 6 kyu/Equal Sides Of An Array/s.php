function find_even_index($arr){
  $resultIndex = 0;

    for($index = 0; $index < count($arr); $index++){
        $arrLeft = array_slice($arr, 0, $index);
        $arrRight = array_slice($arr, $index+1);

        $arrLeftSum = array_sum($arrLeft);
        $arrRightSum = array_sum($arrRight);

        if($arrLeftSum == $arrRightSum){
            return $index;
        }
    }

    return -1;
}
________________________
function find_even_index($arr){
  foreach($arr as $i => $n) {
    if (array_sum(array_slice($arr, 0, $i)) == array_sum(array_slice($arr, $i+1))) {
      return $i;
    }
  }
  return -1;
}
________________________
function find_even_index($arr){
    $sum_right = array_sum($arr);
    $sum_left = 0;

    foreach($arr as $i=>$a){
        $sum_right-=$a;
        if ($sum_left == $sum_right){
            return $i;
        }
        $sum_left +=$a;
    }
    return -1;
}
________________________
function find_even_index($arr){
  $sum = array_sum($arr);
  $total = 0;
  foreach ($arr as $key => $value) {
    if ($total == $sum - $total - $value)
      return $key;
    $total += $value;
  }
  
  return -1;
}
________________________
function find_even_index($arr){
  $sumLeft = 0;
  $sumRight = array_sum($arr);
  $middle = 0;
  foreach($arr as $index => $value) {
    $sumLeft += $middle;
    $middle = $value;
    $sumRight -= $middle;
    if ($sumLeft == $sumRight) return $index;
  }
  return -1;
}
