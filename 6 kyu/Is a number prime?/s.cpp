bool isPrime(int num) {
  for(int i = 2; i <= sqrt(num); i++) if(num % i == 0) return false;
  return num <= 1? false : true;
}
_________________________________
bool isPrime(int num) {
  // your code here..
  
 
   
  if(num==2 || num ==3 || num ==5) 
   return true;
  
  else if(num <=1 || num % 2 ==0 || num % 3 ==0) 
   return false;
  
  else
  {
    for(int i=5; i<=sqrt(num); i+=6 )
     if( (num % i==0) || (num % (i+2) == 0)) return false;
    
    return true;
  
  }
  
  
}

_________________________________
bool isPrime(int num) {
	if (num < 2)return false;
	int x = sqrt(num);
	for (int i = 2; i <= x; i++)if (num % i == 0) return false;
	return true;
}
_________________________________
bool isPrime(int num) {
  for (int i = 2; i <= num / i; i++) {
    if (num % i == 0) return false;
  }
  return num >= 2 ? true : false;
}
