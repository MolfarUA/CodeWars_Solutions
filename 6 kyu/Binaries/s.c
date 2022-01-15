#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct {
  char digit;
  char *coded;
  int length;
} convert[] = { {'0', "10", 2}, {'1', "11", 2}, {'2', "0110", 4}, {'3', "0111", 4}, {'4', "001100", 6}, {'5', "001101", 6},\
{'6', "001110", 6}, {'7', "001111", 6}, {'8', "00011000", 8}, {'9', "00011001", 8}};

char* code(const char* strng){
  char *coded = (char *) malloc(8 * sizeof(char) * strlen(strng));
  *coded = '\0';
  
  for (; *strng != '\0'; strng++)
    strcat(coded, convert[*strng-'0'].coded);
    
  return coded;
}

char* decode(const char* str){
  const char *ptr = str;
  char *decoded = (char *) malloc(strlen(str) * sizeof(char));
  *decoded = '\0';
  
  while (*ptr != '\0')  
    for (int i = 0; i < 10; i++)
      if (ptr == strstr(ptr, convert[i].coded)) {
        strcat(decoded, &convert[i].digit);
        ptr += convert[i].length;break;
      }
  
  return decoded;
}
__________________________
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* dec2bin(char* s)
{
    char* dict[] = {"10", "11", "0110", "0111", "001100", "001101", "001110", "001111", "00011000", "00011001"};
    return dict[atoi(s)];
}
char* code(const char* strng)
{
    int lg = strlen(strng);
    char* ret = (char *)calloc(8 * lg, sizeof(char));
    for (int i = 0; i < lg; ++i)
    {
        char d = strng[i];
        strcat(ret, dec2bin(&d));
    }
    return ret;
}
int val(char c)
{
    return (int)c - '0';
}
int toDec(char *str, int base)
{
    int len = strlen(str), pow = 1, num = 0;
    int i;
    for (i = len - 1; i >= 0; i--)
    {
        num += val(str[i]) * pow;
        pow *= base;
    }
    return num;
}
char* decode(const char* str)
{
    int lg = strlen(str);
    char* ret = (char *)calloc(lg, sizeof(char));
    int i = 0;
    while (i < lg)
    {
        int zero_i = i;
        while ((zero_i < lg) && (str[zero_i] != '1'))
            zero_i++;
        int ll = zero_i - i + 2;
        char* ss = (char *)calloc(80, sizeof(char));
        strncpy(ss, (char *)(str + zero_i + 1), (zero_i + ll) - (zero_i + 1));
        int d = toDec(ss, 2);
        char buf[1];
        sprintf(buf, "%d", d);
        strcat(ret, buf);
        i = zero_i + ll;
    }
    return ret;
}
__________________________
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char* c[10] = {"10", "11", "0110", "0111", "001100", "001101", "001110", "001111", "00011000", "00011001"};

char* code(const char* s)
{  
  int l = strlen(s);
  char* r = calloc(8*l+1, sizeof(char));
  for(int i=0; i<l; i++) strcat(r, c[s[i]-48]);
  return r;
}
char* decode(const char* s)
{
  int l = strlen(s);
  char* r = calloc(l/2+1, sizeof(char));
  const char* p = s;
  int n=0;
  while(*p){
    for(int i=0; i<10; i++){
      int sz = strlen(c[i]);
      if (!memcmp(p, c[i], sz)){
        r[n] = i+48;
        n++;
        p += sz;
      }
    }
  }
  return r;
}
__________________________
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct {
  char digit;
  char *coded;
  int length;
} convert[] = { {'0', "10", 2}, {'1', "11", 2}, {'2', "0110", 4}, {'3', "0111", 4}, {'4', "001100", 6}, {'5', "001101", 6},\
                {'6', "001110", 6}, {'7', "001111", 6}, {'8', "00011000", 8}, {'9', "00011001", 8}};

char* code(const char* strng)
{
  char temp[1024] = {0};
  for (; *strng != '\0'; strng++)
    strcat(temp, convert[*strng-'0'].coded);

  char *coded = (char *) malloc((strlen(temp) + 1) * sizeof(char));
  strcpy(coded, temp);

  return coded;
}

char* decode(const char* str)
{
  const char *ptr = str;
  char word[1024] = {0};
  int index = 0;
  
  while (*ptr != '\0') {
    for (int i = 0; i < 10; i++) {
      if (ptr == strstr(ptr, convert[i].coded)) {
        word[index++] = convert[i].digit;
        ptr += convert[i].length;
        break;
      }
    }
  }
  char *decode = (char *) malloc((strlen(word)+1) * sizeof (char));
  strcpy(decode, word);
  
  return decode;
}
__________________________
#include <stdlib.h>
#include <string.h>

static char *map =
  "10\0______0"  "11\0______1"  "0110\0____2"  "0111\0____3"  "001100\0__4"
  "001101\0__5"  "001110\0__6"  "001111\0__7"  "00011000\08"  "00011001\09";

char* code(const char* s)
{
  char *buf = calloc(1000, 1);  
  
  while (*s)
    strcat(buf, map + (*s++ - '0') * 10);  
  
  return realloc(buf, strlen(buf) + 1);
}

char* decode(const char* s)
{
  char *buf = calloc(1000, 1), *b = buf, *m;
  
  while (*s)
    for (char c = '0'; c <= '9'; c++)
      strstr(s, m = map + (c - '0') * 10) == s ? *b++ = c, s += strlen(m) : 0;
  
  return realloc(buf, b - buf + 1);
}
__________________________
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CODE_MAX_SIZE       8
#define ASCII_NUM_CHANGE    48

char *codeTable[10] = { "10", 
                        "11", 
                        "0110", 
                        "0111", 
                        "001100", 
                        "001101", 
                        "001110", 
                        "001111", 
                        "00011000", 
                        "00011001"};

char* code(const char* strng)
{
    char *retStr = (char *) malloc(sizeof(char)*strlen(strng)*CODE_MAX_SIZE+1);
    retStr[0] = '\0';
    do{
      sprintf(retStr, "%s%s",retStr,codeTable[(*strng)-ASCII_NUM_CHANGE]);  
    }while(*++strng != '\0');
    return retStr;    
}


char* decode(const char* str)
{
  unsigned num_bits;
  unsigned number;
  char *retStr = (char *) malloc(sizeof(char)*strlen(str));
  retStr[0] = '\0';
  while (*str != '\0')
  {
    number=0;
    for(num_bits=1; *str++!= '1'; ++num_bits);
    do{number = number << 1 | ( *str++ == '1');}while(0 < --num_bits);
    sprintf(retStr, "%s%d", retStr, number);
  }
  return retStr;
}
