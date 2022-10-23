553e8b195b853c6db4000048


function hasUniqueChars($string) {
  $array = str_split($string);
  return count($array) == count(array_unique($array));
}
__________________________
function hasUniqueChars($string)
{
    $posicion = [];
    $unico = true;
    for ($i = 0; $i < strlen($string); $i++) {

        if (in_array(ord(substr($string, $i, 1)), $posicion)) {
            $unico = false;
            break;
        }
        array_push($posicion, ord(substr($string, $i, 1)));
    }
    return $unico;
}
__________________________
function hasUniqueChars($string) {
  return count(array_unique(str_split($string))) == count(str_split($string));
}
