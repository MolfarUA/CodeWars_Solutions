58c5577d61aefcf3ff000081


function encodeRailFenceCipher($string, $numberRails) {
  $arr = array_pad([], $numberRails, '');
  for($i = 0, $j = 0; $i < strlen($string); $i++, $j++){
    $arr[abs($j)] .= $string[$i];
    if($j + 1 === $numberRails) $j = -$j;
  }
  return join('', $arr);
}

function decodeRailFenceCipher($string, $numberRails) {
  $n = $numberRails==1?: 2*($numberRails-1); // rails crossed in a cycle
  $cn = floor(strlen($string)/$n); // cycles passed
  $r = strlen($string) - $n*$cn; // remain
  
  // split string over rails
  $arr = [substr($string, 0, $cn + ($r>0))];
  for($j = 1, $s = substr($string, strlen($arr[0])); $j < $numberRails; $j++){
    $arr[$j] = substr($s, 0, 2*$cn+($r>$j)+($n-$r<$j));
    $s = substr($s, strlen($arr[$j]));
  }
  
  // compose answer char by char
  $str = '';  
  for($j = 0; $c = substr($arr[abs($j)],0,1); $j++){
    $str .= $c;
    $arr[abs($j)] = substr($arr[abs($j)],1);
    if($j + 1 === $numberRails) $j = -$j;
  }
  return $str;
}
_____________________________
function encodeRailFenceCipher($s, $r) {
  $res = '';
  for ($k = 0; $k < $r; $k++) {
    $p = 2 * $k;
    $q = 2 * ($r - $k - 1);
    for ($i = $k; $i < strlen($s); $i += $p ? $p : $q) {
      $res .= $s[$i];
      $t = $p; $p = $q; $q = $t;
    }
  }
  return $res;
}

function decodeRailFenceCipher($s, $r) {
  $res = $s;
  $j = 0;
  for ($k = 0; $k < $r; $k++) {
    $p = 2 * $k;
    $q = 2 * ($r - $k - 1);
    for ($i = $k; $i < strlen($s); $i += $p ? $p : $q) {
      $res[$i] = $s[$j++];
      $t = $p; $p = $q; $q = $t;
    }
  }
  return $res;
}
_____________________________
function getArIndex($numberRails, $len) {
  $arRails = array_fill(0, min($numberRails, $len), []);
  $segmLen = 2 * $numberRails - 2;
  for ($i = 0; $i < $len; $i++) {
    $iOtr = $i % $segmLen;
    $arRails[$iOtr < $numberRails ? $iOtr : $segmLen - $iOtr][] = $i;
  } 
  return array_reduce($arRails, function($carry, $item) {
    return array_merge($carry, $item);
  }, []);
}
function encodeRailFenceCipher($string, $numberRails) {
  $strLenMessage =strlen($string);
  $result = '';
  foreach (getArIndex($numberRails, $strLenMessage) as $index) {
    $result .= $string[$index];
  }
  return $result;
}

function decodeRailFenceCipher($string, $numberRails) {
  $strLenMessage =strlen($string);
  $result = str_repeat(' ', $strLenMessage);
  $arIndex = getArIndex($numberRails, $strLenMessage);
  for ($i = 0; $i < count($arIndex); $i++) {
    $result[$arIndex[$i]] = $string[$i];
  }
  return $result;
}
