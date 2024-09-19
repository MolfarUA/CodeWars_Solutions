5875b200d520904a04000003

function enough($cap, $on, $wait) {
  return max(0, $wait - $cap + $on);
}
___________________________
function enough($cap, $on, $wait) {
  
  return $cap >= ($on + $wait) ? 0 : ($wait - ($cap - $on));
}
___________________________
function enough($cap, $on, $wait) {
  $diff = $cap - $on - $wait;
  return $diff < 0 ?  abs($diff) : 0;
}
___________________________
function enough($cap, $on, $wait) {
  $totalPassengers = $on + $wait;
  
  if ($totalPassengers <= $cap) {
    return 0;
  } else {
    return $totalPassengers - $cap;
  }
}
