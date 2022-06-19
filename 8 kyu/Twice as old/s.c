#include <stdlib.h>

int twice_as_old (int father_age, int son_age)
{
  return abs(father_age - son_age * 2);
}
________________________________
#include <stdbool.h>

int twice_as_old (int father, int son){
  return (son * 2 > father)?(son * 2 - father):(father - son * 2 );
}
________________________________
unsigned int twice_as_old (unsigned int father_age, unsigned int son_age)
{
  int age = (father_age - (son_age * 2));
  return age > 0 ? age : -age;
}
________________________________
int twice_as_old (int father, int son)
{
  return abs(son * 2 - father);
}
________________________________
int twice_as_old (int father_age, int son_age)
{ int res;
  if ((son_age*2)>father_age){
    return (son_age*2)-father_age;
  }else{
  return father_age-(son_age*2);
    }
}
