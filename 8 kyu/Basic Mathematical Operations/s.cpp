int basicOp(char op, int val1, int val2) {
  switch(op) {
    case '+': return val1+val2;
    case '-': return val1-val2;
    case '*': return val1*val2;
    case '/': return val2 != 0 ? val1/val2 : 0;
    }
}
________________________________
int basicOp(char op, int val1, int val2) {
  switch (op) {
    case '+': return val1 + val2;
              break;
    case '-': return val1 - val2;
              break;
    case '*': return val1 * val2;
              break;
    case '/': return val1 / val2;
              break;
    default: return -99999;
  }
}
________________________________
int basicOp(char op, int val1, int val2) 
{
  switch (op)
  {
    case '+':
      return val1 + val2;
    case '-':
      return val1 - val2;
    case '*':
      return val1 * val2;
    case '/':
      return val1 / val2;
  }
  return 0;
}
________________________________
int basicOp(char op, int val1, int val2)
{
    try
    {
        switch (op)
        {
        case '+': return val1 + val2;
        case '-': return val1 - val2;
        case '*': return val1 * val2;
        case '/':
            if (val2 == 0) throw std::invalid_argument("Can't divide by 0");
            return val1 / val2;
        default: throw std::invalid_argument("Invalid operator");
        }
    }
    catch (const std::invalid_argument& e)
    {
        std::cerr << "Exception: " << e.what() << std::endl;
    }
}
________________________________
int basicOp(char op, int val1, int val2) {
  if (op == '+') {
    return val1 + val2;
  }
  if (op == '-') {
    return val1 - val2;
  }
  if (op == '*') {
    return val1 * val2;
  }
  if (op == '/') {
    return val1 / val2;  // Divison by zero is undefined.
  }
}
