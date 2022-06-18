57eb8fcdf670e99d9b000272


#include <stdlib.h>
#include <string.h>

/*
** @param str: a C-string containing only lowercase letters and spaces (' ')
** @return:    a C-string allocated on the heap containing the highest scoring word of str
*/
char  *highestScoringWord(const char *str)
{
    int len, score, high_score, index, i;
    char* ret_string;
    
    len = strlen(str);
    ret_string = malloc(len);
    score = 0;
    high_score = -1;
    index = 0;
    for(i = 0; i <= len; i++)
    {
        if(str[i] == ' ' || str[i] == '\0')
        {
            if(score > high_score)
            {
                high_score = score;
                strncpy(ret_string, str + index, i - index);
                ret_string[i - index] = '\0';
            }
            index = i + 1;
            score = 0;
        }
        else
            score += str[i] - 96;
    }
    return (ret_string);
}
_____________________________________________
#include <string.h>

static int scoreWord(char* word) {
    int score = 0;
    for ( char* letter = word ; *letter ; letter++ ) {
        score += *letter - 'a' + 1;
    }
    return score;
}

char  *highestScoringWord(const char *str)
{
    char *copy = strdup( str );
    
    char *token = strtok( copy, " " );
    char *result = strdup( token );  // Malloc
    int highScore = scoreWord( result );
    
    while( token != NULL ) {
        int newScore = scoreWord( token );
        if ( newScore > highScore ) {
            free( result );  // Free
            result = strdup( token ); // Malloc
            highScore = newScore;
        }
        token = strtok( NULL, " " );
    }
    free( copy );
    return result;
}
_____________________________________________
#define _GNU_SOURCE
#include <string.h>
#include <stdlib.h>

int word_score(char *s) { return *s ? *s - 'a' + 1 + word_score(s + 1) : 0; }

char *highestScoringWord(const char *str)
{
  char *dup = strdup(str), *hi = NULL;
  int max = 0, n;
   
  for (char *wrd = strtok(dup, " "); wrd; wrd = strtok(NULL, " "))
    if ((n = word_score(wrd)) > max) max = n, hi = wrd;
  
  return hi = strdup(hi), free(dup), hi;
}
_____________________________________________
#include <stdlib.h>
#include <string.h>

char  *highestScoringWord(const char *str)
{
    int len = strlen(str);
    
    int max = 0;
    int actual = 0;
    int start = 0;
    int where = 0;
    
    for(int i=0; i <= len; i++){
                
        if( (str[i] == ' ') || (str[i] == '\0') ){
            if(max < actual){
                max = actual;
                where = start;
            }
            actual = 0;
            start = i+1;
            continue;
        }
        actual += str[i] - 'a' + 1;
    }
    
    char * result = (char *)calloc(len, sizeof(char));
    
    int index = 0;
    for(int i=where; (str[i] != ' ') && (str[i] != '\0'); i++) result[index++] = str[i];
    
    result = (char *)realloc(result, sizeof(char)*(strlen(result)+1));
    
    return result;
}
_____________________________________________
/*
** @param str: a C-string containing only lowercase letters and spaces (' ')
** @return:    a C-string allocated on the heap containing the highest scoring word of str
*/
#include <ctype.h>
#include <stdlib.h>

char  *highestScoringWord(const char *str)
{
  const char* word = NULL;
  const char* begin = str;
  int max = 0;
  int count =0;
  
  for(int i = 0; str[i]; i++)
  {
    if(str[i] != ' ')
    {
      count += tolower(str[i]) - 'a' + 1;
    }
    else
    {
      if(count > max)
      {
        word = begin;
        max = count;
      }
      begin = &str[i + 1];
      count = 0;
    } 
  }
 
  if(count > max)
    {
      word = begin;
      max = count;
  }

  count = 0;
  for(int i = 0; word[i] != ' ' && word[i] != 0; i++)  
  {
    count++;
  }
  char* dest = malloc(count + 1);
  strncpy(dest , word, count);
  dest[count] = 0;
  return dest;
}
_____________________________________________#include <string.h>
#include <stdlib.h>
/*
** @param str: a C-string containing only lowercase letters and spaces (' ')
** @return:    a C-string allocated on the heap containing the highest scoring word of str
*/
char *highestScoringWord(const char *str)
{
  char *toHeap = strdup((char *) str), *word = strtok(toHeap, " "), *out;
  unsigned int amount = 0, highest = 0;

  do {
    for (char *cpy = word; *cpy; cpy++) amount += *cpy - (('a') - 1);
    if (highest < amount) out = word, highest = amount;
    amount = 0;
  }  while ( (word = strtok(NULL, " ")) );
  
  out = strdup(out);
  free(toHeap);
  return out;
}
