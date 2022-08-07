57cfdf34902f6ba3d300001e


function twoSort($s) {
    asort($s);
    return implode('***', str_split(array_shift($s)));
}
___________________________
function twoSort( array $s ) : string {
    return implode( '***', str_split( min( $s ) ) );
}
___________________________
function twoSort($s) {
  sort($s);
  return implode('***', str_split($s[0]));
}
