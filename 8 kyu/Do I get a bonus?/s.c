56f6ad906b88de513f000d96


#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>

typedef unsigned long long ull;

char *bonus_time(ull salary, bool bonus) {
  char *res = malloc(24 * sizeof(int));

  if (bonus) {
    salary *= 10;
  }
  sprintf(res, "$%llu", salary);
  
  return res;
}
__________________________
#define _GNU_SOURCE

#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>

typedef unsigned long long ull;

char *bonus_time(ull salary, bool bonus) {
  char *result = NULL;
  if (bonus)
    salary *= 10;
  asprintf(&result, "$%llu", salary);
  return result;
}
__________________________
#include <stdbool.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

typedef unsigned long long ull;

char *bonus_time(ull salary, bool bonus) {
    
    salary = bonus ? salary * 10 : salary;
    int len = snprintf(NULL, 0, "%llu", salary);
    char *theString = (char *)malloc(sizeof(char) * len + 1);
    char *dollar = (char *)malloc(sizeof(char) * len + 2);
    strcpy(dollar, "$");
    snprintf(theString, len + 1, "%llu", salary);
    strcat(dollar, theString);
    return dollar;

}
