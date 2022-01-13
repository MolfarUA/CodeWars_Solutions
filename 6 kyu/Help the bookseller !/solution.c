#include <stdio.h>

char* stockSummary(char** lstOfArt, int szlst, char** categories, int szcat) {
  char r[4096]={0};
  int i, j, v, s, l=3;
  if(szlst&&szcat) {
    for(i=0;i<szcat;i++) {
      for(s=0,j=0;j<szlst;j++)
        if(lstOfArt[j][0]==categories[i][0])
          if(sscanf(lstOfArt[j], "%*s %d", &v)) s+=v;
      l=sprintf(r, "%s(%c : %i) - ", r, categories[i][0], s);
    }
  }
  r[l-3]=0;
  return strdup(r);
}
________________________________________
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define MAX_INT_CHARSPACE 32

char getBookCategory(const char bookstr[]){
  return bookstr[0];
}

int getBookCnt(const char bookstr[]){
  int res = 0;
  char *resstr = (char*) calloc(128, sizeof(char));
  size_t resstr_len = 0;
  for (size_t i = 0; i < strlen(bookstr); i++){
    if (bookstr[i] == ' '){
      i++;
      
      while (i < strlen(bookstr)){
        resstr[resstr_len++] = bookstr[i];
        i++;
      }
      
    } 
  }
  sscanf(resstr, "%d", &res);
  
  free(resstr);
  return res;
}

char *stockSummary (
  const char *const books[], size_t nb_books,
  const char *const categories[], size_t nb_categories
  )  
{
  char *resstr;
  int resstring_cap = 1;
  
  if (!nb_books || !nb_categories){
    char *resstr = malloc(resstring_cap * sizeof(char));
    resstr[0] = '\0';
    return resstr;
  }
  
  int *resMap = (int*) calloc(nb_categories,sizeof(int));
  
  for (size_t i = 0; i < nb_categories; i++){
     for (size_t j = 0; j < nb_books; j++){
       if (categories[i][0] == getBookCategory(books[j]) ){
         resMap[i] += getBookCnt(books[j]);
       }
     }  
  }
  
  for (size_t i = 0; i < nb_categories; i++){
    //(:) + space charspaces
    resstring_cap += 5;
    //cathegory charspace  
    resstring_cap += 1;
    //int charspaces
    resstring_cap += MAX_INT_CHARSPACE;
    //delimiter charspaces
    resstring_cap += 3;
  };
  //remove last delimiter
  resstring_cap -= 3;
  
  resstr = malloc(resstring_cap * sizeof(char));
  int char_cnt = 0;
  for (size_t i = 0; i < nb_categories; i++){
    resstr[char_cnt++] = '(';
    resstr[char_cnt++] = *categories[i];
    resstr[char_cnt++] = ' ';
    resstr[char_cnt++] = ':';
    resstr[char_cnt++] = ' ';
    
    char cnt[MAX_INT_CHARSPACE];
    sprintf(cnt, "%d", resMap[i]);
    for (size_t j = 0; j < strlen(cnt); j++){
      resstr[char_cnt++] = cnt[j];
    }
    resstr[char_cnt++] = ')';
    
    if ( (i + 1) != nb_categories){
      resstr[char_cnt++] = ' ';
      resstr[char_cnt++] = '-';
      resstr[char_cnt++] = ' ';
    }else{
      resstr[char_cnt++] = '\0';
    }
  }
 
  free(resMap);
  
  resstr = realloc(resstr,char_cnt);
  return resstr;

}
________________________________________
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

char *stockSummary (const char *const books[], size_t nb_books,
          const char *const categories[], size_t nb_categories)
{ 
  int suma, pocet;
  unsigned long int a, i;
  char kniha[40], pismeno[2], retazec[1000], sum[40];
 
  retazec[0] = '\0';
  if(*books==NULL || *categories==NULL){
    strcat(retazec,"");
  }
  else
  {
    for(a=0; a<nb_categories; a++){
      suma=0;
      for(i=0; i<nb_books; i++){
        sscanf(books[i],"%s %d",kniha, &pocet);
        sscanf(categories[a],"%s",pismeno);
        if(kniha[0]==pismeno[0]){
          suma+=pocet;
        }     
      }   
      sprintf(sum,"%d", suma);
      strcat(retazec,"(");
      strcat(retazec,categories[a]);
      strcat(retazec," : ");
      strcat(retazec,sum);
      strcat(retazec,")");
      if(a<nb_categories-1){
        strcat(retazec," - ");
      }
    }
  }
  char *buffer = calloc(strlen(retazec)+1,sizeof(char));
  for(i=0; i<strlen(retazec); i++){
    buffer[i] = retazec[i];
  }
   
  return buffer;
}
________________________________________
#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>

int extractNumber(const char* entry) {
    bool found_space = false;
    char* num = (char*) calloc(256, sizeof(int));
    for (size_t i = 0; i < strlen(entry); i++) {
        if (entry[i] == ' ') found_space = true;
        else if (found_space) num[strlen(num)] = entry[i]; 
    }
    int res = atoi(num);
    free(num);
    return res;
}

char *stockSummary(const char *const books[], size_t nb_books, const char *const categories[], size_t nb_categories) {
    char* res = (char*) calloc(512, sizeof(char));
    if (nb_books * nb_categories == 0) return res;
    int amount[256] = {0};
    for (size_t i = 0; i < nb_books; i++) {
        amount[books[i][0] - 'A'] += extractNumber(books[i]);
    }
    for (size_t i = 0; i < nb_categories; i++) {
        char ltr = categories[i][0];
        bool last = (i == nb_categories - 1);
        sprintf(res, "%s(%c : %d)%s", res, ltr, amount[ltr - 'A'], last ? "" : " - ");
    }
    return res;
}
________________________________________
#include <stdlib.h>
#include <string.h>
#include <ctype.h>


char *stockSummary(const char *const b[], size_t length,
                   const char *const c[], size_t length2)
{
            if(length==0||length2==0)return strdup("");

    int map[128]={-1};
    int toMinus=129;
    unsigned int i,j;

//map = -1
    while(toMinus--)
    map[toMinus]=-1;

//if 'A' then map[A] to 0
    for(i=0;i<length2;i++)
    map[c[i][0]]+=1;


    for(i=0;i<length;++i){
        for(j=0;j<length2;j++)
            if(*b[i]==*c[j]){
char *p = strdup(b[i]);
    long val=0;
while (*p) { // While there are more characters to process...
    if ( isdigit(*p) || ( (*p=='-'||*p=='+') && isdigit(*(p+1)) )) 
        // Found a number
        val = strtol(p, &p, 10); // Read number
     else 
        // Otherwise, move on to the next character.
        p++;
    
}
map[c[j][0]]+=val;
            }
        }
        char*result=(char*)malloc(10000);
        char* temp=(char*)malloc(10000);
        int check=0;
        for(i=0;i<length2;i++)
            if(map[c[i][0]]>=0){
            check++;
            if(check==1)
            sprintf(result,"(%c : %d)",c[i][0],map[c[i][0]]);
            else{
            sprintf(temp," - (%c : %d)",c[i][0],map[c[i][0]]);
            strcat(result,temp);
            }
            }
  free(temp);
    return result; // memory will be freed
}
