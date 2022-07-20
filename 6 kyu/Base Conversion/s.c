526a569ca578d7e6e300034e


// Translate the input string from the source alphabet to the target alphabet
long long int convertToDec(const char * input, const char * source) {
  int base = strlen(source);
  long long int n = 0;
  for (int i = 0; i < strlen(input); ++i) {
    const char* m = strchr(source, input[i]);
    n = base * n + strchr(source, input[i]) - source;
  }
  return n;
}

char* convertFromDec(long long int n, const char* target) {
  int base = strlen(target);
  const int noDigits = n==0 ? 1 : 1 + floor(log(n) / log(base));
  char* res = (char *) calloc(1 + noDigits, sizeof(char));
  res[noDigits] = '\0';
  for (int i = noDigits - 1; i>=0; --i) {
    res[i] = target[n % base];
    n /= base;
  }
  return res;
}

char * convert(const char * input, const char * source, const char * target) {
  return convertFromDec(convertToDec(input, source), target);
}
__________________________________________
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

// Translate the input string from the source alphabet to the target alphabet
char * convert(const char * input, const char * source, const char * target) {
    size_t input_len = strlen(input);
    size_t source_base = strlen(source);
    size_t target_base = strlen(target);
  
    uintmax_t v = 0;
    for (size_t i = 0; i < input_len; ++i) {
        const char *p = strchr(source, input[i]);
        v = v*source_base + (p ? p - source : 0);
    }
  
    size_t output_len = 1;
    uintmax_t x = 1;
    while (x <= v/target_base) {
        ++output_len;
        x *= target_base;
    }
  
    char *output = malloc(output_len + 1), *p = output;
    while (x != 0) {
        unsigned d = v/x;
        v %= x;
        x /= target_base;
        *p++ = target[d];
    }
    *p = '\0';
  
    return output;
}
__________________________________________
// Translate the input string from the source alphabet to the target alphabet
#include <string.h>
#include <math.h>
#include <stdlib.h>
char * convert(const char * input, const char * source, const char * target) {
  // Code goes here...
  unsigned long len1 = strlen (input);
  unsigned long len2 = strlen (source);
  unsigned long len3 = strlen (target);
  unsigned long num =0,n = 0;
  int i = 0,j = 0,count = 0,m = 0,change = 0,sign = 0;
  char * result = (char*)malloc(sizeof(char)*128);
  
  for (i = len1 - 1;i >= 0;i--){
    for (m = 0;m < len2 ;m++){
      if(input[i]==source[m]){
        break;
      }
    }
    n = pow(len2,len1-1-i);
    num += m * n;
  }
  if(num==0){
    result[count]=target[0];
  }
  while(num!=0){
    sign = num%len3;
    num = num/len3;
    result[count] = target[sign];
    count++; 
  }
  for(j=0;j<count/2;j++){
    change = result[j];
    result[j] = result[count-j-1];
    result[count-j-1] = change;
  }
  return result;
}
