544aed4c4a30184e960010f4


#include <stddef.h>

//  assign divisors to *array
//  set *z to *array length

void divisors(unsigned n, size_t *z, unsigned *array) {
  *z = 0;
  
  for (int i = 2; i <= (n / 2); i++)
  {
    if (n % i == 0)
      array[(*z)++] = i;
  }
}
__________________________________
#include <stddef.h>

void divisors(unsigned n, size_t *z, unsigned *array) {
  *z = 0;
  for(unsigned i = 2; i < n; i++){
    if(n % i == 0)
      array[(*z)++] = i;
    }
}
__________________________________
#include <stddef.h>

void divisors(unsigned n, size_t *z, unsigned *array) {
    *z = 0;
    for(unsigned x = 2; x < n/2+1; x++) {
        if(n % x == 0) {
            array[(*z)++] = x;
        }
    }
}
__________________________________
#include <stddef.h>
void divisors(unsigned n, size_t*z, unsigned *array) {
    
    unsigned int r=2;
    int c=0;
    
    while(r!=n){
        
      if((n%r)==0){
          array[c]=r;
          c++;
       }
           r++;
       }
       
       if(c==0){
           array = NULL;
       }
       
    *z = c;
}
__________________________________
#include <stddef.h>

void divisors(unsigned n, size_t *z, unsigned *array) {
    *z = 0;
    for (unsigned i = 2; i < n; i++) {
        if (0 != n % i) continue;

        array[(*z)++] = i;
    }
}
