55466989aeecab5aac00003e


function sqInRect($width, $height) {
    
    if ($height === $width) {
        return null;
    }
    $squares = [];
    while ($width > 0) {
        if ($height > $width) {
            $squares[] = $width;
            $height -= $width;
        } else {
            $squares[] = $height;
            $width -= $height;
        }
    }
    return $squares;
}
______________________________
function sqInRect($lng, $wdth, &$result = [], $count = 0) {

    if ($lng == $wdth && count($result) == 0) return null;
    if ($lng == 0 || $wdth == 0) return $result;

    $min = min($lng, $wdth);
    $max = max($lng, $wdth);

    $result[] = $min;
    return sqInRect($min, $max-$min, $result, $count+1);
}
______________________________
function sqInRect($lng, $wdth) {

  if ($lng === $wdth) return null;
  
  $shortSide = $lng > $wdth ? $wdth : $lng;
  $longSide = $lng > $wdth ? $lng : $wdth;
  
  return array_merge([$shortSide], sqInRect($longSide - $shortSide, $shortSide) ?: [$shortSide]);
}
