55466989aeecab5aac00003e


#include <stdlib.h>
// C returns a structure named Data.
// array is the returned array.
// sz is array size. 
// If from the beginning square length == square width
// return a Data with sz = 0.
typedef struct Data Data;
struct Data {
     int *array;
     int sz;
};

Data* sqInRect(int lng, int wdth) {
  Data* res = malloc(sizeof(Data));
  res->sz = 0; res->array = NULL;
  if (lng == wdth) return res;
  while (lng > 0 && wdth > 0) {
    res->sz++;
    res->array = realloc(res->array, res->sz * sizeof(int));
    if (lng > wdth) {
      lng -= wdth;
      res->array[res->sz-1] = wdth;
    }
    else {
      wdth -= lng;
      res->array[res->sz-1] = lng;
    }
  }
  return res;
}
______________________________
#include <stdlib.h>

typedef struct Data Data;
typedef struct Data {
     int *array;
     unsigned sz;
} sqdata;

sqdata *sq_in_rect(unsigned length, unsigned width)
{
    sqdata *sqd = calloc(1u, sizeof (sqdata));
    int *v;
    unsigned n, side;

    if (!sqd)
        return NULL;
    else if (length == width)
        return sqd;
    sqd->array = v = malloc(sizeof(int) * (length < width ? width : length));

    do {
        if (length > width)
            width ^= length ^= width ^= length;
        if (!length)
            side = 1;
        else
            side = length;
        sqd->sz += n = width / side;
        width %= side;

        while (n--)
            *v++ = side;
    }
    while (length && width);
    sqd->array = realloc(sqd->array, sizeof(int) * sqd->sz);
    return sqd;
}

Data* sqInRect(int lng, int wdth) {
    return sq_in_rect(lng, wdth);
}
______________________________
#include <stdlib.h>

typedef struct Data Data;
struct Data {
     int *array;
     int sz;
};

Data* sqInRect(int lng, int wdth) {
    Data *result = malloc(sizeof(Data));
    result->sz = 0;
    if (lng == wdth)
        return result;
    result->array = malloc(sizeof(int) * lng);
    while (wdth){
        int stop = lng / wdth;
        for (int i = 0; i < stop; i++)
            result->array[result->sz++] = wdth;
        int tmp = wdth;
        wdth = lng % wdth;
        lng = tmp;
    }
    result->array = realloc(result->array, sizeof(int) * result->sz);
    return result;
}
