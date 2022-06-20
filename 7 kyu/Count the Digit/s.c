566fc12495810954b1000030


int nbDig(int n, int d) {
  int count = (d == 0) ? 1 : 0;
  
  for (int k = 1; k <= n; k++) {
    int kk = k * k;
    while (kk != 0) {
      if (kk % 10 == d)
        count++;
      kk /= 10;
    }
  }
  
  return count;
}
____________________________
int nbDig(int n, int d) {
  int i, c = 0, val;
  for(i=0; i <= n; i++)
  {
      val=i*i;
      while (val > 0) 
      {
        if((val % 10) == d) c++;
        val /= 10;
      }
    } 
    if(val == d) c++;
    return c;
}
____________________________
#include <stdio.h>
#include <stdlib.h>

int nbDig(int n, int d) {
  int count = 0;
  for (int k = 0; k <= n; ++k) {
    int m = k * k;
    do {
      if ((m % 10) == d) count += 1;
      m /= 10;
    } while(m);
  }
  return count;
}
____________________________
int nbDig(int n, int d) {
  int count = 0;
  char str[10];
  for(int k = 0; k <= n; k++) {
    int sum = 0;
    sprintf(str, "%d", k*k);
    for (char *p = str; *p; ++p)
      if (*p-'0' == d)
        ++sum;
    count += sum;
  }
  return count;
}
____________________________
#include <stdlib.h>
#include <stdio.h>

int countDigits(int num, int x)
{
    int result = 0;
    char *s_num = malloc(sizeof(char) * 20);
    sprintf(s_num, "%d", num);
    while (*s_num) {
        if (*s_num == x + '0')
            result++;
        s_num++;
    }
    return result;
}

int nbDig(int n, int d) {
    int result = 0;
    short i = 0;
    for (i = 0; i <= n; i++) {
        result += (countDigits((i * i), d));
    
    }
    return result;
}
