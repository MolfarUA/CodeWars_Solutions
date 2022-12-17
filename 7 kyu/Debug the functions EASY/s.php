5844a422cbd2279a0c000281


function multi($array) {
  return array_product($array);
}
function add($array) {
  return array_sum($array);
}
function reverse($string) {
  return strrev($string);
}
________________________
function multi( array $array ) : int {
  return array_product( $array );
}
function add( array $array ) : int {
  return array_sum( $array );
}
function reverse( string $string ) : string {
  return strrev( $string );
}
________________________
function multi($a) {
  return array_reduce($a, function ($s, $e) {return $s * $e;}, 1);
}
use function array_sum as add;
use function strrev as reverse;
