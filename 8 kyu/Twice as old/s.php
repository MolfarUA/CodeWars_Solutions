5b853229cfde412a470000d0



function twice_as_old($dad_years_old, $son_years_old) {
   return abs( $dad_years_old - $son_years_old * 2);
}
______________________________
function twice_as_old($dad_years_old, $son_years_old) {
  $raznitca = $son_years_old*2;
  if($raznitca > $dad_years_old){
    return $raznitca - $dad_years_old;
   }elseif($raznitca < $dad_years_old){
    return $dad_years_old - $raznitca;
  }else{
    return 0;
  }
}
______________________________
function twice_as_old($dad, $son) {
   return abs($dad-2*$son);
}
