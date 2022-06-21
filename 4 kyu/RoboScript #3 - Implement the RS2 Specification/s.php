58738d518ec3b4bf95000192


// Instructions
const INSTRUCTION_GO_FORWARD = 'F',
  INSTRUCTION_TURN_LEFT = 'L',
  INSTRUCTION_TURN_RIGHT = 'R';
  
// Directions
const RIGHT = 0,
  DOWN = 1,
  LEFT = 2,
  UP = 3;

function execute(string $code): string {
  $instructions = parseCode($code);
  
  $direction = RIGHT; // start direction
  $position = [0, 0]; // start position
  $path = [$position]; // start path

  foreach (getInstruction($instructions) as $token) {
    list($instruction, $times) = splitInstructionToken($token);
    switch ($instruction) {
    case INSTRUCTION_GO_FORWARD:
      for ($i = 0; $i < $times; $i++) {
        $position = nextPosition($position, $direction);
        $path[] = $position;
      }
      break;
    case INSTRUCTION_TURN_RIGHT:
      $direction = rotate($direction, $times);
      break;
    case INSTRUCTION_TURN_LEFT:
      $direction = rotate($direction, -$times);
      break;
    }
  }
  
  return drawPath($path);
}

/**
 * Parse the code and return the list of instruction tokens
 * @param string $code
 * @return array
 */
function parseCode(string $code): array {
  $instructions = [];
  $len = strlen($code);
  $buf = '';
  $level = 0;
  for ($i = 0; $i < $len;) {
    $char = $code[$i];
    switch ($char) {
    case '(':
      if ($level === 0) {
        if ($buf) {
          if (strpos($buf, '(') !== false) {
            $buf = parseCode($buf);
          }
          $stack[] = [
            'instruction' => $buf,
            'times' => 1,
          ];
          $buf = '';
        }
      } else {
        $buf .= $char;
      }
      $level++;
      $i++;
      break;
    case ')':
      $level--;
      $i++;
      if ($level === 0) {
        $times = '';
        while (ctype_digit($code[$i])) {
          $times .= $code[$i];
          $i++;
        }
        if (strpos($buf, '(') !== false) {
          $buf = parseCode($buf);
        }
        $stack[] = [
          'instruction' => $buf,
          'times' => $times ? intval($times) : 1,
        ];
        $buf = '';
      } else {
        $buf .= $char;
      }
      break;
    default:
      $buf .= $char;
      $i++;
      break;
    }
  }
  if ($buf) {
    if (strpos($buf, '(') !== false) {
      $buf = parseCode($buf);
    }
    $stack[] = [
      'instruction' => $buf,
      'times' => 1,
    ];
    $buf = '';
  }
  if ($level !== 0) {
    throw new Exception('Invalid code');
  }
  return $stack;
}

/**
 * Return an iterator of token instructions
 * @param array $instructions
 * @return Traversable
 */
function getInstruction(array $instructions): Traversable {
  foreach ($instructions as $item) {
    for ($i = 0; $i < $item['times']; $i++) {
      if (is_string($item['instruction'])) {
        $tokens = [];
        preg_match_all('/(?<token>[FRL]\d*)/', $item['instruction'], $tokens);
        yield from $tokens['token'];
      } elseif (is_array($item['instruction'])) {
        yield from getInstruction($item['instruction']);
      }
    }
  }
}

/**
 * Rotate a direction to right N times
 * @param int $currentDirection
 * @param int $times Number of rotations to right (if negative, rotate to left)
 * @return int New direction
 */
function rotate(int $currentDirection, int $times): int {
  $newDirection = ($currentDirection + $times) % 4;
  if ($newDirection < 0) {
    $newDirection = 4 + $newDirection;
  }
  return $newDirection;
}

/**
 * Return the new position based on a current position and a direction.
 * @param array $position Coordinates X and Y
 * @param int $direction
 * @return array New position
 */
function nextPosition(array $position, $direction): array {
  switch ($direction) {
  case RIGHT: $position[0] += 1; break;
  case LEFT: $position[0] -= 1; break;
  case UP: $position[1] += 1; break;
  case DOWN: $position[1] -= 1; break;
  }
  return $position;
}

function splitInstructionToken(string $token): array {
  if (!preg_match('/(?<instruction>[FRL])(?<times>\d+)?/', $token, $matches)) {
    throw new Exception(sprintf('Invalid token: %s', $token));
  }
  return [
    $matches['instruction'],
    isset($matches['times']) ? intval($matches['times']) : 1,
  ];
}

function drawPath(array $path): string {
  // Find border of the path
  $minX = $minY = $maxX = $maxY = 0;
  foreach ($path as list($x, $y)) {
    $minX = min($x, $minX);
    $maxX = max($x, $maxX);
    $minY = min($y, $minY);
    $maxY = max($y, $maxY);
  }
  
  // Build matrix of strings
  $width = ($maxX + 1) - $minX;
  $height = ($maxY + 1) - $minY;
  
  $matrix = [];
  for ($l = 0; $l < $height; $l++) {
    $matrix[] = str_repeat(' ', $width);
  }
  
  // Draw path in matrix
  foreach ($path as list($x, $y)) {
    if ($minX < 0) {
      $x = $x - $minX;
    }
    if ($minY < 0) {
      $y = $y - $minY;
    }
  
    $matrix[count($matrix) - 1 - $y][$x] = '*';
  }
  
  return implode("\r\n", $matrix);
}
__________________________
function execute(string $code): string {
  $g= [['*']]; $d= 1; $l= [0,0];
  do{$code= preg_replace_callback("/\(([0-9LFR]+)\)(\d*)/", fn($x)=>str_repeat($x[1],(int)($x[2]?$x[2]:1)) ,$code ,-1 ,$cnt);}
  while($cnt);
  $code= preg_replace_callback("/[LFR]\d+/", fn($x)=>str_repeat($x[0][0],(int)substr($x[0],1)) ,$code);
  for($i=0; $i<strlen($code); ++$i){
    switch($code[$i]){
      case "L": $d-=1; $d= $d<0?3:$d; break;
      case "R": $d= ($d+1)%4; break;
      case "F": $g= mv_fwd($g,$d,$l); break;
      default: echo "BAD SCRIPT\n\n"; return null;
      }// close switch
    }// close for -- end of comands  
  $g= array_map(fn($x)=>implode('',$x), $g);
  return implode("\r\n", $g);
}

function mv_fwd($g,$d,&$l){
  switch($d){
    // the vertical dirs
    case 0: if($l[0]==0){array_unshift($g, array_fill(0,count($g[0]),' ') ); ++$l[0];}
            --$l[0]; $g[$l[0]][$l[1]]= '*'; break;
    case 2: if($l[0]==count($g)-1){array_push($g, array_fill(0,count($g[0]),' ') );}
            ++$l[0]; $g[$l[0]][$l[1]]= '*'; break;
    // the horizontal dirs  
    case 1: if($l[1]==count($g[0])-1){for($i=0; $i<count($g); ++$i){array_push($g[$i], ' ');} }
            ++$l[1]; $g[$l[0]][$l[1]]= '*'; break;
    case 3: if($l[1]==0){for($i=0; $i<count($g); ++$i){array_unshift($g[$i], ' ');} ++$l[1];}
            --$l[1]; $g[$l[0]][$l[1]]= '*'; break;
      }// close switch  
  return $g; 
}
__________________________
function execute(string $code): string {
  $code = unwrap_code($code);
  $steps = code_to_steps($code); //convert RS program to coordinates of robot's steps
  list($left, $top, $right, $bottom) = boundaries($steps);
  
  $width  = $right - $left + 1;
  $height = $bottom - $top + 1;
  
  $field = array_fill(0, $height, str_repeat(' ', $width));

  foreach($steps as list($x, $y)) {
    $field[$y - $top][$x - $left] = '*';
  }
  
  return implode("\r\n", $field);
}

// Returns left, top, right, bottom of a set of coordinates
function boundaries(array $coords): array {
  $bounds = [0, 0, 0, 0];
  foreach ($coords as list($x, $y)) {
    if ($x < $bounds[0]) $bounds[0] = $x;
    if ($x > $bounds[2]) $bounds[2] = $x;
    if ($y < $bounds[1]) $bounds[1] = $y;
    if ($y > $bounds[3]) $bounds[3] = $y;
  }
  return $bounds;
}

function code_to_steps(string $code): array {
  $steps = [ [0,0] ];
  $x = $y = 0;
  $dx = 1; $dy = 0; //initial direction is right
  foreach(str_split($code) as $cmd) {
    switch($cmd) {
      case 'R': 
        list($dx, $dy) = [$dx == 0 ? -$dy : 0, $dy == 0 ?  $dx : 0];
      break;
      case 'L': 
        list($dx, $dy) = [$dx == 0 ?  $dy : 0, $dy == 0 ? -$dx : 0];
      break;
      case 'F': 
        $x += $dx; 
        $y += $dy; 
        $steps[] = [$x, $y]; 
      break;
    }
  }
  return $steps;
}

/* Unwraps RS2 code to a string of single commands, e.g. converts (XY3)2 to XYXYXYXYXYXY */
function unwrap_code(string $code): string {
  // Unwrap parentheses 
  for($count = 1; $count;) {
    $code = preg_replace_callback('/\(([^(]*?)\)(\d+)?/', function($matches) {
      $repeat = $matches[2] ? intval($matches[2]) : 1;
      return str_repeat( $matches[1], $repeat );
    }, $code, -1, $count);
  }
  // Replace command+repeat-count with command repeated repeat-count times 
  $code = preg_replace_callback('/([RLF])(\d+)/', function($matches) {
    return str_repeat( $matches[1], intval($matches[2]) );
  }, $code);
  
  return $code;
}
