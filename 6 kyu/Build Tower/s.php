576757b1df89ecf5bd00073b


function tower_builder(int $n): array {
    $pad = $n * 2 - 1;
    $x = 1;
    
    $arr = [];
    while ($n --> 0) {
        $arr[] = str_pad(str_repeat('*', $x), $pad, ' ', STR_PAD_BOTH);
        $x += 2;
    }
   
    return $arr;
}
_____________________________
function tower_builder(int $n): array {
  $result = array();
  for($i=1; $i<=$n; $i++) {
    $result[] = str_repeat(' ', $n-$i) . str_repeat('*', ($i-1)*2+1) . str_repeat(' ', $n-$i);
  }
  return $result;
}
_____________________________
function tower_builder(int $n): array {
  $arr = [];
  $all=1;
  for ($i = 0; $i < $n; $i++) {
    $all += 2;
  }
  for($count = 1, $i = 0; $i<$n ; $i++, $count += 2) {
    $check = $count;
    $arr[$i] = '';
  while ($check > 0) {
    $arr[$i] .= '*';
    $check--;
    }
    $arr[$i] = str_pad($arr[$i], $all-2, " ", STR_PAD_BOTH); 
  }

  return $arr;
    return str_split((string) $n);
}
_____________________________
function tower_builder(int $n): array {
  for ($i = 0; $i < $n; $i++) {
    $piramid[$i] = str_repeat(' ', $n - ($i + 1)) . str_repeat('*', 2 * $i + 1) . str_repeat(' ', $n - ($i + 1));
  }
  
  return $piramid;
}
_____________________________
function tower_builder(int $n): array {
  $pyramid = [];
  $base = 1;
  $maxWidth = ($n * 2) - 1;
 
  for($row = 1; $row <= $n; $row++) {
    $padding = ($maxWidth - $base);
    if($padding === 0) {
      $pyramid[] = str_pad('', $base, '*');
    } else {
      $padding = $padding / 2;
      $pyramid[] = str_pad('', $padding, ' ') . str_pad('', $base, '*') . str_pad('', $padding, ' ');
    }
    $base = $base + 2;
  }
  
  return $pyramid;
}
