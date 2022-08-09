57f780909f7e8e3183000078


function grow($a) {
  
  if ( !empty($a) ) {
        return $result = array_product($a);
    }
}
_______________________
function grow($a) {
  $r = 1;
  foreach ($a as $k => $v) { $r *= $v; }
  return $r;
}
_______________________
function multiply($x, $y){
    return $x * $y;
}

function grow($a) {
    return array_reduce($a, 'multiply', 1);
}
