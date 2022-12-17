56c5847f27be2c3db20009c3


char *subtract_sum(int n)
{
  return "apple";
}
_______________________________________
char *subtract_sum(__attribute__((unused)) int _) {
  return "apple";
}
_______________________________________
char *subtract_sum(int n) {
  do {
    int m=n,s=0;
    while(m>0) {
      s+=m%10;
      m/=10;
    }
    n-=s;
  }
  while(n>100);
  if(n==1||n==3||n==24||n==26||n==47||n==49||n==68||n==70||n==91||n==93)
    return "kiwi";
  if(n==2||n==21||n==23||n==42||n==44||n==46||n==65||n==67||n==69||n==71||n==88||n==92)
    return "pear";
  if(n==4||n==6||n==25||n==29||n==48||n==50||n==73||n==94||n==96)
    return "banana";
  if(n==5||n==7||n==28||n==30||n==32||n==51||n==53||n==74||n==76||n==95||n==97)
    return "melon";
  if(n==8||n==10||n==12||n==31||n==33||n==51||n==56||n==75||n==77||n==79||n==98||n==100)
    return "pineapple";
  if(n%9==0)
    return "apple";
  if(n==11|n==13||n==34||n==55||n==57||n==59||n==78||n==80)
    return "cucumber";
  if(n==14||n==16||n==35||n==37||n==39||n==58||n==60||n==83)
    return "orange";
  if(n==15||n==17||n==19||n==38||n==40||n==61||n==82||n==84||n==86)
    return "grape";
  if(n==20||n==22||n==41||n==43||n==62||n==64||n==66||n==85||n==87||n==89)
    return "cherry";
}
_______________________________________
#include <stdlib.h>
#include <string.h>

static char *ft_strdup(const char *str)
{
  int i = 0;
  char *dup;
 
  if (str == NULL)
  {
    return (NULL);
  }
  dup = (char *)malloc(sizeof(char) * (strlen(str) + 1));
  while (str[i] != '\0')
  {
    dup[i] = str[i];
    i++;
  }
  dup[i] = '\0';
  return (dup);
}

static int sum_of_number(int n)
{
  int sum = 0;

  if (n > 9)
  {
    sum += sum_of_number(n / 10);
  }
  sum += n % 10;
  return (sum);
}

char *subtract_sum(int n)
{
  char *fruits[] = {"kiwi", "pear", "kiwi", "banana", "melon", "banana", "melon", "pineapple", "apple", "pineapple",
"cucumber", "pineapple", "cucumber", "orange", "grape", "orange", "grape", "apple", "grape",
"cherry", "pear", "cherry", "pear", "kiwi", "banana", "kiwi", "apple", "melon", "banana",
"melon", "pineapple", "melon", "pineapple", "cucumber", "orange", "apple", "orange", "grape", "orange",
"grape", "cherry", "pear", "cherry", "pear", "apple", "pear", "kiwi", "banana", "kiwi",
"banana", "melon", "pineapple", "melon", "apple", "cucumber", "pineapple", "cucumber", "orange", "cucumber",
"orange", "grape", "cherry", "apple", "cherry", "pear", "cherry", "pear", "kiwi", "pear",
"kiwi", "banana", "apple", "banana", "melon", "pineapple", "melon", "pineapple", "cucumber", "pineapple",
"cucumber", "apple", "grape", "orange", "grape", "cherry", "grape", "cherry", "pear", "cherry",
"apple", "kiwi", "banana", "kiwi", "banana", "melon", "banana", "melon", "pineapple", "apple", "pineapple"};
  
  if (n < 10 || n >= 10000)
  {
    return (NULL);
  }
  do
  {
    n -= sum_of_number(n);
  } while (n > 100);
  return (ft_strdup(fruits[n - 1]));
}
