536a155256eb459b8700077e


#include <stdlib.h>

int** create_spiral(int n) {
  if (n<=0) return NULL;
  int** array = (int**) calloc(n, sizeof(int*));
  for (int i=0; i<n; i++)
    array[i] = (int*) calloc(n, sizeof(int));
  int x=-1, y=0, dx=1, dy=0, l=n, k=0;
  while (l>0) {
    for (int i=0; i<l; i++) {
      x += dx;
      y += dy;
      if (x>=0) array[y][x] = ++k;
      if (l==0) return array;
    }
    if (dy==0) l--;
    int t = dx;
    dx = -dy;
    dy = t;
  }
  return array;
}
_________________________
#include <stdlib.h>

int **create_spiral (int n)
{

  if(n <= 0)
    return NULL;

    int r = n, c = n, i;

    int** spiral = (int**)malloc(r * sizeof(int*));
    for (i = 0; i < r; i++)
        spiral[i] = (int*)malloc(c * sizeof(int));

  int start = 0;

  int nums = 1;
  while(n > 0)
  {
    int p = start;
    int q = start;

    int loop_counter = n;

    if(loop_counter == n)
    {
        int i = 0;
        while(i++ < loop_counter)
            spiral[p][q++] = nums++;
        loop_counter -= 1;
        q--;
    }

    if(loop_counter == n - 1)
    {
        p++;
        int i = 0;
        while(i++ < loop_counter)
            spiral[p++][q] = nums++;
        p--;
    }

    if(loop_counter == n - 1)
    {
        q--;
        int i = 0;
        while(i++ < loop_counter)
            spiral[p][q--] = nums++;
        loop_counter -= 1;
        q++;
    }

    if(loop_counter == n - 2)
    {
        p--;
        int i = 0;
        while(i++ < loop_counter)
            spiral[p--][q] = nums++;
    }
    n -= 2;
    start++;
  }


    return spiral;
}
_________________________
#include <stdlib.h>

// allocate an array of pointers
// both the array and the individual pointers will be freed
// return NULL if (n <= 0)
int **create_spiral (int n)
{
  if (n < 1)
    return NULL;
  
  int** two_dim_array = malloc (n * sizeof (int*));
  int i , j;
  int bound_up = 1;
  int bound_right = n - 1;
  int bound_down = n - 1;
  int bound_left = 0;
  int walking_direction = 0;
  int value_to_write = 2;
  
  for (i = 0; i < n; i++)
  {
    *(two_dim_array + i) = malloc (n * sizeof (int));  
  }
  
  two_dim_array[0][0] = 1;
  i = 0;
  j = 0;
   
  while (value_to_write <= n * n)
  {
     if (walking_direction % 4 == 0)
     {
       while (j < bound_right && value_to_write <= n * n)
       {
          j++;
          two_dim_array[i][j] = value_to_write++;
       }
       bound_right--;
       walking_direction++;
     }
     else if (walking_direction % 4 == 1)
     {
       while (i < bound_down && value_to_write <= n * n)
       {
          i++;
          two_dim_array[i][j] = value_to_write++;
       }
       bound_down--;
       walking_direction++;
     }
     else if (walking_direction % 4 == 2)
     {
       while (j > bound_left && value_to_write <= n * n)
       {
          j--;
          two_dim_array[i][j] = value_to_write++;
       }
       bound_left++;
       walking_direction++;
     }
     else if (walking_direction % 4 == 3)
     {
       while (i > bound_up && value_to_write <= n * n)
       {
          i--;
          two_dim_array[i][j] = value_to_write++;
       }
       bound_up++;
       walking_direction++;
     }  
  }
  return two_dim_array;
}
