function sortArray(array $arr) : array {
  $odds = array_filter($arr, function ($n) { return $n % 2 != 0; });
  sort($odds);
  return array_map(function ($n) use (&$odds) {
    if ($n % 2 == 0) return $n;
    return array_shift($odds);
  }, $arr);
}
_______________________________________________
function sortArray(array $arr) : array {
  $even = $odd = array();
  
  foreach($arr as $a){
    if($a % 2 == 0){
      $even[] = $a;
    }else{
      $odd[] = $a;
    }
  }
  sort($odd);
  
  $newArr = [];
  for($i = 0; $i < count($arr); $i++){
    if($arr[$i] % 2 == 0){
      $newArr[] = array_shift($even);
    }else{
      $newArr[] = array_shift($odd);
    }
  }
  return $newArr;
}
_______________________________________________
function sortArray(array $arr) : array {
    $odds = array_filter($arr, function($n){ return $n%2!=0;});
    sort($odds);
    for ($i=0; $i < count($arr); $i++) { 
        $arr[$i] = ($arr[$i]%2==0) ? $arr[$i]: array_shift($odds);
    }
    return $arr;
}
_______________________________________________
function sortArray(array $arr) : array {
  $o = array_filter($arr, function($x){return $x & 1;});
  sort($o);

  for ($i=0; $i<count($arr); $i++) {
    if ($arr[$i] & 1) {
      $arr[$i]=array_shift($o);
    }
  }
  
  return $arr;
}
_______________________________________________
function sortArray(array $arr) : array {
  if(count($arr)==0){
    return array();
  }
  $tmp = $arr[0];
    for($i=0; $i<count($arr);$i++){
        if($arr[$i]%2!=0){
            for ($x=$i; $x < count($arr); $x++) { 
                 if ($arr[$i]>$arr[$x] AND $arr[$x]%2!=0) {
                    $tmp = $arr[$x];
                    $arr[$x] = $arr[$i];
                    $arr[$i] = $tmp;  
                 }else{
             }
             }    
        }
    }
    return $arr;      
}
