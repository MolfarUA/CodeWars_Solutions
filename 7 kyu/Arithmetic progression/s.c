55caf1fd8063ddfa8e000018


#include <stdlib.h>

char *arithmetic_sequence_elements(int a, int d, size_t n)
{ 
  char *result = (char*)calloc(n*11,sizeof(char));
  
  if(n==0)
    return result;
  if(n>1)
    sprintf(result,"%d, ",a);
  else if(n==1)
    sprintf(result,"%d",a);
  for(int i=1;i<n;i++,a+=d){
    if(i==n-1)
      sprintf(result+strlen(result),"%d",a+d);
    else
      sprintf(result+strlen(result),"%d, ",a+d);
  }
    
  return result;
}
___________________________
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

char *arithmetic_sequence_elements(int a, int d, size_t n)
{
  char *result = calloc(1, sizeof(char));
  char tmp[128]; // big enough. Feel lazy to calculate correct size depending on system
  
  for (size_t i = 0; i < n; i++)
  {
    sprintf(tmp, "%li, ", a + d * i);
    result = realloc(result, strlen(tmp) + strlen(result) + 1);
    strcat(result, tmp);
  }
  // remove last ", "
  result[strlen(result) - 1] = '\0';
  result[strlen(result) - 1] = '\0';
  
  return result;
}
___________________________
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

char *arithmetic_sequence_elements(int a, int d, size_t n)
{
  char* result;
  result = malloc(n * 10);
  result[0] = '\0';
  char elem[10];
  elem[0] = '\0';
  for (int i = 0; i < (int)n; i++) {
    sprintf(elem, "%d%c", a + i*d, '\0');
    strcat(result, elem);
    if (i != (int)n - 1)
      strcat(result, ", ");
  }
  return result;
}

