56f173a35b91399a05000cb7


#include <stddef.h>
#include <ctype.h>

size_t find_longest(const char *words) {
  size_t length = 0, max_length = 0;
  const char *pchar = words;
  
  char c;
  do {
    c = *pchar++;
    if (isspace(c) || c == 0) {
      if (length > max_length) {
        max_length = length;
      }
      length = 0;
    } else {
      length++;
    }
  } while (c);

  return max_length;
}
__________________________
#include <stddef.h>
#include <ctype.h>

size_t find_longest(const char *words)
{
  size_t length = 0, max_length = 0;
  const char *pchar = words;
  
  char c;
  while ((c = *pchar++)) {
    if (isspace(c)) {
      if (length > max_length) {
        max_length = length;
      }
      length = 0;
    } else {
      length++;
    }
  }
  if (length > max_length) {
    max_length = length;
  }
      
  return max_length;
}
__________________________
#include <stddef.h>
#include <ctype.h>

size_t find_longest(const char *words) {
  size_t length = 0, max_length = 0;
  const char *pchar = words;
  
  char c;
  while ((c = *pchar++)) {
    if (isspace(c)) {
      if (length > max_length) {
        max_length = length;
      }
      length = 0;
    } else {
      length++;
    }
  }
  
  return length > max_length ? length : max_length;
}
__________________________
#include <stddef.h>
#include <ctype.h>
size_t find_longest(const char *words) {
  size_t length = 0, max_length = 0;
  char *pchar = (char*)words, c;
  while (c = *pchar++) {
    if (isspace(c)) length = 0;
    else max_length = ++length > max_length ? length : max_length;
  }
  return max_length;
}
