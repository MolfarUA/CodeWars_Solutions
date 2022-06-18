function toCamelCase($str){
  return preg_replace_callback("~[_-](\w)~", function($m) { return strtoupper($m[1]); }, $str);
}
________________________
function toCamelCase($str){
    $str = str_replace("-", "_",$str);
    $firstPos = strpos($str, "_");
    return substr($str,0,$firstPos).str_replace("_", "",ucwords(substr($str,$firstPos), "_"));
}
________________________
function toCamelCase($str){
  $words = mb_split('[-_]',$str);
  $res=$words[0];
  for ($i=1;$i<=count($words);$i++){
    $res.=ucfirst($words[$i]);
  }
  return $res;
}
________________________
function toCamelCase($str){
  $str = preg_split('/[-_]/', $str, -1, PREG_SPLIT_NO_EMPTY);
  
  return array_shift($str) . implode('', array_map('ucfirst', $str));
}
________________________
function toCamelCase($str){
   $first_letter = $str[0];
  
   $str_with_almost_camel_case = ucwords( $str, '-_' );
  
   $str_end = substr($str_with_almost_camel_case, 1);

   return str_replace( [ '-',  '_' ] , '', $first_letter. $str_end );
}
