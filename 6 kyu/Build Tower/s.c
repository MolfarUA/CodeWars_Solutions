576757b1df89ecf5bd00073b


void build_tower(unsigned n, char tower[n][2 * n - 1])
{
  unsigned i, j, l=2*n-1;  
  for(i=0;i<n;i++)
  {
    for(j=0;j<l;j++)
      tower[i][j]='*';
  }
  if(n>1)
  {
    for(i=1;i<=n;i++)
    {
      for(j=0;j<l;j++)
      {
        if(j<l-(l-i+1)||j>l-i)
          tower[n-i][j]=' ';
      }
    }
  }
}
_____________________________
#include <string.h>

void build_tower(unsigned n, char tower[n][2 * n - 1]) {
  for (unsigned i = 0; i < n; i++) {
    memset(tower[i], ' ', 2 * n - 1);
    memset(tower[i] + (n - i - 1), '*', 2 * i + 1);
  }
}
_____________________________
#include <string.h>

void build_tower(unsigned n, char tower[n][2 * n - 1])
{
    for (unsigned i = 0; i < n; ++i) {
        char *s = tower[i];
        memset(s, ' ', n - i - 1); s += n - i - 1;
        memset(s, '*', 1 + i*2); s += 1 + i*2;
        memset(s, ' ', n - i - 1);
    }
}
_____________________________
void build_tower(unsigned n, char tower[n][2 * n - 1])
{
  
  int edge = 2 * n - 1;
  int spaces = 0;
  for (int fl = n-1; fl >= 0; fl--, spaces++){
    for (int bl = spaces; bl < edge; bl++){
      tower[fl][bl] = '*';
    }
    for (int bl = 0; bl < spaces; bl++){
      tower[fl][bl] = ' ';
      tower[fl][edge - bl -1] = ' ';
    }
  }
}
_____________________________
void build_tower(unsigned n, char tower[n][2 * n - 1])
{
  int w = (2 * n - 1) / 2;
  for (int i = 0; i < n; i++)
    for (int j = 0; j < (2 * n) - 1; j++)
    {
      if (j >= w - i && j <= w + i)
        tower[i][j] = '*';
      else
        tower[i][j] = 32;
    }
}
_____________________________
void build_tower(unsigned n, char tower[n][2 * n - 1])
{
  unsigned pre = n-1, mid = 1, pos = n-1;
  for(unsigned c=0;c<n;c++) {
    char *ptr = tower[c];
    // pre
    for(int i=0;i<pre;i++)
      *(ptr++) = ' ';
    // mid
    for(int i=0;i<mid;i++)
      *(ptr++) = '*';
    // pos
    for(int i=0;i<pos;i++)
      *(ptr++) = ' ';
    pre--;
    mid+=2;
    pos--;
  }
}
