58e230e5e24dde0996000070
  
  
bool isPrime(int num)
{
    for (int i = 2; i * i <= num; i++)
    {
        if (num % i == 0)
            return false;
    }
    return true;
}

int nextPrime(int num)
{
    if (num == 0 || num == 1)
        return 2;
    
    for (int i = num + 1; ; i++)
    {
        if (isPrime(i))
            return i;
    }
    return -1;
}
__________________________
#include<cmath>
int nextPrime(int n) {
  if(n<2){
    return 2;
  }
  for(int x=n+1;x<n*2;x++){
    bool t=true;
    for(int i=2;i<sqrt(x)+1;i++){
      if(x%i == 0){
        t=false;
        break;
      }
    }
    if(t){
      return x;
    }
  }
  return n;
}
__________________________
#include <math.h>
using namespace std;
bool isPrime(int x){
  for(int i=2; i<=sqrt(x); i++){
    if(x % i == 0){
      return false;
    }
  }
  return true;
}
int nextPrime(int n) {
  int count=0;
  if (n <= 1){
    return 2;
  }
  for(int i=n+1;i>0;i++){
    if(isPrime(i)==true){
      count=i;
      break;
    }
  }
  return count;
}
