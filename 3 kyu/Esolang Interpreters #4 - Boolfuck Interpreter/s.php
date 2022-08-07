5861487fdb20cff3ab000030


function boolfuck(string $code, string $input = ""): string
{
    // prepare binaryInput
    $binaryInput = [];
    if ($input) {
        $input = str_split(strrev($input));
        foreach ($input as $char) {
            $bits = str_pad(decbin(ord($char)), 8, '0', STR_PAD_LEFT);
            array_push($binaryInput, ...str_split($bits));
        }
    }

    // initialize variables
    $ptr = 0; // data pointer
    $memory = [0]; // machine memory
    $ptrMin = 0;
    $ptrMax = 0;
    $binaryOutput = '';

    // interpretation cycle
    $stop = strlen($code);
    for ($i = 0; $i < $stop; $i++) {
        switch ($code[$i]) {
            case '<':
                $ptr--;
                if ($ptr < $ptrMin) {
                    $ptrMin--;
                    $memory[$ptr] = 0;
                }
                break;
            case '>':
                $ptr++;
                if ($ptr > $ptrMax) {
                    $ptrMax++;
                    $memory[$ptr] = 0;
                }
                break;
            case '+':
                $memory[$ptr]++;
                $memory[$ptr] %= 2;
                break;
            case ';':
                $binaryOutput .= $memory[$ptr];
                break;
            case ',':
                $memory[$ptr] = array_pop($binaryInput);
                break;
            case '[':
                if ($memory[$ptr] == 0) {
                    $open = 1;
                    while ($open != 0) {
                        $i++;
                        switch ($code[$i]) {
                            case '[':
                                $open++;
                                break;
                            case ']':
                                $open--;
                                break;
                        }
                    }
                }
                break;
            case ']':
                $closed = 1;
                while ($closed != 0) {
                    $i--;
                    switch ($code[$i]) {
                        case '[':
                            $closed--;
                            break;
                        case ']':
                            $closed++;
                            break;
                    }
                }
                $i--;
                break;
        }
    }

    // decode output
    $binaryOutput = str_split($binaryOutput, 8);
    $output = '';
    foreach ($binaryOutput as $bits) {
        $output .= chr(bindec(strrev($bits)));
    }
    return $output;
}
_____________________________
function boolfuck(string $code, string $input = ""): string {
  // Convert character input into bits.  Each byte is read in little-endian order
  $bit_input = implode(array_map(function ($c) {return strrev(str_repeat("0", 8 - strlen($s = decbin(ord($c)))) . $s);}, str_split($input)));
  // Initialize Tape (can be extended indefinitely in both directions)
  $tape = [0];
  // Pointer
  $pointer = 0;
  // Read bit input left to right
  $input_index = 0;
  // Initialize bit output
  $bit_output = "";
  for ($i = 0; $i < strlen($code); $i++) {
    switch ($code[$i]) {
      case "+":
      // Flip the bit under the pointer
      $tape[$pointer] = intval(!$tape[$pointer]);
      break;
      case ",":
      // Read a bit from the bit input into the current bit under the pointer
      $tape[$pointer] = isset($bit_input[$input_index++]) ? $bit_input[$input_index - 1] : 0;
      break;
      case "<":
      // Moves the pointer left by 1 bit.  Expand tape to the left when necessary
      if (!isset($tape[--$pointer])) $tape[$pointer] = 0;
      break;
      case ">":
      // Moves the pointer right by 1 bit.  Expand tape to the right when necessary
      if (!isset($tape[++$pointer])) $tape[$pointer] = 0;
      break;
      case ";":
      // Output the current bit under the pointer
      $bit_output .= $tape[$pointer];
      break;
      case "[":
      // Skip to matching "]" if bit under current pointer is 0
      if ($tape[$pointer] === 0) {
        $unmatched = 1;
        while ($unmatched) {
          if ($code[++$i] === "[") $unmatched++;
          if ($code[$i] === "]") $unmatched--;
        }
      }
      break;
      case "]":
      // Jump backwards to matching "[" if bit under current pointer is nonzero (i.e. 1)
      if ($tape[$pointer] !== 0) {
        $unmatched = 1;
        while ($unmatched) {
          if ($code[--$i] === "[") $unmatched--;
          if ($code[$i] === "]") $unmatched++;
        }
      }
      break;
    }
  }
  // Convert bit output into character output
  $chars = array_map(function ($b) {return chr(bindec(strrev($b . str_repeat("0", 8 - strlen($b)))));}, str_split($bit_output, 8));
  // Construct output string from character array (not sure why implode() doesn't work properly when I try to convert the bit output in one step and return it straight away)
  $output = "";
  foreach ($chars as $char) $output .= $char;
  return $output;
}
_____________________________
function boolfuck($code, $input_ = "") {
    $r = ""; $inputString = $input_;
    $tape = array (0);

    $input = 0; $output = 0;
    $ptr = 0; $iPtr = 0; $oPtr = 0;

    $stack = array(); $otoc = array(); $ctoo = array();
    for ($i = 0; $i < strlen($code); $i++) {
        if ($code[$i] == '[') array_push ($stack, $i);
        else if($code[$i] == ']') { 
            $otoc[end($stack)] = $i;
            $ctoo[$i] = end($stack);
            array_pop($stack);
        }      
    }
  
    for ($i = 0; $i < strlen($code); $i++) {
        switch ($code[$i]) {
            case '+': $tape[$ptr] = !$tape[$ptr]; break;
            case ',':
                if ($iPtr % 8 == 0) {
                    $input = strlen($inputString) ? ord(substr($inputString, 0, 1)) : 0;
                    $inputString = strlen($inputString) ? substr($inputString, 1) : "";
                }
                $tape[$ptr] = $input & 1;
                $input >>= 1;
                $iPtr++;
            break;
            case ';':
                $output |= ($tape[$ptr] << ($oPtr % 8));
                if ($oPtr % 8 == 7) {
                    $r .= chr($output);
                    $output = 0;
                }
                $oPtr++;
            break;
            case '<':
                if (!$ptr) array_unshift($tape, 0);
                else $ptr--;
                break;
            case '>':
                if ($ptr == count($tape) - 1) array_push($tape, 0);
                $ptr++;
            break;
            case '[': if (!$tape[$ptr]) $i = $otoc[$i]; break;
            case ']': if ($tape[$ptr])  $i = $ctoo[$i]; break;
            default: break;
        }
    }

    if ($oPtr % 8) $r .= chr($output);
    return $r;
}

