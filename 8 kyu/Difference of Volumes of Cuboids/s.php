58cb43f4256836ed95000f97


function findDifference($a, $b) {
  return abs(array_product($a) - array_product($b));
}
________________________
function findDifference(array $a, array $b): int
{
  return abs(array_product($a) - array_product($b));
}
________________________
function findDifference($a, $b) {
  return max([array_product($a), array_product($b)]) - min([array_product($a), array_product($b)]);
}
