#include <stddef.h>

int find_odd (size_t length, const int array[length])
{
  int odd_int = 0;

  for (size_t i = 0; i < length; i++)
    odd_int ^= array[i];

  return odd_int;
}
_______________________________
#include <stddef.h>

int find_odd (size_t length, const int array[length])
{
  int n;
  unsigned long i, j;
  for(i = 0; i < length; i++)
  {
    n = 0;
    for(j = 0; j < length; j++)
    {
      if(array[i] == array[j])
        n++;
    }
    if(n % 2 == 1)
      return array[i];
  }
  return 0;
}
_______________________________
#include <stddef.h>

int find_odd (size_t length, const int array[length])
{
  int index = 0;       /* index into the array */
  int count = 0;       /* count number frequency */
  int tracker;         /* hold each number to be matched */
  int temp;            /* temporary index into the array */
  
  /* loop while the index is less than or equal to the array length */
  while (index <= (int)length-1) {
    tracker = array[index];   /* get item in array at "index" */
    
    /* loop through the array using the temp variable as the index */
    for (temp=0; temp <= (int)length-1; temp++) {
      
      /* compare the item in "tracker" variable to the item in array at index "temp" */
      if (tracker == array[temp]) {
        count++;    /* if true, increment the count variable by 1 */
      }
    }
    
    /* check if the count is odd by checking if the remainder is not 0 */
    if (count % 2 != 0) {
      return tracker;    /* if true, return the number stored in tracker variable */
    }
    
    /* otherwise, reset the counter and move to the next number in the array */
    else {
      count = 0;    /* reset counter */
      index++;      /* increment array index */
    }
  }
  return 0;
}
_______________________________
#include <stddef.h>

int find_odd (size_t length, const int array[length])
{
    int odd = 0;
  
    for (size_t i = 0; i < length; i++) {
        odd ^= array[i];
    }
  
    return odd;
}
