#include <stdbool.h>
#include <stddef.h>

bool plural(const size_t value) {
  return value != 1;
}
__________________
#include <stdbool.h>
#include <stddef.h>

#define true 1
#define false 0

bool plural(const size_t value)
{
  return value == 1 ? false : true;
}
__________________
#include <stdbool.h>
#include <stddef.h>

bool plural(const size_t value)
{
    if(value==1)
        return false;
    else
        return true;
}
__________________
#include <stdbool.h>
#include <stddef.h>

bool plural(const size_t value) {
    return value == 1 ? false : true;
}
