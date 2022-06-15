function basicOp(operation, value1, value2)
{
  // Code
  // if + should be addition 
  // if - should be subtract
  // if * should be multiply 
  // if / should be division
  
  if(operation === '+'){
    return value1 + value2 
    }else if(operation === '-'){
    return value1 - value2 
    }else if(operation === '*'){
    return value1 * value2
    }else if(operation === '/'){
    return value1 / value2  
    }
  
}
________________________________
function basicOp (operation, value1, value2) {
  let result;
   switch(operation) {
      case '+': 
         result = value1 + value2;
         console.log(result)
         break;
      case '-':
         result = value1 - value2;
         console.log(result)
         break;
      case '*':
         result = value1 * value2;
         console.log(result)
         break;
      case '/':
         result = value1 / value2;
         console.log(result)
         break;
   }
  return result;
}

basicOp('+', 4, 7)
________________________________
function basicOp(operation, value1, value2) {
  switch (operation) {
    case '+':
      return value1 + value2;
    case '-':
      return value1 - value2;
    case '*':
      return value1 * value2;
    case '/':
      return value1 / value2;
    default:
      throw new Error('Please, provide a mathematical operation.');
  }
}
________________________________
function basicOp(operation, value1, value2) {
  const OPERATIONS = {
    '+': (val1, val2) => val1 + val2,
    '-': (val1, val2) => val1 - val2,
    '*': (val1, val2) => val1 * val2,
    '/': (val1, val2) => val1 / val2,
  };
  
  return OPERATIONS[operation](value1, value2);
}
________________________________
function basicOp(operation, value1, value2)
{
  let result;
  if(operation === '*') {
    result = value1 * value2;
  }
  if(operation === '+') {
    result = value1 + value2;
  }
  if(operation === '-') {
    result = value1 - value2;
  }
  if(operation === '/') {
    result = value1 / value2;
  }
  return result;
}
