56484848ba95170a8000004d


function gps($interval, $array) {
  $maximum = 0;
  $counter = 1;
  while ($counter  < count($array)) {
    $distance = $array[$counter ] - $array[$counter -1];
    $speed = ($distance / ($interval / 3600));
    if ($speed > $maximum) {
      $maximum = $speed;
    }
    $counter++;
  }
  return floor($maximum);
}
_____________________________
function gps($s, $x) {
    for($i=1; $i<count($x); $i++) {
        $x[$i-1] = 3600 * abs($x[$i] - $x[$i-1]) / $s;
    }
    return floor(max($x));
}
_____________________________
define('SECONDS_PER_HOUR', 3600);

function gps($secondsPerInterval, $cumulativeDistances) {
  if(count($cumulativeDistances) <= 1) {
    return 0;
  }
  
  $averageSpeeds = [];
  
  for($interval=0; $interval < count($cumulativeDistances)-1; $interval++) {
      $intervalDifference = ($cumulativeDistances[$interval+1]-$cumulativeDistances[$interval]);
      $distancePassedInOneSecond = $intervalDifference/$secondsPerInterval;
      $averageSpeeds[] = $distancePassedInOneSecond*SECONDS_PER_HOUR;
  }

  return floor(max($averageSpeeds));
}
