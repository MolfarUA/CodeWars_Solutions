#include <stdbool.h>

const char *boolean_to_string(bool b)
{
    return b ? "true" : "false";
}
_________________________________
#include <stdbool.h>

const char *boolean_to_string(bool b) {
  static const char *const results[2] = {"false", "true"};
  return results[b];
}
_________________________________
#include <stdbool.h>
#include <stdlib.h>
//The returned string should be statically allocated and it won't be freed
const char *boolean_to_string(bool b)
{
  char *res = malloc(6-b);
  if(b == true) 
    {
    *(res)='t';
    *(res+1)='r';
    *(res+2)='u';
    *(res+3)='e';
    *(res+4)='\0';
  }
  else {
    *(res)='f';
    *(res+1)='a';
    *(res+2)='l';
    *(res+3)='s';
    *(res+4)='e';
    *(res+5)='\0';
    
  }
    return res; // your code here
}
