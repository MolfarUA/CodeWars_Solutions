53ee5429ba190077850011d4


function doubleInteger($i) {
  return $i*2;
}
__________________________
function doubleInteger($i)
{
  return $i << 1;
}
__________________________
function doubleInteger(int $i): int
{
  return $i+$i;
}
__________________________
function doubleInteger($i)
{
  return $i+=$i;
}
