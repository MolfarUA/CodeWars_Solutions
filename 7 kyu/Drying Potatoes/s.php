function potatoes(int $p0, int $w0, int $p1): int {
  return $w0 * (100 - $p0) / (100 - $p1);
}
_______________________________________________
function potatoes($p0, $w0, $p1): int
{
  return floor($w0 * 0.01 * (100 - $p0) / (0.01 * (100 - $p1)));
}
_______________________________________________
function potatoes($p0, $w0, $p1): int {
    return (int) $w0 * (100 - $p0) / (100 - $p1);
}
_______________________________________________
function potatoes($p0, $w0, $p1) {
  return intdiv($w0 * (100 - $p0), (100 - $p1));
}
_______________________________________________
function potatoes($p0, $w0, $p1) {
  return $w0 - ceil($w0 * (($p0-$p1)/(100-$p1)));
}
_______________________________________________
function potatoes($p0, $w0, $p1) {
    $dryMatter =  $w0 * (100 - $p0)/100;
    $driedPopatoTotal =  100 * $dryMatter / (100 - $p1);
    return (int)$driedPopatoTotal;
}

