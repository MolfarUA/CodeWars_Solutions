55f9b48403f6b87a7c0000bd


function paperwork(int $n, int $m): int {
  return $n < 0 || $m < 0 ? 0 : $n * $m;
}
__________________________
function paperwork(int $n, int $m): int
{
  if (areBlankPages($n, $m)) {
    return 0;
  }
  
  return $n * $m;
}

function areBlankPages(int $n, int $m): bool
{
  return ($n < 0 || $m < 0);
}
__________________________
function paperwork(int $n, int $m): int
{
      if($m <= 0 or $n <= 0)
        {
        return 0;
      }
  return $m * $n;
}
__________________________
function paperwork(int $n, int $m): int
{
  switch($n * $m) {
    case $n < 0: 
      return 0;
      
    case $m < 0:
      return 0;
      
    default:
      return $n * $m;
      }
}
__________________________
function paperwork(int $n, int $m): int
{
  if ($n < 0 or $m < 0){
    return 0;
  }
  
  return $m * $n;
}
