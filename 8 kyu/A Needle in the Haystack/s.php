function findNeedle($a) {
  return "found the needle at position " . array_search("needle", $a);
}
________________________
function findNeedle($haystack) {
  return 'found the needle at position ' . array_search('needle', $haystack);
}
________________________
function findNeedle($haystack) {
  $b = array_search("needle", $haystack);
  return 'found the needle at position ' .  $b;
}
________________________
function findNeedle($haystack)
{
  $message = "found the needle at position ";
  $index = array_search("needle", $haystack);
  
  $res = $message . $index;
  
  return $res;
  
}
________________________
function findNeedle($haystack) {
  $key =  array_search('needle', $haystack);
  return ($key > 0) ? "found the needle at position $key" : null;
}
