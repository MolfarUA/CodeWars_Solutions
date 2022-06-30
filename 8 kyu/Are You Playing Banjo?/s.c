53af2b8861023f1d88000832



char* are_you_playing_banjo(const char* n) {
  char *r = (char*)calloc(strlen(n) + 20, 1);
  strcpy(r, n);
  strcat(r, (n[0] == 'R' || n[0] == 'r') ? " plays banjo" : " does not play banjo");
  return r;
}
________________________________
#include <stdio.h>

char* are_you_playing_banjo(const char* name) {
  const char* banjo = (name[0] == 'R' || name[0] == 'r')
    ? " plays banjo"
    : " does not play banjo";
  char* ret = NULL;
  asprintf(&ret, "%s%s", name, banjo);
  return ret;
}
________________________________
#define _GNU_SOURCE
#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>

char *are_you_playing_banjo(const char *name) {
  char *result; 
  if(tolower(name[0]) == 'r'){
    asprintf(&result, "%s plays banjo", name);
  } else {
    asprintf(&result, "%s does not play banjo", name);
  }
  return result;
}
________________________________
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
 int i=0 ;

char *are_you_playing_banjo(const char *name)
{
   char * str_ret1="plays banjo" ;   char * str_ret2 ="does not play banjo";   char * NEW_str_ret = NULL ;
   int str_ret1_len ,str_ret2_len,NEW_str_len,name_len, j=0;
   str_ret1_len = strlen(str_ret1)   ;  str_ret2_len = strlen(str_ret2) ;    name_len= strlen(name) ;
  
  if ((name[0] == 'R') || (name[0] == 'r')) 
  {  
  NEW_str_ret = (char *)malloc( sizeof(char) * (str_ret1_len+name_len+1) ) ;  
  for(i = 0 ; i < name_len ; i++) {  NEW_str_ret[i] = name[i]     ; } 
  NEW_str_ret[name_len] =32 ; i++ ;
  for(j=0 ;  j <=str_ret1_len ;  j++)  {  NEW_str_ret[name_len+j+1] = str_ret1[j]   ;  i++ ;       } 
  }
  
  else 
   { 
  NEW_str_ret = (char *)malloc( sizeof(char) * (str_ret2_len+name_len+1) ) ;
  for(i = 0 ; i < name_len ; i++) {  NEW_str_ret[i] = name[i]     ; } 
  NEW_str_ret[name_len] =32 ; i++ ;
  for(j=0 ;  j <=str_ret2_len ;  j++)  {  NEW_str_ret[name_len+j+1] = str_ret2[j]   ;  i++ ;       } 
   }
  
  return NEW_str_ret ;
}
