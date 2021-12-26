#include <stdlib.h>

int *snail(size_t *outsz, const int **mx, size_t m, size_t n)
{
    *outsz = n*n;
    if(n == 0) return NULL;
    
    int *list = (int *)calloc(n*n, sizeof(int));
    size_t index = 0;
    
    for(int i=0;; i++){
    
        int len = n - 2*i;
    
        for(int k=0; k < len; k++) list[index++] = mx[i][i+k];
       
        for(int k=0; k < len - 1; k++) list[index++] = mx[i+k+1][n-i-1];
        
        for(int k=0; k < len - 1; k++) list[index++] = mx[n-i-1][n-i-k-2];
        
        for(int k=0; k < len - 2; k++) list[index++] = mx[n-k-i-2][i];
        
        if(index >= n*n) break;
    }
    
    return list;
}

####################
#include <stdlib.h>

int *snail(size_t *outsz, const int **mx, size_t m, size_t _)
{
  int n = m, *ret = malloc(( *outsz = m * m) * sizeof(int)), o = 0, j = 0;
  while (n > 0) 
  {
    for (int x=o, y=o; x<o+n; x++) ret[j++] = mx[y][x];
    for (int x=o+n-1, y=o+1; y<o+n; y++) ret[j++] = mx[y][x];
    for (int x=o+n-2, y=o+n-1; x>=o; x--) ret[j++] = mx[y][x];
    for (int x=o, y=o+n-2; y>o; y--) ret[j++] = mx[y][x];
    o++;
    n-=2;
  }
  return ret;
}

###################
#include <stdlib.h>
#include <stdio.h>
#include<malloc.h>
#include<string.h>

#define left 0
#define down 1
#define right 2
#define up 3

int *snail(size_t *outsz, const int **mx, size_t column, size_t cols) {
  
  
  const int CoubSize = column;
  int *deepHouse;
  deepHouse = (int*)malloc((column*cols*4 +1));
  int counterHouse = 0;
  int array[CoubSize][CoubSize];
  while(counterHouse < column*cols )
  {
    
      
    array[0][counterHouse] = *(*mx+counterHouse);
    
  
   counterHouse++; 
  }
 
  
 
  int n = CoubSize*CoubSize;
    int x = 0;
    int y = 0;
    int status = 0;
  int pressedArray[CoubSize][CoubSize];
  
   int a = 0;
    while(n > 0) {
        if ( status == up && pressedArray[y][x] == 444444 ) {
            status = 0; y++; x++;
        };
        if ( status == left && pressedArray[y][x] == 444444 ) {
            status++; y++; x--;
        }
         if ( status == down && pressedArray[y][x] == 444444 ) {
            status++; y--; x--;
        }
        if ( status == right && pressedArray[y][x] == 444444 ) {
            status++; y--; x++;
        }
        
  
      
        pressedArray[y][x]= 444444; 
         *deepHouse = array[y][x];
        
        if(status == 0) x++;
        
        if(status == 1) y++;
        
        if(status == 2) x--;
        
        if(status == 3) y--; 
         
          
        if(x == CoubSize) {status++; x--; y++;};
        if(y == CoubSize) {status++; y--; x--;};
        if(x == -1) {status++; x++; y--;};
        if(y == -1) { status++; y++; x++; } ;
        
        if(status>3) {status = 0; };
        
       
        deepHouse++;
       a++;
        n--;
    }
   *outsz = CoubSize*CoubSize;
  counterHouse =  CoubSize*CoubSize;

  while(counterHouse)
  {

   deepHouse--;
   counterHouse--; 
  } 
 return deepHouse;
  
}

##################
#include <stdlib.h>

int *snail(size_t *outsz, const int **mx, size_t rows, size_t cols) {
  // the numbers of rows and cols are passed separately for historical reasons
  // the numbers of rows and cols are passed separately for historical reasons
  int i,j,k=0;
  int *s = calloc(rows*cols,sizeof(int));
  for(i=0;k<rows*cols;i++){
    for(j=i;j<cols-i;j++){
      s[k]=mx[i][j];
      k++;
    }
    if(k>(rows*cols)-1){break;}
    for(j=i+1;j<cols-i;j++){
      s[k]=mx[j][rows-1-i];
      k++; 
    }
    if(k>(rows*cols)-1){break;}
    for(j=rows-2-i;j>=i;j--){
      s[k]=mx[cols-1-i][j];
      k++;
    }
    if(k>(rows*cols)-1){break;}
    for(j=cols-2-i;j>i;j--){
      s[k]=mx[j][i];
      k++;
    }
    if(k>(rows*cols)-1){break;}
  }
  *outsz = rows*cols;
  printf("\n");
  return s;
}

##################
#include <stdlib.h>

void regular(const int **mx, size_t rows, size_t cols, int *out)
{
  size_t start_rows = 0, start_cols = 0;
  while (rows && cols)
  {
    for (size_t i = 0; i < cols; ++i)
    {
      *out++ = mx[start_rows][start_cols + i];
    }
    for (size_t i = 1; i < rows; ++i)
    {
      *out++ = mx[start_rows + i][start_cols + cols - 1];
    }
    if (1 == rows || 1 == cols)
    {
      return;
    }
    for (size_t i = 1; i < cols; ++i)
    {
      *out++ = mx[start_rows + rows - 1][start_cols + cols - i - 1];
    }
    for (size_t i = rows - 2; i > 0; --i)
    {
      *out++ = mx[start_rows + i][start_cols];
    }
    if (0 == rows -2 || 0 == cols - 2)
    {
      return;
    }
    start_rows++;
    start_cols++;
    rows -= 2;
    cols -= 2;
  }
}

int *snail(size_t *outsz, const int **mx, size_t rows, size_t cols) {
  // the numbers of rows and cols are passed separately for historical reasons
  if (0 == rows || 0 == cols)
    return (int *)(*outsz = 0);
  int * ret = malloc(rows * cols * sizeof(int));
  regular(mx, rows, cols, ret);
  *outsz = rows * cols;
  return ret;
}
