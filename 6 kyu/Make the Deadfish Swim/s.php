function parse($data) {
  $commands = str_split($data);
  $result = [];
  $counter = 0;
  
  foreach($commands as $command) {
    switch($command) {
      case 'i': $counter++; break;
      case 'd': $counter--; break;
      case 's': $counter = pow($counter, 2); break;
      case 'o': $result[] = $counter;
    } 
  }
  
  return $result;
}
__________________________________________
function parse($data) {
  $num = 0;
  $res = [];
    foreach(str_split($data) as $word) {
      if($word == 'i') $num++;
      if($word == 'd') $num--;
      if($word == 's') $num *= $num;
      if($word == 'o') $res[] = $num;
    }
  return $res;
}
__________________________________________
/**
 * Make the Deadfish swim
 * 
 * @description simple parser that will parse and run Deadfish.
 *              Deadfish has 4 commands, each 1 character long:
 *                  i increments the value (initially 0)
 *                  d decrements the value
 *                  s squares the value
 *                  o outputs the value into the return array
 * 
 * @author akerayoui
 */
function parse( string $data ): array {
    
    for ( $i = $g = 0, $li = strlen( $data ), $stack = []; $i < $li; $i++ ) {

        if ( ! in_array( $data[$i], ['i', 'd', 's', 'o'] ) )
            continue;
        
        if ( $data[$i] == 'i' )
            $g++;

        elseif ( $data[$i] == 'd' )
            $g--;

        elseif ( $data[$i] == 's' )
            $g**= 2;

        else 
            $stack[] = $g;   
    }

    return $stack;
}
