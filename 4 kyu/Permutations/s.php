5254ca2719453dcc0b00027d


function permutations(string $str): array
{
    if (strlen($str) < 2) {
        return [$str];
    }

    $result = [];
    $stop = strlen($str) - 1;
    for ($i = 0; $i <= $stop; $i++) {
        $substr = substr($str, 0, $i) . substr($str, $i + 1);
        foreach (permutations($substr) as $per) {
            $result[] = $str[$i] . $per;
        }
    }
    return array_unique($result);
}
______________________________
function permutations(string $s): array {
  $result = array();
  
  for($i = 0; $i < 100000; $i++) {
    array_push($result, str_shuffle($s));
  }
  
  
  $result = array_unique($result);
  return $result;
}
______________________________
function permutations(string $str): array {
  if (strlen($str) < 2) return [$str];
  $result = [];
  for ($i = 0; $i < strlen($str); $i++) {
    $substr = substr($str, 0, $i) . substr($str, $i + 1);
    $tmparr = permutations($substr);
    foreach ($tmparr as &$item) $item = $str[$i] . $item;
    $result = array_merge($result, $tmparr);
  }
  return array_unique($result);
}
