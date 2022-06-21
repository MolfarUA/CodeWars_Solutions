5870fa11aa0428da750000da


class SparseField{
    // Sparse Array
    private $entries = [];

    // [ [MinX, MaxX], [MinY, MaxY] ]
    private $limits = [ [INF, -INF], [INF, -INF] ];

    public function add(int $x, int $y){

        $this->entries[] = [$x, $y];

        // Update Min and Max coordinates
        if($x < $this->limits[0][0]){
            $this->limits[0][0] = $x;
        }
        if($x > $this->limits[0][1]){
            $this->limits[0][1] = $x;
        }
        if($y < $this->limits[1][0]){
            $this->limits[1][0] = $y;
        }
        if($y > $this->limits[1][1]){
            $this->limits[1][1] = $y;
        }
    }

    public function output(){

        // Initialize Field Array
        $width = -$this->limits[0][0] + $this->limits[0][1] + 1;
        $height = -$this->limits[1][0] + $this->limits[1][1] + 1;
        $field = array_fill(0, $height, array_fill(0, $width, " "));

        // Add Tracks
        foreach ($this->entries as $entry) {
            $x = $entry[0] - $this->limits[0][0];
            $y = $entry[1] - $this->limits[1][0];
            $field[$y][$x] = '*';
        }

        // Convert to String
        $output = "";
        foreach($field as $row){
            foreach($row as $point){
                $output .= $point;
            }
            $output .= "\r\n";
        }
        return substr($output, 0, -2);
    }
}

class Interpreter{
    const UP = 0;
    const RIGHT = 1;
    const DOWN = 2;
    const LEFT = 3;

    // Change of coordinates after Move
    // E.g. When moving Left, the X coordinate changes by $changeX[LEFT]
    private $changeX = [0, 1, 0, -1];
    private $changeY = [-1, 0, 1, 0];


    public function __construct(){
        $this->field = new SparseField();
        $this->x = 0;
        $this->y = 0;
        $this->direction = self::RIGHT;
        $this->leaveTrack();
    }

    private function leaveTrack(){
        $this->field->add($this->x, $this->y);
    }

    private function performMove($move){
        switch($move){
            case 'F':
                $this->x += $this->changeX[$this->direction];
                $this->y += $this->changeY[$this->direction];
                $this->leaveTrack();
                break;
            case 'L':
                $this->rotate(-1);
                break;
            case 'R':
                $this->rotate(1);
                break;
        }
    }

    // $quadrants: number of 90° turns, could be negative
    private function rotate($quadrants){
        $this->direction = ($this->direction + $quadrants + 4) % 4;
    }

    // Perform Movement as indicated by Token array
    public function execute(array $tokens){
        foreach($tokens as $token){
            for ($i = 0; $i < $token->getIterations(); $i++) {
                $this->performMove($token->move);
            }
        }
    }
}

interface Token{}

class MovementToken implements Token{
    private $iterations = 0;

    public function __construct($move){
        $this->move = $move;
    }

    public function addIterationDigit($digit){
        $this->iterations = $this->iterations * 10 + $digit;
    }

    public function getIterations(){
        if($this->iterations == 0){
            // No number of iterations specified
            return 1;
        }else{
            return $this->iterations;
        }
    }
}

class Tokenizer{

    // Split code into movement tokens: F, L, R, Fn, Ln, Rn (n being any number)
    public static function tokenize(string $command){
        $tokens = [];
        $lastToken = null;
        foreach(str_split($command) as $char){
            if(is_numeric($char)){
                $lastToken->addIterationDigit(intval($char));
            }else{
                $tokens[] = $lastToken;
                $lastToken = new MovementToken($char);
            }
        }

        // First entry always null
        unset($tokens[0]);
        
        $tokens[] = $lastToken;
        return $tokens;
    }
}

function execute(string $code): string {
    $interpreter = new Interpreter();
    $interpreter->execute(Tokenizer::tokenize($code));
    return $interpreter->field->output();
}
__________________________
function execute(string $code): string {
  if (empty($code)) return '*';
  
  preg_match_all("/[FLR]\d*/", $code, $matches);

  // 0 - faces to the right. 1 - faces to the downwards (after R command). etc ...
  $direction = 0;
  $x = 0;
  $y = 0;
  $map = ['*'];
  
  foreach ($matches[0] as $command) {
    
    $repeat = (strlen($command) > 1) ? substr($command, 1) : 1;

    switch ($command{0}) {
      case 'R':
        for ($i=0; $i < $repeat; $i++) {
          ($direction == 3) ? ($direction = 0) : $direction++;
        }
        break;
      case 'L':
        for ($i=0; $i < $repeat; $i++) {
          ($direction == 0) ? ($direction = 3) : $direction--;
        }
        break;
      case 'F':
        for($i=0; $i < $repeat; $i++) {
          move($map, $x, $y, $direction);
        }
      break;
    }
  }
  
  return implode("\r\n", $map);
}

function move(& $map, & $x, & $y, $direction) {
  $space = ' ';
  
  switch ($direction) {
    case 0:
      $x++;
      if ($x == strlen($map[$y])) {
        foreach ($map as $k => $v) {
          $map[$k] .= $space;
        }
      }
      break;
    case 1:
      $y++;
      if ($y == count($map)) {
        array_push($map, str_repeat($space, strlen($map[0])));
      }
      break;
    case 2:
      if ($x == 0) {
        foreach ($map as $k => $v) {
          $map[$k] = $space . $v;
        }
      } else {
        $x--;
      }
      break;
    case 3:
      if ($y == 0) {
        array_unshift($map, str_repeat($space, strlen($map[0])));
      } else {
        $y--;
      }
      break;
  }
  
  $map[$y]{$x} = '*';
}
__________________________
function execute(string $code): string {
  $g= [['*']]; $d= 1; $l= [0,0];
  $code= preg_replace_callback("/[LFR]\d+/",fn($x)=>str_repeat($x[0][0],(int)substr($x[0],1)),$code);
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
