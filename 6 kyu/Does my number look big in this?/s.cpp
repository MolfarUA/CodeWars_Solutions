#include <cmath>
bool narcissistic( int value ){
  std::string a = std::to_string(value);
  int sum = 0;
  for(int i = 0; i < a.size(); i++){
    sum += pow(a[i]-48,a.size());
  }
  return sum == value;
}
________________________
#include <math.h>

bool narcissistic(int value) {
  std::string str = std::to_string(value);
  double res = 0;
  for (size_t i = 0; i < str.length(); i++)
  {
    res += pow((str[i] - '0'), str.length());
  }
  if (value == res)
    return true;
  else
    return false;
}
________________________
bool narcissistic( int value ){
  
  std::string num = std::to_string(value);
  int narc = 0;
  int length = num.length();
  int pow = 1;
  
  if (value == 0)
    return false;
  
  for(int i = 0; i < length; i++){
    pow = (num[i] - 48);
    for(int j = 1; j < length; j++){
      pow = pow * (num[i] - 48);
    }
    narc += pow;
  }
  
  if(value == narc)
    return true;
  else 
    return false;
}
________________________
#include <math.h>

int num_of_digits(int num){
  int counter = 0;
  if (num == 0){
    return 1;
  }
  int number = num;
  while (number != 0){
    number /= 10;
    counter++;
  }
  return counter;
}

bool narcissistic( int value ){
  int sum = 0;
  int val = value;
  int digits_number = num_of_digits(value);
  for (int i = 0; i < digits_number; i++){
    sum += pow((val % 10), digits_number);
    val /= 10;
  }
  return value == sum;
}
