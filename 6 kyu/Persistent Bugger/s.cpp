int persistence(long long n) {
  long long p = 1;
  if (n < 10) { return 0; } 
  while (n > 0) { p = (n % 10) * p; n = n/10; }
  return persistence(p) + 1;
}
________________________________________
int persistence(long long n){
    int count=0,mul=1;
    std::string one=std::to_string(n);

    while(one.length()>1){
        mul=1;
        for(int i=0;i<one.length();i++)
            mul*=(one[i]-'0');
      
        one=std::to_string(mul);
        count++;
    }

    return count;
}
________________________________________
int persistence(long long n){
  int steps = 0;
  for (long long sum = 1; n > 9; n = sum, sum = 1, steps++)
    for (; n != 0; n /= 10)
      sum *= n%10;
  return steps;
}
________________________________________
int persistence(long long n){
  int steps = 0;
  for (long long sum = 1; n > 9; n = sum, sum = 1, steps++)
    for (long long tmp = n; tmp != 0; tmp /= 10)
      sum *= tmp%10;
  return steps;
}
________________________________________
#include <string>
#include <cstdio>
#include <vector>

int persistence(long long n)
{
  int count{0};
  while (n>9)
  {
     long long int k {n};
     long long int size {0};
     long long int l{1};
      while (k>0)
      {
        k/=10;
        size++;
      }
      std::string s ("",size);
      sprintf((char*)s.c_str(),"%lli",n);
      std::vector<char> vec1 {};
      std::vector<int> vec3 (vec1.size()); 
        for (unsigned int i = 0 ; i < s.size(); i++)
          {
            vec1.push_back(s[i]);
            vec3[i]=vec1[i]-'0';
            l*=vec3[i];
          }
      n=l;
      count++;
  }
  return count;
}
