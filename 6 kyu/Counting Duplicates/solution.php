function duplicateCount($text) {

$dupCount = 0;
$text = array_count_values(str_split(strtolower($text)));

foreach ($text as $val) {
if ($val > 1) { $dupCount = $dupCount+1; }   
}

return $dupCount;
}
______________________
function duplicateCount($text) : int {
  $stats = array_count_values(str_split(strtolower($text)));
  return count(array_filter($stats, function($value) {return $value > 1;} ));
}
_______________
function duplicateCount($text) {
  $text = strtolower($text);
        $count = 0;
        foreach (count_chars($text, 1) as $val){
            if ($val > 1) $count++;
        }
        return $count;
}
