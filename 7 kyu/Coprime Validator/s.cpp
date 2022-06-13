#include <numeric>

bool are_coprime(unsigned a, unsigned b) {
  return std::gcd(a, b) == 1;
}
___________________________
bool are_coprime(unsigned int a, unsigned int b) {
    if (b <2) return b==1;
    return are_coprime(b, a%b);
}
___________________________
#include <cmath>
bool are_coprime(unsigned int a, unsigned int b) {
  for(int i = 2; i<fmax(a,b); i++){
    if ((a%i == 0)&&(b%i == 0)){
      return false;
    }
  }
  return true;
}
___________________________
bool are_coprime(unsigned int a, unsigned int b) {
  std::vector<int> fcA;
  std::vector<int> fcB;
  std::cout << a << ", " << b << std::endl;
  for(unsigned int i = 1; i<= a; i++ ){
    if(a % i == 0){
      fcA.push_back(i);
    }
  }
  for(unsigned int i = 1; i <= b; i++){
    if(b % i == 0) {
      fcB.push_back(i);
    }
  }
  for(unsigned int i = 0; i < fcA.size(); i++){
    int valueA = fcA[i];
    if(valueA > 1 ){
      for(unsigned int j = 0; j < fcB.size(); j++){
        int valueB = fcB[j];
        if(valueB == valueA){
          return false;
        }
      }
    }
  }
  return true;
}
___________________________
#include <math.h>
using namespace std;

bool are_coprime(unsigned int a, unsigned int b) {
  
  int minVal = a<b?a:b;
  bool coPrime = true;
  
  for(int i = 2; i<=floor(minVal/2);i++){
    
    if(a%i == 0 && b%i == 0) {
      coPrime = false; break;
    }
  }
  
  if(a%minVal == 0 && b%minVal == 0) coPrime = false;
  return coPrime;
}
