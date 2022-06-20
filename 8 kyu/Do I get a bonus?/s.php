56f6ad906b88de513f000d96


function bonusTime($s, $b) {
  return "$" . $s * ($b ? 10 : 1);
}
__________________________
function bonusTime($salary, $bonus) {
    return sprintf('$%s', $bonus ? $salary * 10 : $salary);
}
__________________________
function bonusTime($salary, $bonus) {
    if($bonus == true){
      return "$" . 10 * $salary; 
    }
    else {
      return "$" . $salary;
    }
}
__________________________
function bonusTime($salary, $bonus) {
 if ($bonus) {
   $salary = $salary * 10;
 }
 return '$'.$salary;
}
