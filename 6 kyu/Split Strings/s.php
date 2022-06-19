515de9ae9dcfc28eb6000001


function solution($str) {
  if (empty($str))
    return [];
  if (strlen($str) % 2 != 0)
    $str .= "_";
  return str_split($str, 2);
}
________________________________
function solution($str): array {
  preg_match_all('/\w{2}/', $str . '_', $matches);
  return array_values($matches[0]);
}
________________________________
function solution($str) {
  return strlen($str) ? str_split($str . (strlen($str) & 1 ? "_" : ""), 2) : [];
}
________________________________
function solution($str) {
  
  if($str === '') return [];
  
  $array_str = str_split($str, 2);
  $end = end($array_str);
  
  if(strlen($end) === 1)
      $array_str[key($array_str)] .= '_';
  
  return $array_str;
}
________________________________
function solution($str) {
  return array_slice(str_split("{$str}__", 2), 0, -1);
}
