544675c6f971f7399a000e79


function stringToNumber(string $str): int {
  return (int)$str;
}
_______________________
function stringToNumber($str) { return +$str; }
_______________________
function stringToNumber(string $str):int {
  return intVal($str);
}
_______________________
function stringToNumber($str) {
  if(!$str){
    return 0;
  }
  
  return (int) $str;
}
_______________________
function stringToNumber($str) {
  return $number = (int)$str;
}
