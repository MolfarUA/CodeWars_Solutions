559b8e46fa060b2c6a0000bf


function diagonal(int $n, int $p): int
{
  $fact = function ($x) use (&$fact) {
    return $x <= 1 ? 1 : $x * $fact($x - 1);
  };
  
  return round($fact($n + 1) / $fact($n - $p) / $fact($p + 1));
}
_____________________________
function diagonal($n, $p) {
    if ($p === 0) {
      return $n + 1;
    }
  $sum = 0;
  if ($p === 1) {
    for ($i= 0; $i <= $n ; $i++) {
       $sum += $i;
   }
   
   return $sum;
 }
 $sum = 0;
 for ($i= 2; $i <= $n ; $i++) {
     $sum += C($p,$i);
 }
  
  return $sum;
 
}
 function C($k, $n) {
   if ((gt($k)* gt($n-$k)) <= gt($n)) {
      return gt($n) / (gt($k)* gt($n-$k));
   }
 }
 function gt($n) {
   $gt = 1;
   for ($i=1; $i<= $n; $i++) {
   
    $gt *= $i;
     
   }
   return $gt;
 }
_____________________________
function diagonal($n, $p) {
    $numer = 1;
    $denom = 1;
    for($i = 0; $i < $p + 1; $i++){
        $numer *= $n + 1 - $i;
        $denom *= $p + 1 - $i;
    }
    return floor($numer/$denom);
}
