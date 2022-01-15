unsigned single_digit(unsigned long long n) {
  while (n >= 10)
    n = __builtin_popcountll(n);
  return n;
}
__________________________
typedef unsigned long long uint64;
uint64 hamming_weight(uint64 n) { return (n & 1) + (n == 0 ? 0 : hamming_weight(n >> 1)); }
uint64 single_digit(uint64 n) { return n > 9 ? single_digit(hamming_weight(n)) : n; }
__________________________
unsigned single_digit (unsigned long long n)
{
  while (n >= 10) n = __builtin_popcountl(n);
  return n;
}
__________________________
unsigned single_digit(unsigned long long n) {
    return n > 9u ? single_digit(__builtin_popcountll(n)) : n;
}
__________________________
unsigned single_digit (unsigned long long n)
{
  if(n<10) return n;
  unsigned f=0;
      while(n)
      {
          (n&1)==1? f++: f;
          n>>=1;
      }
  return f<10? f: single_digit(f);
}
__________________________
unsigned single_digit (unsigned long long n)
{
   unsigned long long total = n;
  
   while (total >= 10) 
   {  
       unsigned long long input_val = total;
       total = 0;
       while (input_val > 0) 
       {
           total += (input_val & 1);
           input_val >>= 1;
       }
   }
   return total;
}
__________________________
unsigned single_digit (unsigned long long n)
{
  if(n<10){
    return n;
  }
  int sum=0,i=1,arr[100],j=0,sum1=0;
  while(1){
    arr[j]=n%2;
    sum+=arr[j];
    j+=1;
    i*=10;
    n/=2;
    if (n==0 && sum>9){
      n=sum;
      sum=0;
      j=0;
      i=1;
    }
    if(n==0 && sum<10){
      break;
    }
  }
  for(i=0;i<j;i++){
    sum1+=arr[i];
  }
  return sum1;
}
