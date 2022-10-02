55c04b4cc56a697bb0000048


#include <limits.h>
#include <stdbool.h>

bool scramble(const char *str1, const char *str2)
{
    int count1[CHAR_MAX - CHAR_MIN + 1] = {0};
    for (; *str1; ++str1) ++count1[*str1 - CHAR_MIN];
    for (; *str2; ++str2)
        if (--count1[*str2 - CHAR_MIN] < 0)
            return false;
    return true;
}
______________________________
#include <stdbool.h>

bool scramble(const char *str1, const char *str2)
{
    int index[26] = {0};
    
    while (*str2)
        index[*str2++ - 'a']++;
    while (*str1)
        index[*str1++ - 'a']--;
    for (int i = 0; i < 26; i++) {
        if (index[i] > 0)
            return false;
    }
    return true;
}
______________________________
#include <stdbool.h>
#include <string.h>

bool scramble(const char *str1, const char *str2)
{
  int len1 = strlen(str1);
  int len2 = strlen(str2);
  int T1[26] = {0};
  int T2[26] = {0};
  for (int i = 0; i < len1; i++) T1[str1[i]-'a']++;
  for (int i = 0; i < len2; i++) T2[str2[i]-'a']++;
  for (int i = 0; i < 26; i++)
  {
    if (T1[i] < T2[i]) return false;    
  }
  return true;
}
