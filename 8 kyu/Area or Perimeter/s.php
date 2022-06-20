5ab6538b379d20ad880000ab


function areaOrPerimeter (int $l, int $w){
 return $l == $w ? $l * $w : ($l * 2) + ($w * 2);
}
________________________
function areaOrPerimeter (int $l, int $w){
    if ($l == $w) {
        return $l * $w;
    } else {
        return $l + $w + $l + $w;
    }
}
________________________
function areaOrPerimeter (int $l, int $w){
  $output = ($l == $w ? $l * $w : 2 * $l + 2 * $w);
  return $output;
}
