function parse(data) {
  let res = [];

  data.split('').reduce((cur, s) => {
    if (s === 'i') cur++;
    if (s === 'd') cur--;
    if (s === 's') cur = Math.pow(cur, 2);
    if (s === 'o') res.push(cur);
    
    return cur;
  }, 0);
  
  return res;
}
__________________________________________
onst parse = data => {
  const Commands = {
      INCREMENT:  'i',
      DECREMENT:  'd',
      SQUARE:     's',
      OUTPUT:     'o'
  }

  var outputs = [],
      value = 0;
  
  data.split('').forEach(command => {
    switch(command) {
      case Commands.INCREMENT:  value++;                   break;
      case Commands.DECREMENT:  value--;                   break;
      case Commands.SQUARE:     value = Math.pow(value, 2);break;
      case Commands.OUTPUT:     outputs.push(value);       break;
    }
  });
  
  return outputs;
}
__________________________________________
// Return the output array, and ignore all non-op characters
function parse( data )
{
  res = []
  i = 0
  data.split("").forEach(e => {
    switch(e){
        case 'i':
          i++
          break
        case 'd':
          i--
          break
        case 's':
          i=i**2
          break
        case 'o':
          res.push(i)
          break
    }
  })
  return res
}
__________________________________________
function parse( data ) {
  let arr = [];
  let num = 0;
  
  for (let i=0; i< data.length; i++) {
    switch(data[i]) {
      case 'i':
        num +=1;
        break;
        
      case 'd':
        num-=1;
        break;
        
      case 's':
        num*=num;
        break;
        
      case 'o':
        arr.push(num);
        break;
    }
  }
  return arr;
}
__________________________________________
const parse = data => {
  let currValue = 0, array = [];
  
  for (let i in [...data]) {
    if (data[i] == 'i') currValue += 1;
    if (data[i] == 'd') currValue -= 1;
    if (data[i] == 's') currValue *= currValue;
    if (data[i] == 'o') array.push(currValue);
  }
    
  return array;
}
