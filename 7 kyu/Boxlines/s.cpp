/*
*   Количество ребер направленных вдоль любой оси i
* можно определить как:
*
*       S(i) = n(i) * ((n(j)) + 1) * (n(k) + 1)       (1)
*     где  n(i) - количество ребер вдоль искомой оси i, 
*          (n(j)+1) - количество ребер направленных вдоль оси i
*            по перпендикулярной оси j к оси i, 
*          (n(k)+1) - количество ребер направленных вдоль оси i
*            по перпендикулярной оси k к оси i. 
*
*   Исходя из того что у нас трехмерное пространство (i,j,k) в котором
* есть 3 типа ребер направленных вдоль каждой оси, то общее количество ребер
* будет определятся как сумма ребер в каждом направлении:
*
*         S(i,j,k) = S(i) + S(j) + S(k)         (2)
*/

#define INT unsigned long long     // !! переполнение иначе :(

INT oneDirection(INT i, INT j, INT k)
{
  return i * (j + 1) * (k + 1);   //  реализация ур. 1
}

INT f(unsigned int x, unsigned int y, unsigned int z)
{
  INT result;
  result = oneDirection(x, y, z)    // реализация ур. 2
          + oneDirection(y, z, x)
          + oneDirection(z, x, y);
  return result;
}
_____________________________________
unsigned long long f(unsigned int a,unsigned int y, unsigned int z){
  //TODO: Your code here
  unsigned long long x = a;
  return 12*(x*y*z) - (x-1)*y*z*4 - (y-1) *x * z*4 - (z-1)*x*y*4 +(x-1)*(y-1)*z + (x)*(y-1)*(z-1) + (x-1)*(y)*(z-1);
}
_____________________________________
long long f(long long x,long long y,long long z){
if(x>0 && y>0 && z>0)
  return (((x+1)*(y+1)*z)+((x+1)*(z+1)*y)+((y+1)*(z+1)*x));
  else
    return f(x,y,z);
  }
_____________________________________
#include <algorithm>

using namespace std;
unsigned long long f(unsigned int x,unsigned int y, unsigned int z){
  uint64_t xx = x;// max(x,max(y,z)) == 1 ? 1 : max(x,max(y,z));
  uint64_t yy = y;// min(max(x,y), max(y,z)) == 1 ? 1 : min(max(x,y), max(y,z));
  uint64_t zz = z;// min(x, min(y,z)) == 1 ? 1 : min(x, min(y,z));
  
  cout << xx << ":" << yy << ":" << zz << endl;
  cout << "z: " << ((zz-1)*(xx*(yy+1) + yy*(xx+1))) << endl;
  return ((12*xx - 4*(xx-1)) * yy - (yy-1)*(3*xx + 1)) * zz - (zz-1)*(xx*(yy+1) + yy*(xx+1));
  
}
_____________________________________
unsigned long long f(unsigned int x,unsigned int y, unsigned int z)
{
  return (x * (y + 1ul) * (z + 1ul)) + (y * (x + 1ul) * (z + 1ul)) + (z * (x + 1ul) * (y + 1ul));
}
