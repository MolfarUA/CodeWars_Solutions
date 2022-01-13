import 'dart:math';

bool isSquare(num n) => sqrt(n) % 1 == 0;
__________________________________
import 'dart:math';

var isSquare = (n) => sqrt(n).remainder(1) == 0;
__________________________________
isSquare(n) { 
  for(var i = 0; i <= n; i++){
    if(i*i == n)
      return true;
  }
  return false;
}
__________________________________
import 'dart:math';
bool isSquare(int n) => n>=0 && sqrt(n) == sqrt(n).round();
__________________________________
import "dart:math";
bool isSquare(n) { 
var ra = sqrt(n);
return (ra%1==0) ?  true:  false;
  
}
