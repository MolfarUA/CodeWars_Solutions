int basic_op(char op, int value1, int value2) 
{
  switch (op)
  {
    case '+': return (value1 + value2);
    case '-': return (value1 - value2);
    case '*': return (value1 * value2);
    case '/': if (value2 != 0) return (value1 / value2);
    default: return 0;
  }
  return 0;
}
________________________________
int basic_op(char op, int x, int y) {
  switch(op) {
    case '+': return x + y;
    case '-': return x - y;
    case '*': return x * y;
    case '/': return x / y;
    default:  return x;
  }
}
________________________________
int basic_op(char op, int value1, int value2) {
  switch(op){
    case 43: return value1 + value2;  //43 = ASCII for "+"
    case 45: return value1 - value2;  //45 = ASCII for "-"
    case 42: return value1 * value2;  //42 = ASCII for "*"
    case 47: return value1 / value2;  //47 = ASCII for "/"
  }
  return 0;
}
________________________________
int basic_op(char op, int value1, int value2) {
  switch (op) 
  {
    case ('+'):
      return value1 + value2;
    case ('-'):
      return value1 - value2;
    case ('*'):
      return value1 * value2;
    case ('/'):
      return value1 / value2;
  }
}
________________________________
#define CHAR_MAX 127

int plus( int a, int b ) 
{
  return a + b;
}

int minus( int a, int b ) 
{
  return a - b;
}

int multiply( int a, int b ) 
{
  return a * b;
}

int divide( int a, int b ) 
{
  return a / b;
}

const int(* const operations[CHAR_MAX])(int, int) = 
{ 
  [ '+' ] = plus, 
  [ '-' ] = minus, 
  [ '*' ] = multiply, 
  [ '/' ] = divide 
};

int basic_op( char op, int value1, int value2 ) 
{
  return operations[ op ]( value1, value2 );
}
