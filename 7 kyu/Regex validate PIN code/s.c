#include <stdbool.h>
#include <string.h>
#include<ctype.h>

bool validate_pin(const char *pin) {
  int pinLen = strlen(pin);
  if(pinLen == 4 || pinLen == 6) {
    for(int i = 0; i < pinLen; i++) {
      if(pin[i] < 48 || pin[i] > 57) {
        return false;
      }
    }
    return true;
  }
 return false;
}
____________________________
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

bool validate_pin(const char *pin) {
  int l = strlen(pin);
  if(l != 4 && l != 6) return false;
  for(const char* p = pin; *p; p++){
    if(!isdigit(*p)) return false;
  }
  return true;
}
____________________________
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

bool validate_pin(const char *pin) {

  // Declaring length variable to loop through pin, and i for iterating.
  int length, i;
  
  // Collects array length of passed pointer.
  length = strlen(pin);
  
  // Checks only when pin is 4 or 6 characters.
  if (length == 6 || length == 4)
    {
      // Loops through pin to check each character.
      for (i = 0; i < length; i++)
        // Immediately returns false if any character is not a digit.
        if (!isdigit(pin[i]))
          return false;
        // Returns true if previous conditional didn't trigger.
        return true;
    }
  
  // Returns false if the pin is any size other than 4 or 6 characters long.
  return false;
}
____________________________
#include <stdbool.h>
#include <stdio.h>

bool validate_pin(const char *pin) {
  int n = 0;
  sscanf(pin, "%*6[0-9]%n", &n);
  return (n == 4 || n == 6) && pin[n] == '\0';
}
____________________________
#include <stdbool.h>
#include <string.h>

bool validate_pin(const char *pin) {

    size_t len = strlen(pin);
    char nums[] = "0123456789";
    
    if(!(len == 4 || len == 6)) return false;
    
    for(size_t i=0; i<len; i++)
    {
      if(strchr(nums, pin[i]) == NULL)
        return false;
    }
  
  return true;
}
