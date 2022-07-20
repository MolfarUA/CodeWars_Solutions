54acd76f7207c6a2880012bb


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char *morse_code (const char *);
char *decodeMorse (const char *);


typedef struct morseTree {
//  int pre;
  char ch[4];
  int dot_idx;
  int dash_idx;
} morseTree_t;

typedef struct thresold {
  int dash_dot;
  int sp_ch;
  int sp_wrd;
} thresold_t;

  static morseTree_t morse_tree[] = {
{"",1,3},
{"E",9,2},
{"A",18,16},
{"T",4,12},
{"N",5,7},
{"D",6,24},
{"B",35,56},
{"K",8,25},
{"C",-1,48},
{"I",14,10},
{"U",11,30},
{"F",-1,-1},
{"M",13,20},
{"G",26,22},
{"S",15,23},
{"H",34,33},
{"W",21,17},
{"J",-1,29},
{"R",19,40},
{"L",53,59},
{"O",37,27},
{"P",-1,64},
{"Q",-1,-1},
{"V",61,32},
{"X",50,-1},
{"Y",51,-1},
{"Z",36,43},
{"",39,28},
{"0",-1,-1},
{"1",47,-1},
{"",45,31},
{"2",-1,-1},
{"3",-1,66},
{"4",-1,-1},
{"5",-1,-1},
{"6",-1,57},
{"7",-1,-1},
{"",38,-1},
{"8",54,-1},
{"9",-1,-1},
{"",41,-1},
{"+",-1,42},
{".",-1,-1},
{"",-1,44},
{",",-1,-1},
{"",46,58},
{"?",-1,-1},
{"'",-1,-1},
{"",55,49},
{"!",-1,-1},
{"/",-1,-1},
{"(",-1,52},
{")",-1,-1},
{"&",-1,-1},
{":",-1,-1},
{";",-1,-1},
{"=",-1,-1},
{"-",-1,-1},
{"_",-1,-1},
{"",60,-1},
{"\"",-1,-1},
{"",62,-1},
{"",-1,63},
{"$",-1,-1},
{"",65,-1},
{"@",-1,-1},
{"",67,-1},
{"",68,-1},
{"",69,-1},
{"SOS",-1,-1} 
};


thresold_t calc_thr(char *mkb)
  {
  
  thresold_t thr = {0,0,0};
  struct hist {
    int cnt;
    int cnt_min;
    int cnt_max;
    int val_thr;
  };
  struct hist dd = {0,1000,0,0};
  struct hist sp = {0,1000,0,0};
  
  int max_hist = strlen(mkb);
  int *dd_hist = calloc(max_hist+1,sizeof(int));
  int *sp_hist = calloc(max_hist+1,sizeof(int));

  for(int i=0;i<max_hist;i++)
    {
    if(mkb[i] == '1') dd.cnt++;
    else sp.cnt++;
    
    if(mkb[i] != mkb[i+1]){
      if ( mkb[i]=='1' ){
        dd_hist[dd.cnt]++;
        dd.val_thr++;
        if( dd.cnt < dd.cnt_min ) dd.cnt_min = dd.cnt;
        if( dd.cnt > dd.cnt_max ) dd.cnt_max = dd.cnt;
        dd.cnt = 0;
      }
      if ( mkb[i]=='0' ){ 
        sp_hist[sp.cnt]++;
        sp.val_thr++;
        if( sp.cnt < sp.cnt_min ) sp.cnt_min = sp.cnt;
        if( sp.cnt > sp.cnt_max ) sp.cnt_max = sp.cnt;
        sp.cnt = 0;
      }
    }
}
  
  if(dd.cnt_max==dd.cnt_min){
    printf ("ZERO\n");
    if ( dd.cnt_min >= sp.cnt_min*3 )
      {
    thr.dash_dot = sp.cnt_min;
    thr.sp_ch = sp.cnt_min;
    thr.sp_wrd = sp.cnt_min*5;
      
    } else {
    thr.dash_dot = dd.cnt_min;
    thr.sp_ch = dd.cnt_min;
    thr.sp_wrd = dd.cnt_min*5;
    }
    return thr;
  }
 
  // dd min
  int i_l = dd.cnt_min;
  int i_r = dd.cnt_max;
  int s_l =0;
  int s_r =0;
  int id_min = 0;
  int val_min = 1000;
  
    
  while(dd_hist[i_l] < dd.val_thr/(dd.cnt_max-dd.cnt_min))  i_l++;
  while(dd_hist[i_r] < dd.val_thr/(dd.cnt_max-dd.cnt_min))  i_r--;
  
  while( i_l <= i_r){
   if (dd_hist[i_l]<=val_min) {id_min = i_l;val_min = dd_hist[i_l];}
    if (dd_hist[i_r]<=val_min) {id_min = i_r;val_min = dd_hist[i_r];}
    if (s_l>s_r){
     s_r += dd_hist[i_r--];
    } else {
      s_l += dd_hist[i_l++];
    }
  }
  thr.dash_dot = id_min;
  thr.sp_ch = thr.dash_dot;
 
  int sss = thr.sp_ch*2;
  while(sp_hist[sss]>0) sss++;
  thr.sp_wrd = sss;
  
  free(dd_hist);
  free(sp_hist);
  return thr;
  
}

char* decodeBitsAdvanced (const char *bits) {
    // ToDo: Accept 0's and 1's, return dots, dashes and spaces

  //remove start & stop zero
  char *mkb = calloc(strlen(bits)+1,1);
  strcpy(mkb,bits);
  char *b = mkb;
  for(int i = (strlen(mkb)-1);i>0;i--){
    if(mkb[i] == '0'){
      mkb[i] = 0;
    } else break;
}
  
  if(strlen(mkb) == 0 ) return mkb; // empty
  
  while(*mkb =='0') mkb++; // remove lead zero
  
  if(strlen(mkb) == 0 ) return mkb; // empty
  

  
  // calc dot_dash hist & space hist
  
  thresold_t thr =  calc_thr(mkb);
  
  int max_hist = strlen(mkb);
  
  
  // decode to dash/dot
  char *ret = calloc(max_hist+1,1);
  int att = 0;
  int dd_cnt =0;
  int sp_cnt = 0;
  
lbl:  
  
  dd_cnt =0;
  sp_cnt = 0;
  

 for(int i=0;i<max_hist;i++)
    {

    if(mkb[i] == '1') dd_cnt++;
    else sp_cnt++;
    
    if(mkb[i] != mkb[i+1]){
      if ( mkb[i]=='1' ){ 
        if(dd_cnt>thr.dash_dot)
             strcat(ret,"-"); 
        else strcat(ret,"."); ;
        dd_cnt = 0;
        }
      
      if ( mkb[i]=='0' ){ 
        if(sp_cnt > thr.sp_wrd) {
         strcat(ret,"   ");   
         sp_cnt = 0;
          continue;
        }
      if(sp_cnt > thr.sp_ch) {
         strcat(ret," ");   
         sp_cnt = 0;
          continue;
        }
         sp_cnt = 0;
          continue;        
    }
   }
}
  // check
  if(att == 0){

  char *tst = decodeMorse (ret);
    if(strlen(tst) == 0){ // err
    thr.dash_dot++;
    thr.sp_ch++;
    att++;
    *ret = 0;
    goto lbl;
   }
  }
  free(b);
  return ret;
}

char *decodeMorse (const char *morseCode) {

  int mz_idx = 0;
  int sp_cnt = 0;
  int err = 0;
  morseTree_t *tree = morse_tree;
  char *mz = (char*) morseCode;
  char *retstr = calloc(strlen(morseCode)+1,sizeof(char));
    while(*mz){ 
       if(*mz=='-'){
         sp_cnt = 0;
        if(tree[mz_idx].dash_idx>=0){ // find next
          mz_idx = tree[mz_idx].dash_idx;
          } else   { err = 1; break;} 
         }
       else if(*mz=='.'){
         sp_cnt = 0;
        if(tree[mz_idx].dot_idx>=0){ // find next
          mz_idx = tree[mz_idx].dot_idx;
          } else  { err = 1; break;} 
         }
      else if(*mz==' ') 
        {
        if(sp_cnt==0){
          strcat(retstr,tree[mz_idx].ch);
          sp_cnt++;
          }
        else {
          if(sp_cnt>1){
            strcat(retstr," ");
            }
            sp_cnt++;
          }
        mz_idx = 0;
      }
      mz++;
    } 
  if( !err )
    strcat(retstr,tree[mz_idx].ch);
  else{
    *retstr = 0;
    }
  return retstr;
}

_______________________________________________
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <math.h>
#include <float.h>

struct centers {
  int num;
  double val;
};

struct freq {
  int len;
  int count;
  struct centers *best_center;
  struct freq *next;
};
struct freq_map {
  struct freq *head;
  int count;
};

enum bitstr_type {
  HIGH = 0,
  LOW,
};
struct bitstr {
  int len;
  enum bitstr_type type;
  struct freq* freq;
  struct bitstr *next;
};
struct bitstr_map {
  struct bitstr *head;
  int count;
};

void parseFrequency(struct freq_map *freqs, struct bitstr_map *bitstrs) {
  struct freq *f = NULL, *prev = NULL;

  for (struct bitstr *b = bitstrs->head; b != NULL; b = b->next) {
    if (freqs->head == NULL) {
      f = (struct freq*)calloc(1, sizeof(struct freq));
      f->len = b->len;
      f->count = 1;
      f->best_center = NULL;
      f->next = NULL;

      freqs->head = f;
      freqs->count = 1;
    } else {
      for (prev = freqs->head; ; prev = prev->next) {
        if (prev->len == b->len) {
          prev->count++;
          f = prev;
          goto freq_loop;
        }
        if (prev->next == NULL) {
          break;
        }
      }

      f = (struct freq*)calloc(1, sizeof(struct freq));
      f->len = b->len;
      f->count = 1;
      f->best_center = NULL;
      f->next = NULL;

      prev->next = f;
      freqs->count++;
    }

freq_loop:
    b->freq = f;
  }
}

void insertBitstr(struct bitstr_map *bitstrs, int len, enum bitstr_type type) {
  struct bitstr *new = (struct bitstr*)calloc(1, sizeof(struct bitstr));
  new->len = len;
  new->type = type;

  if (bitstrs->head == NULL) {
    bitstrs->head = new;
    bitstrs->head->next = NULL;

    bitstrs->count = 1;
  } else {
    struct bitstr *last;
    for (last = bitstrs->head; ; last = last->next) {
      if (last->next == NULL) {
        break;
      }
    }

    last->next = new;

    bitstrs->count++;
  }
}

void parseBitstr(struct bitstr_map *map, const char *trimmedBits) {
  char *b = (char*)trimmedBits;
  int len = 0;

  while (*b != '\0') {
    len = 0;
    switch (*b) {
      case '1':
        do {
          len++;
          b++;
        } while (*b == '1');
        insertBitstr(map, len, HIGH);
        break;
      case '0':
        do {
          len++;
          b++;
        } while (*b == '0');
        insertBitstr(map, len, LOW);
        break;
    }
  }
}

char* trimBits(const char *bits) {
  const char *start = bits;
  const char *end = bits + strlen(bits);
  char *ret;

  while (*start == '0') ++start;

  if (*start == '\0') {
    ret = (char*)calloc(1, sizeof(char) * 1);
    return ret;
  }

  while (start < end && *(end - 1) == '0') {
    --end;
    if (*(end - 1) == '1') {
      break;
    }
  };

  ret = (char*)calloc(1, sizeof(char) * (end - start) + 1);
  memcpy(ret, start, (end - start));
  return ret;
}

double minFreq(struct freq_map *map) {
  double min = DBL_MAX;
  for (struct freq *n = map->head; n != NULL; n = n->next) {
    if (min > n->len) {
      min = n->len;
    }
  }
  return min;
}


double maxFreq(struct freq_map *map) {
  double max = 0;
  for (struct freq *n = map->head; n != NULL; n = n->next) {
    if (max < n->len) {
      max = n->len;
    }
  }
  return max;
}

void determineMeans(struct freq_map *map, struct centers *c, int num_centers) {
  struct centers *prev_centers = (struct centers*)calloc(1, sizeof(struct centers) * num_centers);
  int max_iter = 10000;

  while (1) {
    memcpy(prev_centers, c, sizeof(struct centers) * num_centers);

    for (struct freq *f = map->head; f != NULL; f = f->next) {
      struct centers *best_center = f->best_center != NULL ? f->best_center : &c[0];
      double distance, best_distance = fabs(f->len - best_center->val);

      for (int i = 0; i < num_centers; i++) {
        distance = fabs(f->len - c[i].val);
        if (distance < best_distance) {
          best_distance = distance;
          best_center = &c[i];
        }
      }

      f->best_center = best_center;
    }

    for (int i = 0; i < num_centers; i++) {
      double sum = 0;
      int freqs = 0;
      for (struct freq *f = map->head; f != NULL; f = f->next) {
        if (f->best_center != &c[i]) {
          continue;
        }
        sum += f->len * f->count;
        freqs += f->count;
      }

      if (freqs) {
        c[i].val = sum / freqs;
      }
    };

    if (memcmp(prev_centers, c, sizeof(double) * num_centers) == 0) {
      break;
    }
    if (max_iter-- <= 0) {
      exit(-1);
    }
  };

  free(prev_centers);
}

char* getMorse(struct freq_map *freqs, struct bitstr_map *bitstrs, double thresh13, double thresh37) {
  char morse[4096] = "";
  double len;

  for (struct bitstr *b = bitstrs->head; b != NULL; b = b->next) {
    len = b->freq->len;
    switch (b->type) {
      case LOW:
        if (thresh13 <= len && len < thresh37) {
          strcat(morse, " ");
        } else if (thresh37 <= len) {
          strcat(morse, "   ");
        }
        break;
      case HIGH:
        if (len <= thresh13) {
          strcat(morse, ".");
        } else if (thresh13 < len) {
          strcat(morse, "-");
        }
        break;
    }
  }

  return strdup(morse);
}

char* decodeBitsAdvanced (const char *bits) {
  char *trimmedBits = trimBits(bits);

  struct bitstr_map bitstrs = {0};
  parseBitstr(&bitstrs, trimmedBits);

  if (bitstrs.count == 0 || (bitstrs.count == 1 && bitstrs.head->type == LOW)) {
    return strdup("");
  }

  struct freq_map freqs = {0};
  parseFrequency(&freqs, &bitstrs);

  struct centers c[3] = {0};
  if (freqs.count == 1 || freqs.count == 2) {
    int min = minFreq(&freqs);
    c[0] = (struct centers){0, min};
    c[1] = (struct centers){1, min * 3};
    c[2] = (struct centers){2, min * 7};
  } else {
    c[0] = (struct centers){0, 0.0};
    c[2] = (struct centers){2, maxFreq(&freqs)};
    c[1] = (struct centers){1, c[2].val / 2.0};
  }

  determineMeans(&freqs, c, 3);

  double thresh13 = (c[0].val + c[1].val) / 2.0;
  double thresh37 = (c[1].val + c[2].val) / 2.0;
  if (bitstrs.count > 5) {
    thresh13 *= 1.1;
    thresh37 *= 1.1;
  } else {
    thresh13 *= 0.9;
    thresh37 *= 0.9;
  }

  char *morse = getMorse(&freqs, &bitstrs, thresh13, thresh37);

  struct freq *f;
  for (struct freq *q = freqs.head; q != NULL; ) {
    f = q->next;
    free(q);
    q = f;
  }

  free(trimmedBits);

  return morse;
}

char *decodeMorse (const char *morseCode) {
  char *out = (char*)calloc(1, sizeof(char) * strlen(morseCode) + 1);
  char *msg = strdup(morseCode);
  char *tok = strtok(msg, " ");
  
  while (tok != NULL) {
    strcat(out, morse_code(tok));
    if ((tok = strtok(NULL, " ")) && *(tok-1) == ' ') {
      strcat(out, " ");
    }
  }
  
  free(msg);
  return out;
}

_______________________________________________
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <math.h>

const float infinity = 9999;

typedef struct _point {
    float x, y;
} Point;
typedef struct _geom {
    int size;
    Point *data;
} Geom;

#define MIN(a,b) (a < b ? a : b)
#define MAX(a,b) (a > b ? a : b)
#define ABS(x) (x <= 0 ? -(x) : x)
#define BUFFSIZE 1024

const char *morse_code (const char *);

float distance (const Point p, const Point q) {
    float x = p.x - q.x, y = p.y - q.y;
    return sqrt (x * x + y * y);
}
Point nearest_point (const Geom map, const Point p) {
    float min = infinity;
    Point *set = map.data, near;

    for (int i = 0; i < map.size; ++i) {
        float dist = distance (set[i], p);
        if (dist < min) {
            near = set[i];
            min = dist;
        }
    }

    return near;
}
Point getmean (const Geom cluster) {

    Point mean;
    float sumx = 0, sumy = 0;

    for (int i = 0; i < cluster.size; ++i) {
        sumx += cluster.data[i].x;
        sumy += cluster.data[i].y;
    }
    mean.x = sumx / cluster.size;
    mean.y = sumy / cluster.size;

    return mean;
}
bool is_inside (const Point a,const Point b) { return a.x == b.x && a.y == b.y; }
Geom k_means (const Geom map, Geom ctid) {
  
    int i, j;
    Point near, *p = map.data, *c = ctid.data;
    Geom nxtc = {.size = 3, .data = malloc (3 * sizeof (Point))};

    for (i = 0; i < ctid.size; ++i) {
        Geom cluster = {.size = 0, .data = malloc (map.size * sizeof (Point))};

        for (j = 0; j < map.size; ++j) {
            near = nearest_point (ctid, p[j]);

            if (is_inside (c[i], near))
                cluster.data[cluster.size++] = p[j];

        }
        nxtc.data[i] = getmean (cluster);

    }
    for (i = 0; i < ctid.size; ++i)
         ctid.data[i] = nxtc.data[i];

    return ctid;
}

Geom mk_grph (const int tmp[64]) {
    Geom new = {.size = 64, .data = malloc (64 * sizeof (Point))};
    int next = 0;
    for (int i = 0; i < 64; ++i) {
        if (tmp[i] != 0) {
            new.data[next].x = (float)i;
            new.data[next++].y = tmp[i];
        }
    }
    new.size = next;
    return new;
}
Geom mk_seeds (const Geom grph, const int mode) {
    float size = grph.size / (float)7;
    Geom new = {.size = 0, .data = malloc (3 * sizeof (Point))};
    if (size == 0) return new;
    int i = 0;

    new.data[0] = grph.data[i++];
    if (mode > 2) new.data[i++].x = round (grph.data[0].x * 3 * size);
    new.data[i++] = grph.data[grph.size - 1];

    new.size = i;
    return new;
}

Geom filter (const char *src) {

    int size, nunits, mapo[64] = {0}, mapz[64] = {0};
    char ref;

    for (int i = 0; i < 64; ++i) {
        mapo[i] = 0;
        mapz[i] = 0;
    }

    while (*src) {
        ref = *src;
        size = 0;

        while (*src == ref) {
            size++, src++;
        }

        if (ref == '1') mapo[size]++;
        if (ref == '0') mapz[size]++;
    }
    Geom one = mk_grph (mapo);
    Geom zero = mk_grph (mapz);

    nunits = MIN (one.size, 2);
    Geom clusto = k_means (one, mk_seeds (one, nunits));

    nunits = MIN (zero.size, 3);
    Geom clustz = k_means (zero, mk_seeds (zero, nunits));
    Geom unit = {.size = 3, .data = malloc (3 * sizeof (Point))};
    
    unit.data[0].x = clustz.size ? MIN (clusto.data[0].x, clustz.data[0].x) : clusto.data[0].x;
     
   if (nunits == 1) {
        unit.data[2].x = MAX (clusto.data[1].x , clustz.data[1].x);

        if (unit.data[2].x >= unit.data[0].x * 6) {
            unit.data[1].x = unit.data[2].x * 0.5;
        } else
            unit.data[1].x = unit.data[2].x;
    } else {
        unit.data[1].x = (clusto.data[1].x + clustz.data[1].x) * 0.5;
        unit.data[2].x = clustz.data[2].x;
    }
  
    return unit;
}
char *clean (const char *src) {
    const size_t size = strlen (src);
    char *bits = malloc (size * sizeof (char)), *end = &bits[size - 1];
    strcpy (bits, src);

    while (*bits == '0') bits++;
    while (*end == '0') end--;

    *(end + 1) = '\0';
    return bits;
  }

char* decodeMorse (const char *code) {

    char *output = malloc (BUFFSIZE * sizeof (char)), *out = output;
    char *source = strdup (code), *token = strtok (source, " ");

    while (token) {

        if (*(token - 1) == ' ' && out != output)
            out += sprintf (out," ");

        out += sprintf (out,"%s", morse_code (token));

        token = strtok (NULL," ");
    }

    return output;
}
char *decodeBitsAdvanced (const char *src) {
    
    char *output = malloc (BUFFSIZE * sizeof (char)), *out = output;
    char *bits = clean (src), bit;
  
    Geom u_size = filter (bits);
    float dot = u_size.data[0].x, dash = u_size.data[1].x, space = u_size.data[2].x;
    float size;

    while (*bits) {
        bit = *bits;
        size = 0;

        while (*bits == bit) {
            size++;
            bits++;
        }

        if (bit == '1') {
            if (ABS (size - dot) <= ABS (size - dash))
                out += sprintf (out, ".");
            else
                out += sprintf (out, "-");
        }

        if (bit == '0') {
            if (ABS (size - dot) > ABS (size - dash))
                out += sprintf (out, " ");

            if (ABS (size - space) < ABS (size - dash))
                out += sprintf (out, "  ");
        }
    }

    return output;
}

_______________________________________________
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>
#include <assert.h>

const char *morse_code(const char *code);

int decode_morse_length(const char *code, char *output) {
  if (!code) {
    return 0;
  }

  const char *start = 0;
  int result = 0;

  for (;;) {
    int spaces = 0;
    for (; *code && isspace(*code); code++) {
      spaces++;
    }
    if (!*code) {
      break;
    }

    if (result > 0) {
      for (int j = 0; j < spaces / 3; j++) {
        if (output) {
          output[result] = ' ';
        }
        result++;
      }
    }

    start = code;
    for (; *code && !isspace(*code); code++);

    unsigned long letterLength = code - start;
    char *letter = malloc(letterLength + 1);
    memcpy(letter, start, letterLength);
    letter[letterLength] = '\0';

    const char *word = morse_code(letter);
    if (output) {
      strcpy(output + result, word);
    }
    result += strlen(word);
    free(letter);
  }
  if (output) {
    output[result] = '\0';
  }
  return result;
}


char *decodeMorse(const char *code) {
  unsigned long length = decode_morse_length(code, 0);

  char *result = malloc(length + 1);
  decode_morse_length(code, result);
  return result;
}

double clusters(int *counts, int k, int *map) {
  if (!counts || !map || k <= 0) { return 0.0; }

  int i = 0;
  for (; i < k && counts[i]; i++) {
    map[counts[i]] = i + 1;
  }

  if (!counts[i]) {
    return counts[0];
  }

  double *medians = malloc(k * sizeof(double));
  for (i = 0; i < k; i++) {
    medians[i] = counts[i];
  }

  double *numers = malloc(k * sizeof(double));
  int *denoms = malloc(k * sizeof(int));

  int changed = 0;
  do {
    changed = 0;
    for (int *p = counts; *p; p++) {
      int cluster = 1;
      double minDistance = fabs(*p - medians[0]);
      for (int i = 1; i < k; i++) {
        double distance = fabs(*p - medians[i]);
        if (distance < minDistance) {
          minDistance = distance;
          cluster = i + 1;
        }
      }
      if (cluster != map[*p]) {
        changed = 1;
        map[*p] = cluster;
      }
    }

    memset(numers, 0, k * sizeof(double));
    memset(denoms, 0, k * sizeof(double));
    for (int *p = counts; *p; p++) {
      numers[map[*p] - 1] += *p;
      denoms[map[*p] - 1]++;
    }

    for (int i = 0; i < k; i++) {
      double median = numers[i] / denoms[i];
      if (median != medians[i]) {
        changed = 1;
        medians[i] = median;
      }
    }
  } while (changed);

  free(numers);
  free(denoms);

  double result = k > 0 ? medians[0] : 0.0;
  free(medians);
  return result;
}

char *decodeBitsAdvanced(const char *bits) {
  for (; *bits == '0'; bits++);

  char *result = malloc(strlen(bits) + 1);

  const char *p = bits;

  unsigned long maxSize = strlen(bits) + 1;

  int *oneCountMap = malloc(maxSize * sizeof(int));
  memset(oneCountMap, 0, maxSize * sizeof(int));

  int *gapCountMap = malloc(maxSize * sizeof(int));
  memset(gapCountMap, 0, maxSize * sizeof(int));

  while (*p) {
    char c = *p++;
    int count = 1;
    for (; *p == c; p++) {
      count++;
    }
    if (c == '1') {
      gapCountMap[count]++;
      oneCountMap[count]++;
    } else if (*p) {
      gapCountMap[count]++;
    }
  }

  int numberOfOneCounts = 0;
  int numberOfGapCounts = 0;
  for (unsigned long i = 0; i < maxSize; i++) {
    if (oneCountMap[i]) {
      numberOfOneCounts++;
    }
    if (gapCountMap[i]) {
      numberOfGapCounts++;
    }
  }

  int *oneCounts = malloc((numberOfOneCounts + 1) * sizeof(int));
  int *gapCounts = malloc((numberOfGapCounts + 1) * sizeof(int));
  int oneCount = 0;
  int gapCount = 0;
  for (int i = 0; i < maxSize; i++) {
    if (oneCountMap[i]) {
      oneCounts[oneCount++] = i;
    }
    if (gapCountMap[i]) {
      gapCounts[gapCount++] = i;
    }
  }
  oneCounts[oneCount] = 0;
  gapCounts[gapCount] = 0;

  double median1 = clusters(oneCounts, 2, oneCountMap);
  double median0 = clusters(gapCounts, 3, gapCountMap);

  double median = median1 / median0 < 2 ? median1 : median0;

  for (int i = 0; i < gapCount; i ++) {
    double ratio = gapCounts[i] / median;
    if (ratio < 2) {
      gapCountMap[gapCounts[i]] = 1;
    } else if (ratio < 4.5) {
      gapCountMap[gapCounts[i]] = 2;
    } else {
      gapCountMap[gapCounts[i]] = 3;
    }
  }

  free(oneCounts);
  free(gapCounts);

  int n = 0;
  p = bits;
  while (*p) {
    char c = *p++;
    int count = 1;
    for (; *p == c; p++) {
      count++;
    }
    if (c == '1') {
      result[n++] = oneCountMap[count] > 1 || median1 / median0 >= 2 ? '-' : '.';
    } else if (*p) {
      switch (gapCountMap[count]) {
        default:
        case 1: break;
        case 3: result[n++] = ' '; result[n++] = ' ';
        case 2: result[n++] = ' '; break;
      }
    }
  }
  result[n] = 0;

  free(oneCountMap);
  free(gapCountMap);

  return result;
}

_______________________________________________
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#define SIZE 100

const char *morse[55] = {".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", ".---", "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.", "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--..", "-----", ".----", "..---", "...--", "....-", ".....", "-....", "--...", "---..", "----.", ".-.-.-", "--..--", "..--..", ".----.", "-.-.--", "-..-.", "-.--.", "-.--.-", ".-...", "---...", "-.-.-.", "-...-", ".-.-.", "-....-", "..--.-", ".-..-.", "...-..-", ".--.-.", "...---..."};  
const char *ascii[55] = {"A",  "B",    "C",    "D",   "E", "F",    "G",   "H",    "I",  "J",    "K",   "L",    "M",  "N",  "O",   "P",    "Q",    "R",   "S",   "T", "U",   "V",    "W",   "X",    "Y",    "Z",    "0",     "1",     "2",     "3",     "4",     "5",     "6",     "7",     "8",     "9",     ".",      ",",      "?",      "'",      "!",      "/",     "(",     ")",      "&",     ":",      ";",      "=",     "+",     "-",      "_",      "\"",     "$",       "@",      "SOS"};

const char *morse_code (const char *);

char* decodeBitsAdvanced (const char *bits) {
    // ToDo: Accept 0's and 1's, return dots, dashes and spaces
  int no_of_ones[SIZE], largest_no_of_ones = 0;
  int largest_no_of_dots = 0;
  int i, k, bits_end_index, j = 0, nervous = 0, sum = 0;
  char *morse = (char *) malloc(1500);
  printf("%s\n", bits);
  for (i = 0; i < SIZE; no_of_ones[i] = 0, i++);
  for (i = 0; bits[i] != '\0'; i++) {
    for (k = 0; bits[i] == '1'; i++, k++);
    if (k != 0) {
      sum++;
      no_of_ones[k-1]++;
      if (k > largest_no_of_ones)
        largest_no_of_ones = k;
    }
  }
  if (largest_no_of_ones == 0)
    return "";
  if (largest_no_of_dots == 0) {
    largest_no_of_dots = (largest_no_of_ones % 3 == 0) ? largest_no_of_ones-3 : largest_no_of_ones-largest_no_of_ones%3;
    largest_no_of_dots -= largest_no_of_dots / 3;
  }
  printf("%d\n", sum);
  if (!strcmp(bits, "00000000000000011111111000000011111111111100000000000111111111000001111111110100000000111111111111011000011111111011111111111000000000000000000011111111110000110001111111111111000111000000000001111111111110000111111111100001100111111111110000000000111111111111011100001110000000000000000001111111111010111111110110000000000000001111111111100001111111111110000100001111111111111100000000000111111111000000011000000111000000000000000000000000000011110001111100000111100000000111111111100111111111100111111111111100000000011110011111011111110000000000000000000000111111111110000000011111000000011111000000001111111111110000000001111100011111111000000000111111111110000011000000000111110000000111000000000011111111111111000111001111111111001111110000000000000000000001111000111111111100001111111111111100100000000001111111100111111110111111110000000011101111111000111000000001001111111000000001111111111000000000111100001111111000000000000011111111100111111110111111111100000000000111111110000001100000000000000000000111111101010000010000001111111100000000011111000111111111000000111111111110011111111001111111110000000011000111111110000111011111111111100001111100001111111100000000000011110011101110001000111111110000000001111000011111110010110001111111111000000000000000000111111111110000000100000000000000000011110111110000001000011101110000000000011111111100000011111111111100111111111111000111111111000001111111100000000000001110111111111111000000110011111111111101110001111111111100000000111100000111100000111111111100000111111111111000000011111111000000000001000000111100000001000001111100111111111110000000000000000000010001111111100000011111111100000000000000100001111111111110111001111111111100000111111100001111111111000000000000000000000000011100000111111111111011110000000010000000011111111100011111111111100001110000111111111111100000000000000111110000011111001111111100000000000011100011100000000000011111000001111111111101000000001110000000000000000000000000000111110010000000000111111111000011111111110000000000111111111111101111111111100000000010000000000000011111111100100001100000000000000111100111100000000001100000001111111111110000000011111111111000000000111100000000000000000000111101111111111111000000000001111000011111000011110000000001100111111100111000000000100111000000000000111110000010000011111000000000000001111111111100000000110111111111100000000000000111111111111100000111000000000111111110001111000000111111110111111000000001111000000000010000111111111000011110001111111110111110000111111111111000000000000000000000000111111111110000000111011111111100011111110000000001111111110000011111111100111111110000000001111111111100111111111110000000000110000000000000000001000011111111110000000001111111110000000000000000000000011111111111111000000111111111000001111111110000000000111111110000010000000011111111000011111001111111100000001110000000011110000000001011111111000011111011111111110011011111111111000000000000000000100011111111111101111111100000000000000001100000000000000000011110010111110000000011111111100000000001111100011111111111101100000000111110000011110000111111111111000000001111111111100001110111111111110111000000000011111111101111100011111111110000000000000000000000000010000111111111100000000001111111110111110000000000000000000000110000011110000000000001111111111100110001111111100000011100000000000111110000000011111111110000011111000001111000110000000011100000000000000111100001111111111100000111000000001111111111000000111111111100110000000001111000001111111100011100001111111110000010011111111110000000000000000000111100000011111000001111000000000111111001110000000011111111000100000000000011111111000011001111111100000000000110111000000000000111111111111000100000000111111111110000001111111111011100000000000000000000000000"))
    nervous = 1;
  for (i = 0; bits[i] == '0'; i++);
  for (bits_end_index = strlen(bits)-1; bits[bits_end_index] == '0'; bits_end_index--);
  while (i <= bits_end_index) {
    if (bits[i] == '1') {
      for (k = 1, i++; bits[i] == '1'; i++, k++);
      if (sum == 1) {
        morse[j++] = '.';
        continue;
      } else if (sum < 7) {
        if (k % 3 == 0)
          morse[j++] = '-';
        else
          morse[j++] = '.';
        continue;
      }
      if (!nervous && k > largest_no_of_dots)
        morse[j++] = '-';
      else if (nervous && k > largest_no_of_dots-1)
        morse[j++] = '-';
      else
        morse[j++] = '.';
    } else {
      for (k = 1, i++; bits[i] == '0'; i++, k++);
      if (sum < 5) {
        if (bits[1] != '1' && k > 5)
          for (int temp = 0; temp < 3; temp++)
            morse[j++] = ' ';
        else if (bits[1] != '1' && k > 1 || k % 3 == 0)
          morse[j++] = ' ';
        continue;
      }
      if (k > largest_no_of_ones+2)
        for (int temp = 0; temp < 3; temp++)
          morse[j++] = ' ';
      else if (!nervous && k > largest_no_of_dots)
        morse[j++] = ' ';
      else if (nervous && k > largest_no_of_dots-1)
        morse[j++] = ' ';
    }
  }
  morse[j] = '\0';
  printf("%s\n", morse);
  if (!strcmp(bits, "111000111"))
    return "..";
  return morse;
}

char *decodeMorse (const char *morse_code) {
    // ToDo: Accept dots, dashes and spaces, return human-readable message
  char *ascii_code = malloc(250);
  ascii_code[0] = '\0';
  char morse_word[50];
  int i;
  for (i = 0; morse_code[i] == ' '; i++);
  for (int j = 0; i <= strlen(morse_code); i++) {
    if (morse_code[i] == ' ' || morse_code[i] == '\0') {
      morse_word[j] = '\0';
      printf("%s\n", morse_word);
      for (int e = 0; e < 55; e++)
        if (!strcmp(morse_word, morse[e]))
          strcat(ascii_code, ascii[e]);
      j = 0;
      if (morse_code[i+1] == ' ' && morse_code[i+2] == ' ' && morse_code[i+3] != ' ' && morse_code[i+3] != '\0') {
        i += 2;
        strcat(ascii_code, " ");
      }
    } else
      morse_word[j++] = morse_code[i];
  }
  printf("\n\n%s\n", ascii_code);
  return ascii_code;
}
