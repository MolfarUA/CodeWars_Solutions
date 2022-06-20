57aa218e72292d98d500240f


function heron(float $a, float $b, float $c): float {
  return sqrt(($s = ($a + $b + $c) / 2) * ($s - $a) * ($s - $b) * ($s - $c));
}
________________________
function heron($a, $b, $c)
{
  $s = ($a + $b + $c) / 2;
  return sqrt( $s * ($s - $a) * ($s - $b) * ($s - $c) );
}
________________________
function heron($a, $b, $c)
{
  $s = ($a + $b + $c)/2;
  return $p = sqrt($s * ($s - $a) * ($s - $b) * ($s - $c));
}
