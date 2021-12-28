int get_sum(int a, int b)
{
  int n = (a < b ? b - a : a - b) + 1;
  return n *(a + b)/ 2;
}

_______________________________________
int get_sum(int a, int b)
{
  //Good luck!
  return (a + b) * (std::abs(a - b) + 1) / 2;
}

_______________________________________
int get_sum(int a, int b)
{
  // Gauss's formula.
  return (abs(a - b) + 1)*(a + b) / 2;
}

_______________________________________
#include <utility>

int get_sum(int a, int b)
{
  int sum = 0;
  if (a > b) std::swap(a, b);
  while (a != b) {
    sum += a;
    a++;
  }
  sum += b;
  return sum;
}

_______________________________________
int get_sum(int a, int b)
{
  int sum=0,i;
    if(a>b)
      {
      for(i=b;i<=a;i++)
      sum+=i;
    }
  else if(b>a)
    {
    for(i=a;i<=b;i++)
      sum+=i;
  }
  else
    sum=a;
return sum;
}

_______________________________________
int get_sum(int a, int b)
{
  return (a+b) * (abs(a-b) + 1) / 2;
}

_______________________________________
int get_sum(int a, int b)
{
  if(a==b){
    return a;
  }
  else if(a>b){
    return a+get_sum(a-1,b);
  }
  else {
    return b+get_sum(b-1,a);
  }
}
