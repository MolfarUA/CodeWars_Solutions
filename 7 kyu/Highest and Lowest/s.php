function highAndLow($numbers) {
  $a = explode(' ', $numbers);
  return max($a) . " " . min($a);
}
______________________________
/**
 * Highest and Lowest
 * 
 * @description return the highest and lowest number
 *              in format of "$high $low" string.
 * 
 * @param string $numbers string of space separated numbers
 * @return string
 * 
 * @author akerayoui
 */
function highAndLow( string $numbers ) : string {

    // explode string as array of numbers
    $explode = explode( " ", $numbers );

    // return the desired string value
    return max( $explode ) . " " . min( $explode );
}
______________________________
function highAndLow($numbers)
{
  #Splitting the string into array on spaces
  $arr = explode(' ',$numbers);
  
  #Sorting the array - the smallest item will be first and the biggest will be last
  sort($arr);
  
  #Returning the last item in the array (biggest) followed by a space and the first item in the array (smallest)
  return $arr[count($arr)-1]." ".$arr[0];
}
______________________________
function highAndLow($numbers){
  $arr = explode(" ", $numbers);
  $high = max($arr);
  $low = min($arr);
  return "$high $low";
}
______________________________
function highAndLow($numbers)
{
  return max(explode(" ", $numbers)) . " ". min(explode(" ", $numbers));
}
______________________________
function highAndLow($numbers)
{
  $arr = explode(' ', $numbers);
  $max = max($arr);
  $min = min($arr);
  return $max . ' ' . $min;
}
