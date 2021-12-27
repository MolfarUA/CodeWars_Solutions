function calc(string $expression) {
  $expression = preg_replace_callback(
    "/\((((?>[^()]+)|(?R))*)\)/", function($brackets) {
    return calc($brackets[1]);
  }, $expression
  );
  $expression = str_replace("--", "", $expression);
  $num = "\s*\-?\d+(?:\.\d+)?\s*";
  while (preg_match("/($num)([\*\/])($num)/", $expression, $action)) {
    switch ($action[2]) {
      case "*":
        $expression = str_replace($action[0], calc($action[1]) * calc($action[3]), $expression);
        break;
      case "/":
        $expression = str_replace($action[0], calc($action[1]) / calc($action[3]), $expression);
        break;
    }
  }
  while (preg_match("/($num)([\+\-])($num)/", $expression, $action)) {
    switch ($action[2]) {
      case "+":
        $expression = str_replace($action[0], calc($action[1]) + calc($action[3]), $expression);
        break;
      case "-":
        $expression = str_replace($action[0], calc($action[1]) - calc($action[3]), $expression);
        break;
    }
  }

  return $expression;
}
______________________________________________________
function calc(string $expression): float
{
    $expression = str_replace(' ', '', $expression);
    if ($expression[0] == '-') {
        $expression = 0 . $expression;
    }

    $index = lowestPriority($expression);
    if ($index > 0) {
        $left = calc(substr($expression, 0, $index));
        $right = calc(substr($expression, $index + 1));
        switch ($expression[$index]) {
            case '+':
                return $left + $right;
                break;
            case '-':
                return $left - $right;
                break;
            case '*':
                return $left * $right;
                break;
            case '/':
                return $left / $right;
                break;
        }
    }

    if ($expression[0] == '(' && substr($expression, -1) == ')') {
        return calc(substr($expression, 1, -1));
    }
    return (float)$expression;
}

function lowestPriority(string $expression): int
{
    $closed = 0;
    $secondaryIndex = 0;
    for ($index = strlen($expression) - 1; $index > 0; $index--) {
        $s = $expression[$index];
        if ($s == ')') {
            $closed++;
        }
        if ($s == '(') {
            $closed--;
        }
        if ($closed == 0) {
            if (($s == '+' || $s == '-') && notOperator($expression[$index - 1])) {
                return $index;
            }
            if (($s == '*' || $s == '/') && $secondaryIndex == 0) {
                $secondaryIndex = $index;
            }
        }
    }
    return $secondaryIndex;
}

function notOperator(string $char): bool
{
    switch ($char) {
        case '+':
        case '-':
        case '*':
        case '/':
            return false;
            break;
        default:
            return true;
    }
}
______________________________________________________
function getMaxBraceLevel(string $expression): int {
  $strLen = strlen($expression);
  $level = 0;
  $maxLevel = 0;
  for ($cursor = 0; $cursor < $strLen; $cursor++) {
    if ($expression[$cursor] === '(') {
      $level++;
    } else if ($expression[$cursor] === ')') {
      $level--;
    }
    $maxLevel = max($level, $maxLevel);
  }
  return $maxLevel;
}

function calcSubExpression(string $exp): string {
  $parts = preg_split('/(\/|\*|\+|-)/', $exp, 0, PREG_SPLIT_DELIM_CAPTURE);
  $parts = array_map('trim', $parts);
  $i = 2;
  while($i < count($parts)) {
    if ($parts[$i - 2] === '' && $parts[$i - 1] === '-') {
      if (isset($parts[$i + 2]) && $parts[$i] === '' && $parts[$i + 1] === '-') {
        array_splice($parts, $i - 2, 5, $parts[$i + 2]);
      } else {
        array_splice($parts, $i - 2, 3, '-' . $parts[$i]);
      }
    }
    $i++;
  }
  $operations = [
    '/' => function($a, $b) { return $a / $b; },
    '*' =>  function($a, $b) { return $a * $b; },
    '-' =>  function($a, $b) { return $a - $b; },
    '+' =>  function($a, $b) { return $a + $b; }
  ];
  foreach ($operations as $operator => $calcResult) {
    $i = 0;
    while($i < count($parts)) {
      if ($parts[$i] === $operator) {
        $result = $calcResult((float) $parts[$i - 1], (float) $parts[$i + 1]);
        array_splice($parts, $i - 1, 3, $result);
      } else {
        $i++;
      }
    }
  }
  return (string) $parts[0];
}

function calcExpressionPart(string $expression, int $start, int $end): string {
  $subExpression = substr($expression, $start + 1, $end - $start - 1);
  $result = calcSubExpression($subExpression);
  $result = str_pad($result, $end - $start + 1, ' ');
  $expression = substr($expression, 0, $start) . $result . substr($expression, $end + 1);
  return $expression;   
}

function calc(string $expression): float {
  $savedExp = $expression;
  $expression = '(' . $expression . ')';
  $strLen = strlen($expression);
  $maxBraceLevel = getMaxBraceLevel($expression);
  $level = 0;
  for ($maxLevel = $maxBraceLevel; $maxLevel >= 0; $maxLevel--) {
    $subExpressionStart = null;
    for ($cursor = 0; $cursor < $strLen; $cursor++) {
      if ($expression[$cursor] === '(') {
        $level++;
        $subExpressionStart = $cursor;
      } else if ($expression[$cursor] === ')') {
        if ($level === $maxLevel) {
          $expression = calcExpressionPart($expression, $subExpressionStart, $cursor);
        }
        $level--;
      }
    }
  }
  return (float) trim($expression, ' ');
}
