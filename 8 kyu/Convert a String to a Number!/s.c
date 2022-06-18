544675c6f971f7399a000e79


int string_to_number(const char *src) {
    return atoi(src);
}
_______________________
int string_to_number(const char *src)
{
    int i,value=0,m;

    for(i=0; i<src[i] ; i++)
    {
        if(src[i]!='-')
        {
            m=src[i]-'0';   //converts every string to digit: ex '1' ->1 '2'->2 etc
                            // let say '9' value in ASCII is 56,  '0' value is 47 
                            // 56-47 = 9
            value=10*value+m; 
        }

    }
    if(src[0]=='-')   // if has sign converts the number to negativ
        value*=-1;

    return value;
}
_______________________
#include <stdio.h>
int string_to_number(const char *src) {
  
  int i;
  for(i=0; src[i+1] != '\0'; i++);
  int power = 0, num = 0;
  
  while(i>=0){
    
    if(src[i] == '-'){
      num *=-1;
      break;
    }
    
    int temp = src[i] - '0';
    for(int j=0; temp != 0 && j<power; j++) temp *= 10;
    num += temp;
    power++; i--;
  }
  
  return num;
}
_______________________
#include <string.h>
#include <stdlib.h>
#include <math.h>
int string_to_number(const char *src) {
  /*
  int x;
  int y = 0;
  int len = strlen(src);
  int neg_flag = (src[0] != '-' ? 0: 1);
  for(int i=0+neg_flag; i<len; i++) {
    x = pow(10,len-1-i) * ((int)src[i]-48);
    y += x;
  }
  y = (neg_flag == 0 ? y : -y);
  printf("%d\n",y);
  */
  int y = atoi(src);
  return y;
}
_______________________
#include <string.h>
#include <stddef.h>

int string_to_number(const char *src)
{
  if (!src || !src[0])
    return 0;
  
  int k = 1;
  int num = 0;
  
  for (size_t i = strlen(src) - 1; i != 0; i--)
  {
    num += (src[i] - '0') * k;
    k *= 10;
  }
    
  if (src[0] == '-')
    num = -num;
  else
    num += (src[0] - '0') * k;
  
  return num;
}
_______________________
#include<stdio.h>

int string_to_number(const char *src) 
{
  int length=0;
  int num = 0;
  int neg = 0;
  if(src[length]=='-')
        {
          neg =1;
          length++;
        }
  while(src[length]!='\0')
    {
      num+=src[length]-'0';
      num*=(src[length+1]=='\0' )? 1 : 10;
      length++;
    }
 
    if(neg)
      {
        num*=-1;  
      }


  return num;
}
_______________________
#include <stdio.h>
#include <string.h>

int string_to_number(const char *src) {
    size_t s = strlen(src);
    int r = 0;

    size_t i = (src[0] == '-') ? 1 : 0;

    for (; i < s; i++) {
        r = r * 10 + (src[i] - '0');
    }
    return (src[0] == '-') ? 0 - r : r;
}
_______________________
#include <stdlib.h>

int string_to_number(const char *src) {
  return atoi(src);
  return 0;
}
