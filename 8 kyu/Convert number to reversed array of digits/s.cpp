std::vector<int> digitize(unsigned long n) 
{
    std::vector <int> num;
    while(n!=0){
        num.push_back(n%10);//fetch the LSB of the number
        n = n / 10;//right shift the number
    }
    return num;
}
________________________
std::vector<int> digitize(unsigned long long n) 
{        
  std::vector<int> digits;
  for(;n>0;digits.push_back(n%10),n/=10);
  return digits;
}
________________________
std::vector<int> digitize(unsigned long n) 
{   
  std::vector<int> myVec;
  unsigned long val = n;
  do {
    myVec.push_back(val % 10);
    val = (val - (val % 10)) / 10;
  } while (val > 0);
  
  return myVec;
}
________________________
std::vector<int> digitize(unsigned long n) 
{        
  std::vector<int> digits;
  if(n==0){
    digits.push_back(n);
  }
  while(n>0){
    digits.push_back(n%10);
    n=n/10;
  }
  return digits;
}
