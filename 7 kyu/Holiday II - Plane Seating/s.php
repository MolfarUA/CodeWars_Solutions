57e8f757085f7c7d6300009a


function planeSeat($a) {
  $matched = preg_match("/^([1-9]|[1-5]\d|60)([A-HK])$/", $a, $matches);
  if (!$matched) {
    return "No Seat!!";
  }
  $x = $matches[1] <= 20 ? "Front" : ($matches[1] <= 40 ? "Middle" : "Back");
  $y = $matches[2] <= "C" ? "Left" : ($matches[2] <= "F" ? "Middle" : "Right");
  return "$x-$y";
}
_______________________________
function planeSeat($a){
  if (!preg_match('/^([1-9]|[1-5][0-9]|60)([ABCDEFGHK])$/', $a, $matches)) {
    return 'No Seat!!';
  }
  $section = (intval($matches[1]) > 40) ? 'Back' : ((intval($matches[1]) > 20) ? 'Middle' : 'Front');
  $cluster = ($matches[2] > 'F') ? 'Right' : (($matches[2] > 'C') ? 'Middle' : 'Left');
  return "{$section}-{$cluster}";
}
_______________________________
function planeSeat($a){
    echo "<br>";
echo $a;
      echo "<br>";
  $num = preg_replace("/[A-Za-z]/","",$a);
    $let = preg_replace("/[0-9]/","",$a);
  $let = preg_replace("/I|J|[L-Z]/","*",$let);
//  echo $let;
  echo "<br>";
  if ($num>60 or $let=="*" or $let=="") return "No Seat!!";
  elseif($num>=1 and $num<=20) $c="Front";
  elseif($num>=21 and $num<=40) $c="Middle";
  elseif($num>=40 and $num<=60) $c="Back";
if ($let=="A" or $let=="B" or $let=="C") $d="Left";
  elseif ($let=="D" or $let=="E" or $let=="F") $d="Middle";
   elseif ($let=="G" or $let=="H" or $let=="K") $d="Right";
return $c."-".$d;
  
}
_______________________________
function planeSeat($a){
  $number = implode("",array_filter(preg_split('#[^\d]#',$a)));
  $letter = implode("",array_filter(preg_split('#[\d]#',$a)));
  
  $arrayLetter = ["A"=>"Left",
                 "B"=>"Left",
                 "C"=>"Left",
                 "D"=>"Middle",
                 "E"=>"Middle",
                 "F"=>"Middle",
                 "G"=>"Right",
                 "H"=>"Right",
                 "K"=>"Right"];
  
  if($number > 60) {
    return "No Seat!!";
  }
  
  if(!array_key_exists($letter, $arrayLetter)) {
    return "No Seat!!";
  }
  
  if($number >= 1 AND $number <= 20){
    $numberPosition = "Front";
  }
  
  if($number >= 21 AND $number <= 40){
    $numberPosition = "Middle";
  }
  
  if($number > 40){
    $numberPosition = "Back";
  }
  
  return $numberPosition."-".$arrayLetter[$letter];
}
