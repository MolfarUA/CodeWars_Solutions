function findNb($m) {
  $n = 0;
  while ($m > 0) $m -= ++$n**3;
  return $m ? -1 : $n;
}
_________________________________________
function findNb($m) {
    $n = (sqrt(8 * sqrt($m) + 1) - 1) / 2;
    
    return $n == (int)$n ? $n : -1;
}
_________________________________________
function findNb($m) {
    $n = 0;
    while($m > 0)
      $m -= pow(++$n, 3);
    return $m == 0 ? $n : -1;
}
_________________________________________
/*
since in fact we have a growing array of values of the function (n (n + 1) / 2) ^ 2 => m, then using the bisection method
we find the desired value of n in several iterations without having to sum the values in a loop
*/
function findNb($m) {
    $search_range = array("start"=>0,"middle"=>-1,"end"=>4183059834009);
    while (true) {
      $search_range["middle"] = intdiv(($search_range["start"]+$search_range["end"]) , 2);
      $F_first = sum3($search_range["start"]);
      $F_last  = sum3($search_range["end"]);
      $F_middle = sum3($search_range["middle"]);
       
      if ($F_middle<$m) { $search_range["start"] = $search_range["middle"];}
      else {$search_range["end"] = $search_range["middle"];}
      
      //stop search
      if ($F_middle==$m||($search_range["end"]-$search_range["start"]==1)) {break;}
     
    }
    
    if ($F_middle==$m) return $search_range["middle"];
    if ($F_first==$m) return $search_range["start"];
    if ($F_last==$m) return $search_range["end"];

    return -1;
}

/*
n^3+(n-1)^3+...1^3 == 1^3+2^3+...+n^3 == (n(n+1)/2)^2
*/
function sum3($n){
  return pow(($n*($n+1))/2,2);
}
