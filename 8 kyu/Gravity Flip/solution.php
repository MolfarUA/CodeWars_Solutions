function flip(string $dir, array $arr): array {
  $dir == 'R' ? sort($arr) : rsort($arr);
  return $arr;
}

_____________________________________________
function flip(string $dir, array $arr): array {
  $dir === 'R' ? sort($arr): rsort($arr); 
  return $arr;
}

_____________________________________________
function flip(string $dir, array $arr): array {
  $dir == 'L' ? rsort ( $arr ) : sort( $arr );
  return $arr;
}

_____________________________________________
function flip(string $dir, array $arr): array {
  
  if ("R" == $dir) {
      sort($arr);
      return $arr;
  } elseif ("L" == $dir) {
      rsort($arr);
      return $arr;
  }
}

_____________________________________________
function flip(string $dir, array $arr): array {
  
  switch($dir) {
      case 'R':
        sort($arr);
        break;
      case 'L':
        rsort($arr);
        break;
      default:
        throw new Exception("UNKNOWN {$dir}");
  }
  
  return $arr;
}
