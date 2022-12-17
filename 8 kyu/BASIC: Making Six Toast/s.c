5834fec22fb0ba7d080000e8


#include <stdlib.h>

short six_toast(short num) {
    return abs(num - 6);
}
________________________
#include <stdlib.h>

#define MAX_TOASTS 6

short 
six_toast(short num) {
  
  return abs (num - MAX_TOASTS);
}
________________________
#define LEARN return
#define TO    6 < num ?
#define COUNT num - 6 :
#define TOAST 6 - num;

short six_toast(short num) {
  LEARN TO COUNT TOAST
}
