function sum_intervals(array $intervals): int {
    $values = [];

    foreach ($intervals as $interval) {
        for ($i = $interval[0]; $i < $interval[1]; $i++) {
            $values[$i] = 1;
        }
    }
    
    return array_sum($values);
}
                                                  
_______________________
function sum_intervals(array $intervals): int
{
    usort($intervals, function($a, $b) { return $a[0] - $b[0]; });
    $top = -INF;
    $cnt = 0;
    foreach ($intervals as list($from, $to)) {
        $local_from = max($from, $top);
        if ($to > $local_from) {
            $cnt += $to - $local_from;
            $top = $to;
        }
    }
    return $cnt;
}
          
___________________________
function sum_intervals(array $intervals): int {
  $heap = [];
  foreach ($intervals as $interval) {
    array_push($heap, ...range($interval[0], $interval[1] - 1));
  }
  return count(array_unique($heap));
}
          
______________________
function sum_intervals(array $intervals): int {
  foreach ($intervals as $interval)
    for ($i = $interval[0]; $i < $interval[1]; $i++)
      $points[$i] = 1;
  return array_sum($points);
}
                                              
_____________________
function sum_intervals(array $ints, $res=0): int {
  usort($ints,fn($a,$b)=>$a[0]-$b[0]);
  for($i=0; $i<count($ints); ++$i){
    if($i < count($ints)-1 and $ints[$i][1] >= $ints[$i+1][0]){
      $tmp= array_merge($ints[$i],$ints[$i+1]);
      $ints[$i+1]= [min($tmp),max($tmp)]; }
    else{ $res+= $ints[$i][1]-$ints[$i][0]; }    
    }
  return $res;
}
