55c6126177c9441a570000cc


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* joinStrings(char *strings[], int count);
char** split(char *str, const char *delim, int *length);

int nbWeight(const char* str) {
  int sum = 0;
  for (int i = 0; i < strlen(str); i++) {
    sum += str[i] - '0';
  }
  return sum;
}
static int compare (const void * a, const void * b) {
    int w1 = nbWeight(*(const char **) a); int w2 = nbWeight(*(const char **) b);
    if (w1 == w2) {
        return strcmp (*(const char **) a, *(const char **) b);
    } else {
        return w1 - w2;
    }
}
char* orderWeight(char* s) {
    int lg;
    char** res = split(s, " ", &lg);
    qsort(res, lg, sizeof(const char *), compare);
    char* result = joinStrings(res, lg);
    free(res);
    return result;
}
_____________________________
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <stdio.h>

int compare(const void *a, const void *b) {
  const char* as = *((char**) a);
  const char* bs = *((char**) b);
  unsigned long long aw = 0, bw = 0;
  while (*as) {
    aw += *as++ - '0';
  }
  while (*bs) {
    bw += *bs++ - '0';
  }
  if (aw != bw) {
    return aw - bw;
  } else {
    return strcmp(*(char**)a, *(char**)b);
  }
}

char** makeList(char* s, size_t *n) {
  const size_t len = strlen(s);
  char* storage = (char*) malloc(len + 3);
  strcpy(storage, s);
  storage[len + 1] = '!'; storage[len + 2] = '\0';
  size_t count = 0;
  char* idx = storage;
  while (*idx) {
    idx = index(idx, ' ');
    if (NULL != idx) {
      do {
        *idx = '\0';
        ++idx;
      } while (' ' == *idx);
      ++count;
    } else {
      ++count;
      break;
    }
  }
  *n = count;
  if (0 == count) { return NULL; }
  char** result = (char**) malloc(count * sizeof(char *));
  idx = storage;
  for (size_t i = 0; i < count; ++i) {
    result[i] = idx;
    if (i < count - 1) {
      idx = 1 + (char*) memchr(idx, '\0', len - (idx - storage));
      while (!*idx) { ++idx; };
    }
  }
  return result;
}

void sprintfList(char* dest, char** list, size_t n) {
  for (size_t i = 0; i < n; ++i) {
    strcpy(dest, list[i]);
    dest += strlen(list[i]);
    *dest++ = (i == n - 1)?'\0':' ';
  }
}

char* orderWeight(char* s) {
  size_t n;
  char** list = makeList(s, &n);
  if (NULL == list) {
    char* p = (char*) malloc(1);
    *p = '\0';
    return p;
  }
  qsort(list, n, sizeof(char*), compare);
  char* result = (char*) malloc(strlen(s) + 1);
  sprintfList(result, list, n);
  free(list);
  return result;
}
_____________________________
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* joinStrings(char *strings[], int count);
char** split(char *str, const char *delim, int *length);

int nbWeight(const char* str) {
  int sum = 0;
  for (int i = 0; i < strlen(str); i++) {
    sum += str[i] - '0';
  }
  return sum;
}
static int compare (const void * a, const void * b) {
    int w1 = nbWeight(*(const char **) a); int w2 = nbWeight(*(const char **) b);
    if (w1 == w2) {
        return strcmp (*(const char **) a, *(const char **) b);
    } else {
        return w1 - w2;
    }
}
char* orderWeight(char* s) {
    int lg;
    char** res = split(s, " ", &lg);
    qsort(res, lg, sizeof(const char *), compare);
    char* result = joinStrings(res, lg);
    free(res);
    return result;
}
