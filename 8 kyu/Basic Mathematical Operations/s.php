function basicOp($op, $val1, $val2)
{
  switch ($op) {
    case '+':
      return $val1 + $val2;
    case '-':
      return $val1 - $val2;
    case '*':
      return $val1 * $val2;
    case '/':
      return $val1 / $val2;
  }
}
________________________________
function basicOp($op, $val1, $val2)
{
  switch ($op) {
    case '+':
      return $val1 + $val2;
      break;
    case '-':
      return $val1 - $val2;
      break;
    case '*':
      return $val1 * $val2;
      break;
    case '/':
      return (($val1 == 0 || $val2 == 0) ? 'This operation is impossible' : ($val1 / $val2));
      break;
  }
}
________________________________
interface BinaryOperator {
  public function perform($value1, $value2);
}

class AdditionOperator implements BinaryOperator {
  public function perform($value1, $value2) {
    return $value1 + $value2;
  }
}

class SubtractionOperator implements BinaryOperator {
  public function perform($value1, $value2) {
    return $value1 - $value2;
  }
}

class MultiplicationOperator implements BinaryOperator {
  public function perform($value1, $value2) {
    return $value1 * $value2;
  }
}

class DivisionOperator implements BinaryOperator {
  public function perform($value1, $value2) {
    return $value1 / $value2;
  }
}

function get_operator($op)
{
  switch ($op)
  {
    case '+': return new AdditionOperator();
    case '-': return new SubtractionOperator();
    case '*': return new MultiplicationOperator();
    case '/': return new DivisionOperator();
  }
}

function basicOp($op, $val1, $val2)
{
  $operator = get_operator($op);
  return $operator->perform($val1, $val2);
}
________________________________
function basicOp($o, $x, $y) {
  return eval("return $x $o $y;");
}
________________________________
function basicOp($op, $val1, $val2)
{
  if(in_array($op, array('+', '-', '*', '/')) && is_numeric($val1) && is_numeric($val2)) {
    switch($op) {
      case '+': return $val1 + $val2;
      case '-': return $val1 - $val2;
      case '*': return $val1 * $val2;
      case '/': return $val1 / $val2;
    }
  } else {
    return "Invalid input. Only numbers and arithmentic operators allowed.";
  }
}
