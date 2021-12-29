function dnaToRna($str) {
  return str_replace("T", "U", $str);
}

_____________________________
function dnaToRna($str) {
  return strtr($str, 'T', 'U');
}

_____________________________
function dnaToRna($s) {
  
/* solution without function */  
//   $a = str_split($s);
  
//   foreach($a as $k=>$v){
//     $v=="T" ? $a[$k] = "U" : $a[$k] = $v;
//   }
  
//   return implode($a);

  
/* solution with function */  
  $trans = array("T" => "U");
  return  strtr($s, $trans);
  
   
}
