55cb632c1a5d7b3ad0000145


#include <stdint.h>

char *hoop_count(uint32_t n)
{
    return n < 10 ? "Keep at it until you get it" : "Great, now move on to tricks";
}
_____________________________
#include <stdint.h>

const char *hoop_count(uint32_t n) {
  return n < 10 ? "Keep at it until you get it" : "Great, now move on to tricks";
}
_____________________________
#include <stdint.h>

char *hoop_count(uint32_t n) {
  char *res = calloc(32, sizeof(char));
  if (n>=10) {
    sprintf(res, "Great, now move on to tricks");
  }
  else {
    sprintf(res, "Keep at it until you get it");
  }
  return res;
}
_____________________________
#include <stdint.h>

char *hoop_count(uint32_t n)
{
if(n<10)
return ("Keep at it until you get it");

else if(n)
return ("Great, now move on to tricks");
}
