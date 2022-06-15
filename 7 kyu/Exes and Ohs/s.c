#include <stdbool.h>

bool xo (const char* str)
{
  unsigned x = 0, o = 0;
  for (char *p = str; *p; p++) {
      if      (tolower(*p)=='x') x++;
      else if (tolower(*p)=='o') o++;
  }
  return x == o;
}
__________________________________
#include <stdbool.h>

bool xo (const char* str)
{
  int cnt_o=0;
  int cnt_x=0;
  while(*str){
    if(*str=='o'||*str=='O'){
      cnt_o++;
    }
    else if(*str=='x'||*str=='X'){
      cnt_x++;
    }
    *str++;
  }
  
  return cnt_o==cnt_x;
}
__________________________________
#include <stdbool.h>

bool xo(const char* str) {
  bool result = false;
  int x_count = 0;
  int o_count = 0;
  for (int i = 0; str[i] != '\0'; i++) {
    if (str[i] == 'x' || str[i] == 'X') {
      x_count += 1;
    } else if (str[i] == 'o' || str[i] == 'O') {
      o_count += 1;
    }
  }
  if (x_count == o_count) result = true;
  return result;
}
__________________________________
#include <stdbool.h>
#include <string.h>

bool xo (const char* str)
{ 
  size_t len = strlen(str);
  int sum = 0;
  for(size_t ch = 0; ch < len; ch++)
  {
      sum += ('o'==tolower(str[ch]));
      sum -= ('x'==tolower(str[ch]));
  }
  return (0 == sum);
}
__________________________________
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

bool xo (const char* str)
{
  size_t count_x = 0;
  size_t count_o = 0;
  
  while (*str)
  {
    if (tolower(*str) == 'x')
    {
      count_x++;
    }
    
    if (tolower(*str) == 'o')
    {
      count_o++;
    }
    
    str++;
  }
  
  
  return (count_x == count_o);
}
