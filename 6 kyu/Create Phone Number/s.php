function createPhoneNumber(array $digits): string {
  return sprintf("(%d%d%d) %d%d%d-%d%d%d%d", ...$digits);
}
_______________________________
function createPhoneNumber($numbersArray) {
  return vsprintf("(%d%d%d) %d%d%d-%d%d%d%d", $numbersArray);
}
_______________________________
function createPhoneNumber($numbersArray) {
    return sprintf('(%d%d%d) %d%d%d-%d%d%d%d', ...$numbersArray);
}
_______________________________
function createPhoneNumber($numbersArray) {
  preg_match('/(\d{3})(\d{3})(\d{4})/', implode('', $numbersArray), $matches);
  return '('.$matches[1].') '.$matches[2].'-'.$matches[3];
}
_______________________________
$arr = array(1,2,3,4,5,6,7,8,9,0);

function createPhoneNumber($numbersArray) {
  foreach ($numbersArray as $k=> &$v) {
    if ($k == 0) {
      $v = '(' . $v;
    }else if($k == 2){
      $v .= ') ';
    }else if($k == 5){
      $v .= '-';
    }
  }
  unset($v);
  return implode($numbersArray);
}


echo createPhoneNumber($arr);
