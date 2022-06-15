void fakeBin(const char *digits, char *buffer) {
  for (int i = 0; digits[i] != 0; i++) {
    *buffer++ = digits[i] >= '5' ? '1' : '0';
  }
  *buffer = 0;
}
__________________________________
#include <string.h>
void fakeBin(const char *digits, char *buffer) {
  for (size_t i = 0; i < strlen(digits); buffer[++i] = '\0')
    if(digits[i] < 53) buffer[i] = 48;
    else buffer[i] = 49;
}
__________________________________
void fakeBin(const char *digits, char *buffer) {
  // Please place result in the memory pointed to by
  // the buffer parameter. Buffer has enough memory to
  // accommodate the answer as well as the null-terminating
  // character.
  int i = 0;
  while (digits[i] != '\0'){
    if (digits[i] - 48 < 5){
      buffer[i++] = '0';
    } else {
      buffer[i++] = '1';
    }
  }
  buffer[i] = '\0';
}
__________________________________
void fakeBin(const char *d, char *b){
  int i=0;
  
    while(d[i]!='\0'){
      if(d[i]<'5'){
            b[i]='0';
    }else{
      b[i]='1';
    }
    i++;
    }
    b[i]='\0';
}
__________________________________
#include <stdio.h>

void fakeBin(const char *digits, char *buffer) {

    char *bp = buffer;
    for (const char *p = digits; *p != 0; p++, bp++) {
        *bp = ('0' <= *p && *p <= '4') ? '0' : '1';
    }
    *bp = '\0';
}
