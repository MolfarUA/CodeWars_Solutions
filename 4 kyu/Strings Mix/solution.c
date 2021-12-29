#include <stdlib.h>
#include <ctype.h>

struct string {
  int str;
  char c;
  int cnt;
};

char* mix(char* s1, char* s2) {
  int a1[26] = {0}, a2[26] = {0};
  struct string res[26];
  char c;
  char *result, *p;
  int cnt = 0;
  
  int comp(const struct string *s1, const struct string *s2);
  
  while (c = *s1++)
    if (islower(c))
      a1[c - 'a']++;
      
  while (c = *s2++)
    if (islower(c))
      a2[c - 'a']++;
      
  for (int i = 0; i < 26; i++) {
    if (a1[i] > a2[i] && a1[i] > 1) {
      res[cnt].str = 1;
      res[cnt].c = 'a' + i;
      res[cnt].cnt = a1[i];
      cnt++;
    }
    else if(a2[i] > a1[i] && a2[i] > 1) {
      res[cnt].str = 2;
      res[cnt].c = 'a' + i;
      res[cnt].cnt = a2[i];
      cnt++;
    }
    else if(a1[i] == a2[i] && a1[i] > 1) {
      res[cnt].str = 3;
      res[cnt].c = 'a' + i;
      res[cnt].cnt = a1[i];
      cnt++;
    }
  }
  
  qsort(res, cnt, sizeof(struct string), comp);
  
  result = malloc(sizeof(char) * (cnt * (res[0].cnt  + 3) + 1));
  p = result;
  *p = '\0';
  for (int i = 0; i < cnt; i++) {
    *p++ = (res[i].str == 3) ? '=' : '0' + res[i].str;
    *p++ = ':';
    while (res[i].cnt--)
      *p++ = res[i].c;
    *p++ = '/';
  }
  if (p > result)
    *(p - 1) = '\0';
  
  return result;
}

int comp(const struct string *s1, const struct string *s2) {
  if (s1->cnt != s2->cnt)
    return -s1->cnt + s2->cnt;
  else if (s1->str != s2->str)
    return s1->str - s2->str;
  else
    return s1->c - s2->c;
}

__________________________________________________
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#define ASZ 26
#define max(a, b) (((a) > (b)) ? (a) : (b))

struct tally {
    char letter;
    const char *prefix;
    unsigned counts[2];
};

int order(const void *a0, const void *b0) {
    const struct tally *a = a0, *b = b0;
    const unsigned max_a = max(a->counts[0], a->counts[1]),
                   max_b = max(b->counts[0], b->counts[1]);

    if (max_a != max_b)
        return max_b - max_a;

    int diff = strcmp(a->prefix, b->prefix);

    return diff ? diff : a->letter - b->letter;
}

void tally_up(struct tally *t, const char *s, int n) {
    char c;

    while (*s) if (islower((c = *s++)))
        t[c - 'a'].counts[n]++;
}

char *stringify(const struct tally *t) {
    size_t len = 0;
    char *string = calloc(128, sizeof *string);

    for (size_t i = 0; i < ASZ; i++) {
        if (t[i].counts[0] < 2 && t[i].counts[1] < 2) continue;

        const char *prefix = t[i].prefix;

        while (*prefix)
            string[len++] = *prefix++;

        for (size_t j = 0; j < max(t[i].counts[0], t[i].counts[1]); j++)
            string[len++] = t[i].letter;

        string[len++] = '/';
    }
  
    if (len) string[len - 1] = 0;
  
    return realloc(string, len ? len : 1);
}

char *mix(const char *s1, const char *s2) {
    struct tally graph[ASZ] = { 0 };

    tally_up(graph, s1, 0);
    tally_up(graph, s2, 1);

    for (size_t i = 0; i < ASZ; i++) {
        unsigned c1 = graph[i].counts[0],
                 c2 = graph[i].counts[1];
 
        graph[i].letter = 'a' + i; 
        graph[i].prefix = (c1 == c2) ? "=:" : (c1 > c2) ? "1:" : "2:";
    }

    qsort(graph, ASZ, sizeof *graph, order);

    return stringify(graph);
}

__________________________________________________
#import <stdlib.h>
#import <string.h>
#import <stdio.h>

typedef struct LetterStats {
  char winner;
  int count;
  char letter;
} LetterStats;

static int compareLetterStats(const void *lhs, const void *rhs) {
  LetterStats *stats1 = (LetterStats *)lhs;
  LetterStats *stats2 = (LetterStats *)rhs;

  return stats1->count != stats2->count
    ? stats2->count - stats1->count
    : (stats1->winner != stats2->winner
       ? stats1->winner - stats2->winner
       : stats1->letter - stats2->letter);
}

static const int LetCount = 26;

typedef struct Hist {
  int hist[LetCount];
} Hist;

static Hist buildHist(char *s) {
    Hist result;
  memset(result.hist, 0, LetCount * sizeof(int));

  for (char *p = s; *p; p++) {
    if (*p >= 'a' && *p <= 'z') {
      result.hist[*p - 'a']++;
    }
  }

  return result;
}

char *mix(char* s1, char* s2) {
  Hist hist1 = buildHist(s1);
  Hist hist2 = buildHist(s2);

  LetterStats stats[LetCount];

  for (int i = 0; i < LetCount; i++) {
    stats[i].letter = 'a' + i;

    int cmp = hist1.hist[i] - hist2.hist[i];
    if (cmp > 0) {
        stats[i].winner = '1';
        stats[i].count = hist1.hist[i];
    } else {
        stats[i].winner = cmp ? '2' : '=';
        stats[i].count = hist2.hist[i];
    }
  }

  qsort(stats, LetCount, sizeof(LetterStats), &compareLetterStats);

  int n = 0;
  int resultSize = 1;
  for (; n < LetCount; n++) {
    if (stats[n].count <= 1) {
      break;
    }
    resultSize += 3 + stats[n].count; // '1' + ':' + '/'
  }

  char *result = (char *)malloc(resultSize * sizeof(char));

  char *q = result;
  for (int i = 0; i < n; i++) {
    char letterString[stats[i].count + 1];
    memset(letterString, stats[i].letter, stats[i].count * sizeof(char));
    letterString[stats[i].count] = '\0';
      
    int bytesWritten = sprintf(q, "%c:%s/", stats[i].winner, letterString);
    q += bytesWritten > 0 ? bytesWritten : 0;
  }
  if (q != result) {
      q--;
  }
  *q = '\0';

  return result;
}

__________________________________________________
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#define CHAR_COUNT ('z' + 1 -'a')
#define CHARCNT struct char_counter

struct char_counter
{
  char c;
  int count;
  char symbol;
};

CHARCNT *get_char_count(char *input)
{
  int len = strlen(input);
  CHARCNT *result = calloc(sizeof(CHARCNT), CHAR_COUNT);
  for(int i = 0; i < len; i++)
    if((input[i] >= 'a') && (input[i] <= 'z'))
    {
      result[tolower(input[i]) - 'a'].c = tolower(input[i]);
      result[tolower(input[i]) - 'a'].count++;
      result[tolower(input[i]) - 'a'].symbol = 0;
    }
  return(result);
}

CHARCNT *del_null_cnt(CHARCNT *input, int *size)
{
  *size = 0;
  int *numbers = calloc(sizeof(int), CHAR_COUNT);
  for(int i = 0; i < CHAR_COUNT; i++)
    if(input[i].count > 1)
    {
      numbers[*size] = i;
      (*size)++;
    }
  CHARCNT *result = calloc(sizeof(CHARCNT), *size);
  for(int i = 0; i < *size; i++)
  {
    result[i].c = input[numbers[i]].c;
    result[i].count = input[numbers[i]].count;
    result[i].symbol = input[numbers[i]].symbol;
  }
  return(result);
}

CHARCNT *merge_charcnt(CHARCNT *a, CHARCNT *b)
{
  CHARCNT *result = calloc(sizeof(CHARCNT), CHAR_COUNT);
  for(int i = 0; i < CHAR_COUNT; i++)
  {
    result[i].c = i + 'a';
    result[i].count = a[i].count > b[i].count ? a[i].count : a[i].count < b[i].count ? b[i].count : a[i].count;
    result[i].symbol = a[i].count == b[i].count ? '=' : a[i].count > b[i].count ? '1': '2';
  }
  free(a);
  free(b);
  return(result);
}

void sorting(CHARCNT *a, CHARCNT *b)
{
  CHARCNT *tmp = malloc(sizeof(CHARCNT));
  tmp->c = b->c;
  tmp->count = b->count;
  tmp->symbol = b->symbol;
  b->c = a->c;
  b->count = a->count;
  b->symbol = a->symbol;
  a->c = tmp->c;
  a->count = tmp->count;
  a->symbol = tmp->symbol;
}

CHARCNT *sort_charcnt(CHARCNT *input, int *size)
{
  for(int i = 0; i < *size - 1; i++)
    for(int j = i + 1; j < *size; j++)
    {
      if(input[i].count < input[j].count)
      {
        sorting(&input[i], &input[j]);
      } else if((input[i].count == input[j].count) && (input[i].symbol > input[j].symbol))
      {
        sorting(&input[i], &input[j]);
      } else if((input[i].count == input[j].count) && (input[i].symbol == input[j].symbol) && (input[i].c > input[j].c))
      {
        sorting(&input[i], &input[j]);
      }
    }
  return(input);
}

char *create_str(CHARCNT a)
{
  char *str = calloc(sizeof(char), a.count);
  for(int i = 0; i < a.count; i++)
    str[i] = a.c;
  char *result = calloc(sizeof(char), a.count + 3);
  sprintf(result, "%c:%s/", a.symbol, str);
  return(result);
}

char *mix(char *s1, char *s2)
{
  int size = 0;
  CHARCNT *counts = sort_charcnt(del_null_cnt(merge_charcnt(get_char_count(s1), get_char_count(s2)), &size), &size);
  char *result = calloc(sizeof(char), 1);
  for(int i = 0; i < size; i++)
    strcat(result, create_str(counts[i]));
  result[strlen(result) - 1] = '\0';
  return(result);
}
