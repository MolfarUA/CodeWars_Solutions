5263c6999e0f40dee200059d


function getPINs($observed) {
  $variants = [
    "1" => ["1", "2", "4"],
    "2" => ["1", "2", "3", "5"],
    "3" => ["2", "3", "6"],
    "4" => ["1", "4", "5", "7"],
    "5" => ["2", "4", "5", "6", "8"],
    "6" => ["3", "5", "6", "9"],
    "7" => ["4", "7", "8"],
    "8" => ["5", "7", "8", "9", "0"],
    "9" => ["6", "8", "9"],
    "0" => ["8", "0"]
  ];
  
  $digits = str_split($observed);
  $result = $variants[array_shift($digits)];
  if($digits){
    $result = array_reduce($digits, function($result, $digit) use ($variants){
      $rr = [];
      foreach($result as $r){
        foreach($variants[$digit] as $m){
          $rr[] = $r.$m;          
        }
      }
      return $rr; 
    }, $result);
  }
  return $result;
}
______________________________
function getPINs(string $observed): array
{
    return array_map('join', cartesianProduct(array_map('digitVariations', str_split($observed))));
}

function digitVariations(int $digit): array
{
    $neighbors = [
        1 => [1, 2, 4],
        2 => [1, 2, 3, 5],
        3 => [2, 3, 6],
        4 => [1, 4, 5, 7],
        5 => [2, 4, 5, 6, 8],
        6 => [3, 5, 6, 9],
        7 => [4, 7, 8],
        8 => [5, 7, 8, 9, 0],
        9 => [6, 8, 9],
        0 => [8, 0],
    ];

    return $neighbors[$digit];
}

function cartesianProduct(array $a): array
{
    if (!$a) return [[]];

    $subset = array_shift($a);
    $cartesianSubset = cartesianProduct($a);

    $result = [];
    foreach ($subset as $value) {
        foreach ($cartesianSubset as $p) {
            array_unshift($p, $value);
            $result[] = $p;
        }
    }

    return $result;
}
______________________________
function getPINs($observed) {
  return (new PINsGenerator($observed))->getPINs(); 
}

class PINsGenerator {
  
  private $possible = [
    "1" => [1, 2, 4],
    "2" => [2, 1, 3, 5],
    "3" => [3, 2, 6],
    "4" => [4, 1, 5, 7],
    "5" => [5, 2, 4, 6, 8],
    "6" => [6, 3, 5, 9],
    "7" => [7, 4, 8],
    "8" => [8, 5, 7, 9, 0],
    "9" => [9, 6, 8],
    "0" => [0, 8]
  ];
  
  private $observed;
  
  function __construct($observed) {
    $this->observed = (string) $observed;
  }
  
  private function combine($begin = "", $i=0) {
    if($i >= strlen($this->observed)) return [$begin];
    
    $possible = $this->possible[$this->observed[$i]];
    $PINs = [];
    
    for($j=0; $j<count($possible); $j++) {
      $PINs = array_merge($PINs, $this->combine($begin.$possible[$j], $i+1));
    }
    
    return $PINs;
  }
  
  function getPINs() {
    return $this->combine();
  }
}
