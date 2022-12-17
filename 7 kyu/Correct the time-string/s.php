57873ab5e55533a2890000c7


function timeCorrect($timestring) {
    if (is_null($timestring)) {
      return null;
    }
    if (empty($timestring)) {
      return '';
    }
    if (!preg_match('/^\d{2}\:\d{2}\:\d{2}$/', $timestring)) {
      return null;
    }
    
    list($h, $m, $s) = explode(':', $timestring);
    $time = $h*3600 + $m*60 + $s;

    return date('H:i:s', $time);
}
_________________________________
function format_n($n) {return str_pad(intval($n), 2,'0', STR_PAD_LEFT);}

function timeCorrect($timestring) {
  if ($timestring === null) return null;
  
  if (empty($timestring)) return '';
  
  if (preg_match('/[^\d:]/', $timestring)) return null;
  
  $arr = explode(':', $timestring);
  
  if (count($arr) !== 3) return null;
  
  list($hours, $minutes, $seconds) = [$arr[0], $arr[1], $arr[2]];

  switch(true) {
      case $seconds > 59 : $minutes += $seconds / 60; $seconds = $seconds % 60;
      case $minutes > 59 : $hours += $minutes / 60; $minutes = $minutes % 60;
      case $hours > 23   : $hours = $hours % 24;
  }
  
  return format_n($hours).":".format_n($minutes).":".format_n($seconds);
}
_________________________________
function timeCorrect($timestring) {
  
  if (empty($timestring)) {
    return $timestring;
  }
  
  $splitted = explode(':', $timestring);
  
  if (count($splitted) < 2) {
    return null;
  }

  if(preg_match("/[a-z]/i", $timestring)){
    return null;
}
  
  $date = new \DateTime();
  $date->setTime(intval($splitted[0]), intval($splitted[1]), intval($splitted[2]));
  
    return $date->format("H:i:s");
}
