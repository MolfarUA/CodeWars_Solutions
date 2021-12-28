int get_sum(int a , int b) {
    
    int start = b;
    int finish = a;
    
    if (a < b){
      start = a;
      finish = b;
    }
      
    int sum = 0;  
    for (; start <= finish; start++){
      sum += start;
    }
    
    return sum;
}

__________________________________
int get_sum(int a, int b) 
{
   return ((a + b) * 0.5)*(abs(a - b) + 1);
}

__________________________________
int get_sum(int a , int b) {
    if(a == b){
      return a;
    }
    int max, min;
    max = a > b ? a : b;
    min = a < b ? a : b;
    int sum = 0;
    
    for(int i = min; i <= max; i++){
      sum += i;
    }
    return sum;
}

__________________________________
int get_sum(int a , int b) 
{
  int c = 0;
  
  if (a < b)
  {
    while (a != b)
    {
      c += a;
      a++;
    }
    c += a;
    return (c);
  }
  else if (b < a)
  {
    while (b != a)
    {
      c += b;
      b++;
    }
    c += b;
    return (c);
  }
  else (a == b);
    return (a);
}

__________________________________
int get_sum(int a , int b) {
  int max = a > b ? a : b;
  int min = a < b ? a : b;
  int item = a + b;
  int nb_item = max - min + 1;
  return (item*nb_item)/2;
}
