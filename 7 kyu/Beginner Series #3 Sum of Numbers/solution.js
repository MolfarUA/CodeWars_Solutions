const GetSum = (a, b) => {
  let min = Math.min(a, b),
      max = Math.max(a, b);
  return (max - min + 1) * (min + max) / 2;
}

_______________________________________
function GetSum( a,b )
{
   if (a == b) return a;
   else if (a < b) return a + GetSum(a+1, b);
   else return a + GetSum(a-1,b);
}

_______________________________________
function GetSum(a,b)
{
  return (Math.abs(a - b) + 1) * (a+b) / 2;
}

_______________________________________
function GetSum( a,b )
{
  tmp = 0;
  
  if(a < b)
    while(a <= b) tmp += a++;
  else
    while(a >= b) tmp += a--;
      
  return tmp;
}

_______________________________________
function GetSum( a,b ) {
   var result = 0;
   var bigger = a > b ? a : b;
   var smaller = a > b ? b : a;
   for (var i = smaller; i <= bigger; i++) { result += i }
   return result
}

_______________________________________
function GetSum( a,b )
{
//if both a and b are equal return a
   if(a===b){
     return a;
   }
   var result = 0;
   
   var x = a, y = b;
 // check the larger and smaller numbers and assign them to x and y
   if(a > b) {
      x = b, y = a;
   }
 //in a loop add the numbers from the smaller one until it reaches the larger number
   for(var i = x; i <=y; i++ ) {
     result += i;
   }
   return result;
   
}

_______________________________________
function getSum( a, b ){
  return Array.from({length: b >= a ? b-a+1 : a-b+1}, (_, i)=> b >= a ? i+a : i+b).reduce((a, b)=> a + b, 0)
}
