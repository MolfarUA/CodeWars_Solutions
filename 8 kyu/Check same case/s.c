#include <ctype.h>
int same_case (char a, char b)
{
  if (!isalpha(a) || !isalpha(b)){
    return -1;
  }
  return ('a' <= a  && a <= 'z' && 'a' <= b && b <= 'z') || ('A' <= a && a <= 'Z' && 'A' <= b && b <= 'Z');
}
__________________________
int same_case (char a, char b)
{
   return !isalpha(a) || !isalpha(b)? -1: !isupper(a) == !isupper(b);
}
__________________________
#include <string.h>
char * choose_case(char chartest)
{
  if (chartest>='a' && chartest<='z')
    return "min";
  else if (chartest>='A' && chartest<='Z')
    return "maj";
  else
    return "autre";
}
int same_case (char a, char b)
{
  if (strcmp(choose_case(a), "autre")==0 || strcmp(choose_case(b), "autre")==0 )
    return -1;
  if (strcmp(choose_case(a), choose_case(b))==0)
      return 1;
  else
      return 0;
  return 0;
}
__________________________
int same_case (char a, char b)
{
  if ((isalpha(a) == isalpha(b)) && (isalpha(a) != 0)) {
    if (isupper(a) == isupper(b)) {
      return 1;
    } else {
       return 0;
    }
  } else {
    return -1;
  }
}
__________________________
int same_case (char a, char b)
{
  if (a < 'A' || (a > 'Z' && a < 'a') || a > 'z' || b < 'A' || (b > 'Z' && b < 'a') || b > 'z') {
    return -1;
  }
  else if ((a >= 'a' && a <= 'z' && b >= 'a' && b <= 'z') || (a >= 'A' && a <= 'Z' && b >= 'A' && b <= 'Z')) {
    return 1;
  }
  return 0;
}
__________________________
int same_case (char a, char b)
{
  if((a >= 'A' && a <= 'Z') && (b >= 'A' && b <= 'Z')){
    return 1;
  } else if(((a >= 'a' && a <= 'z') && (b >= 'a' && b <= 'z'))){
    return 1;
    }
  else if(((a >= 'a' && a <= 'z') && (b >= 'A' && b <= 'Z')) || ((a >= 'A' && a <= 'Z') && (b >= 'a' && b <= 'z'))){
    return 0;
  }
  return -1;
}
