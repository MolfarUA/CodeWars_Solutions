int find_even_index(const int *values, int length) {
  int sum = 0;
  
  for(int i = 0; i < length; i++) sum += values[i];
  
  int left = 0;
  int right = sum;
  
  for(int i = 0; i < length; i++)
  {
    right -= values[i];
    if(left == right) return i;
    left += values[i];
  }
  return -1;
}
________________________
int find_even_index(const int *values, int length) {
  int i, sum, left, right;
  
  sum = 0;
  for (i = 0; i < length; i++) sum += values[i];
  
  left = 0;
  for (i = 0; i < length; i++) {
    right = sum - left - values[i];
    
    if (left == right) return i;
    
    left += values[i];
  }
  
  return -1;
}
________________________
int total_sum(const int *values, int length) 
{
    int sum = 0;
    int i = 0;
    for (i = 0; i < length; i++)
    {
        sum += values[i];
    }

    return sum;
}

int left_sum(const int *values, int index) 
{
    int lsum = 0;
    int i = 0;
    for (i = 0; i < index; i++)
    {
        lsum += values[i];
    }
    return lsum;
}

int find_even_index(const int *values, int length) 
{
    int index = -1;
    int LeftSum = 0;
    int TotalSum = 0;
    int RightSum = 0;
    TotalSum = total_sum(values, length);
    
    int i = 0;
    for (i = 0; i < length; i++) 
    {
        LeftSum = left_sum(values, i);
        RightSum = TotalSum - LeftSum - values[i];
        if (LeftSum == RightSum)
        {
            index = i;
            break;
        }
    }
    return index;
}
________________________
int find_even_index(const int *values, int length) {
  int left = 0, right = 0, i = 0;
  for(i=0;i<length;i++)   right+=values[i];
  if(!right)  return 0;
  for(i=0;i<length;i++)
  {
    right-=values[i];  
    if(left==right) return i;
    left+=values[i];    
  }
  return -1;
}
________________________
int find_even_index(const int *values, int length) {
  int acc = 0, lft = 0;
  for(int i = 0; i != length; i++) acc += values[i];
  for(int i = 0; i != length; i++){
    acc -= values[i];
    if(acc == lft) return i;
    lft += values[i];
  }
  return -1;
}
