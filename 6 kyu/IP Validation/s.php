515decfd9dcfc23bb6000006


function isValidIP(string $str): bool
{
    return filter_var($str, FILTER_VALIDATE_IP);
}
_____________________________
function isValidIP(string $str): bool
{
    return filter_var($str,FILTER_VALIDATE_IP,FILTER_FLAG_IPV4);
}
_____________________________
function isValidIP(string $str): bool{
  $array = explode('.', $str);
  if(count($array) == 4){
    foreach($array as $n){
      if($n > 255 || $n < 0 || !ctype_digit($n)){
        return false;
      }
    }
  } else {
    return false;
  }
  return true;
}
