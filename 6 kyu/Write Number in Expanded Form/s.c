5842df8ccbd22792a4000245


#include <string.h>
#include <stdlib.h>

char *expandedForm(char *string, unsigned long long n)
{
  char *s;
  char *tmp;
  memset(string, 0, strlen(string));
  asprintf(&s, "%llu", n);
  for(size_t i = 0; i < strlen(s); i++){
    if(*(s+i) != '0'){
      tmp = (char*)calloc(sizeof(char), strlen(s) - i + 1);
      *tmp = *(s+i);
      for(int j = 0; j < strlen(s) - i - 1; j++) 
        *(tmp + 1 + j) = '0';
      if(i != 0) string = strcat(string, " + ");
      string = strcat(string, tmp);
     }
  }
  return string;
}
_________________________
#include <stdio.h>

typedef unsigned long long ull;

ull get_max_term (ull n)
{
  return (n < 10) ? n : (10 * get_max_term(n / 10));
}

char *expandedForm(char *string, ull n)
{
  ull term = get_max_term(n);
  char *next = string + sprintf(string, "%llu%s", term, (term == n) ? "" : " + ");
  if (term != n)
    expandedForm(next, n - term);
  return string;
}
_________________________
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

char *expandedForm(char *o, unsigned long long n)
{
  char* s = calloc(21,sizeof(char));
  sprintf(s, "%llu", n);
  unsigned long l = strlen(s);
  unsigned long j = 0;
  for (unsigned long i = 0; i < l ; i++){
    if (s[i]=='0')continue;
    o[j++] = s[i];
    for (unsigned long k = i+1 ; k < l ; k++) {
      o[j++] = '0';
    }
    o[j++] = ' ';
    o[j++] = '+';
    o[j++] = ' ';
  }
  o[j - 3]='\0';
  return o;
}
