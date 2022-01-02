#include <stddef.h>

void ones_counter (size_t length_in, const char numbers[length_in], size_t *length_out, int counts[])
{
  size_t i = 0;
  int j = 0;
  while (i < length_in)
  {
    int cnt = 0;
    while (numbers[i++] == 1 && i <= length_in)
    {
      cnt++;
    }
    if (cnt > 0)
      counts[j++] = cnt;
  }
  *length_out = j;
}
_____________________________________________
#include <stddef.h>


void
ones_counter (size_t len_in,
              const char arr_in[len_in],
              size_t* len_out,
              int arr_out[])
{
   *len_out = 0;

   for (size_t i = 0; i < len_in; i++) {
      size_t counter = 0;

      for (size_t j = i; j < len_in && arr_in[j] == 1; j++) {
         counter++;
      }

      if (counter != 0) {
         arr_out[*len_out] = counter;
         ++(*len_out);
         i += counter;
      }
   }
}
_____________________________________________
#include <stddef.h>

void ones_counter (size_t arr_length, const char xs[arr_length], size_t *res_length, int res[]) {
  *res_length = 0;
  int x = 0, i = 0, j = 0, flag = 1;
  while (i < arr_length) {
    if (xs[i] == 1) {
      x++;
      if (flag == 1) {
        *res_length = *res_length + 1;
        flag = 0;
      }
    } else if (xs[i] == 0) {
      flag = 1;
      if (x != 0) {
        res[j++] = x;
        x = 0;
      }
    }
    i++;
  }
  if (x != 0) {
    res[j++] = x;
  }
}
_____________________________________________
#include <stddef.h>

void ones_counter (size_t length_in, const char numbers[length_in], size_t *length_out, int counts[])
{
  int length = 0;
  for (int i = 0; i < length_in; i++) {
    if (numbers[i] != 0) {
      if (i == 0 || numbers[i - 1] == 0) {
        counts[length] = 0;
        length++;
      }
      ++counts[length - 1];
    }
  }
  *length_out = length;
}
_____________________________________________
#include <stddef.h>

void ones_counter (size_t length_in, const char numbers[length_in], size_t *length_out, int counts[]) {
int inside = 0, runlength = 0;
*length_out = 0;

while (length_in--) {
  if (*numbers++ == 1) {
    if (inside)
      runlength++;
    else
      inside = 1, runlength = 1;
    }
  else
    if (runlength)  
      counts[(*length_out)++] = runlength, inside = 0, runlength = 0;
  }
if (runlength)  
  counts[(*length_out)++] = runlength;
}
