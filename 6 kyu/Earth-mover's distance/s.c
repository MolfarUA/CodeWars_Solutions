#include <math.h>
#include <stdlib.h>

typedef struct { double x, p; } Atom;

// Comparison for sorting atoms by their x component:
int atom_cmp(const void *a, const void *b)
{
 double x1 = ((Atom*)a)->x, x2 = ((Atom*)b)->x;
 return x1 > x2 ? 1 : x1 == x2 ? 0 : -1;
}

double earth_movers_distance(double x[], double px[], unsigned nx,
                             double y[], double py[], unsigned ny)
{
 Atom d[ nx + ny ];
 for(unsigned i=0; i != nx; i++)
 {
   d[i].x = x[i];
   d[i].p = px[i];
 }
 for(unsigned i=0; i != ny; i++)
 {
   d[nx + i].x = y[i];
   d[nx + i].p = -py[i];
 }
  
 qsort(d, nx + ny, sizeof(double)*2, atom_cmp);
  
 double f = 0.0, sum = 0.0, last = 0.0;
 for(unsigned i=0; i != nx+ny; i++)
 {
   sum += fabs(f) * (d[i].x - last);
   f += d[i].p;
   last = d[i].x;
 }
   
 return sum;
} 
_________________________________________________
#include <math.h>
#include <stdlib.h>

typedef struct { double x, p; } pt_s;

int pt_cmp (const void *p1, const void *p2)
{
    double d = ((const pt_s *)p1)->x - ((const pt_s *)p2)->x;
    return (d < 0) ? -1 : (d > 0) ? 1 : 0;
}

double earth_movers_distance(double x[], double px[], unsigned numx,
                             double y[], double py[], unsigned numy)
{
    pt_s *ptx = malloc(numx*sizeof(pt_s));
    for (unsigned ix = 0; ix < numx; ++ix) {
        ptx[ix].x = x[ix];
        ptx[ix].p = px[ix];
    }
    qsort(ptx, numx, sizeof(pt_s), pt_cmp);
  
    pt_s *pty = malloc(numy*sizeof(pt_s));
    for (unsigned iy = 0; iy < numy; ++iy) {
        pty[iy].x = y[iy];
        pty[iy].p = py[iy];
    }
    qsort(pty, numy, sizeof(pt_s), pt_cmp);
  
    double r = 0, vx = 0, vy = 0;
    for (unsigned ix = 0, iy = 0; ix < numx && iy < numy;) {
        if (vx == 0) { vx = ptx[ix].p; }
        if (vy == 0) { vy = pty[iy].p; }
        double v = fmin(vx, vy);
        r += v*fabs(ptx[ix].x - pty[iy].x);
        vx -= v;
        vy -= v;
        if (vx == 0) { ++ix; }
        if (vy == 0) { ++iy; }
    }
  
    free(ptx);
    free(pty);
  
    return r;
}
_________________________________________________
int comp(const void *a, const void *b) { 
  const double (*ia)[2] = a; 
  const double (*ib)[2] = b;
  if ((*ia)[0]<(*ib)[0]) return -1; 
  if ((*ia)[0]>(*ib)[0]) return +1;
  return 0;
}

double earth_movers_distance(double x[], double px[], unsigned numx, double y[], double py[], unsigned numy) {
  
  unsigned n = numx+numy;
  double emd=0.0, tx[numx][2], ty[numy][2], z[n][3];
  int sortedx=1, sortedy=1;
  
  for (unsigned i=0; i<numx; i++) { tx[i][0]=x[i]; tx[i][1]=px[i]; if (i>0 && (tx[i][0]-tx[i-1][0])<0) sortedx=0; }
  for (unsigned i=0; i<numy; i++) { ty[i][0]=y[i]; ty[i][1]=py[i]; if (i>0 && (ty[i][0]-ty[i-1][0])<0) sortedy=0; }  
  
  if (!sortedx) qsort(tx, numx, sizeof(double)*2, comp);
  if (!sortedy) qsort(ty, numy, sizeof(double)*2, comp);

  unsigned i=0, j=0, k=0;
  while (i<numx && j<numy) {
    if (tx[i][0]>ty[j][0])  { z[k][0]=ty[j][0]; z[k][1]=0;        z[k][2]=ty[j][1]; j++; k++;      continue; }
    if (tx[i][0]<ty[j][0])  { z[k][0]=tx[i][0]; z[k][1]=tx[i][1]; z[k][2]=0;        i++; k++;      continue; }
    if (tx[i][0]==ty[j][0]) { z[k][0]=tx[i][0]; z[k][1]=tx[i][1]; z[k][2]=ty[j][1]; i++; j++; k++; continue; }
  }
  
  for (; i<numx; i++, k++) { z[k][0]=tx[i][0]; z[k][1]=tx[i][1]; z[k][2]=0; }
  for (; j<numy; j++, k++) { z[k][0]=ty[j][0]; z[k][1]=0;        z[k][2]=ty[j][1]; }  
  
  double bal=0.0;
  for (unsigned i=0; i<k-1; i++) {
    bal += z[i][1]-z[i][2];
    emd =  (bal>=0) ? emd + (z[i+1][0]-z[i][0])*bal : emd;
  }
  
  bal=0.0;
  for (unsigned i=k-1; i>0; i--) {
    bal += z[i][1]-z[i][2];
    emd =  (bal>=0) ? emd + (z[i][0]-z[i-1][0])*bal : emd;
  }

  return emd;
}
_________________________________________________
#include <math.h>
#include <stdlib.h>

typedef struct Probability {
  double value;
  double probability;
} Probability;

int probCmp(const void *va, const void *vb) {
  Probability *a = (Probability *)va, *b = (Probability *)vb;
  return (a->value < b->value) - (a->value > b->value);
}

double earth_movers_distance(double vx[], double px[], unsigned nx,
                             double vy[], double py[], unsigned ny) {
  double work = 0; unsigned ix = 0;
  Probability x[nx], y[ny];
  for (unsigned i = 0; i < nx; ++i) {
    x[i].value = vx[i];
    x[i].probability = px[i];
  }
  for (unsigned i = 0; i < ny; ++i) {
    y[i].value = vy[i];
    y[i].probability = py[i];
  }
  qsort(x,nx,sizeof x[0], probCmp);
  qsort(y,ny,sizeof y[0], probCmp);
  for (unsigned iy = 0; iy < ny; ++iy) while (1) {
    if (y[iy].probability > x[ix].probability) {
      work += x[ix].probability * fabs(y[iy].value - x[ix].value);
      y[iy].probability -= x[ix].probability;
      ++ix;
    } else {
      work += y[iy].probability * fabs(y[iy].value - x[ix].value);
      x[ix].probability -= y[iy].probability;
      break;
    }
  }
  return work;
}
_________________________________________________
#include <stdlib.h>

typedef struct pw {
    double p;
    double w;
} pw;

int srt( const void *a, const void *b )
{
    const pw *pwa = a;
    const pw *pwb = b;
    if ( pwa->p > pwb->p) {
        return 1;
    }
    if ( pwa->p < pwb->p ) {
        return -1;
    }
    return 0;
}

double earth_movers_distance(double x[], double px[], unsigned numx,
                             double y[], double py[], unsigned numy)
{
    pw *ax = malloc( numx * sizeof(pw) );
    pw *ay = malloc( numy * sizeof(pw) );
    unsigned iy = 0;
    double emd = 0.0;
  
    for ( unsigned i = 0; i < numx; i++ ) {
        ax[i].p = x[i];
        ax[i].w = px[i];
    }
    for ( unsigned i = 0; i < numy; i++ ) {
        ay[i].p = y[i];
        ay[i].w = py[i];
    }

    qsort( ax, numx, sizeof(pw), srt );
    qsort( ay, numy, sizeof(pw), srt );

    for ( unsigned x = 0; x < numx; x++ ) {
        for ( unsigned y = 0; y < numy; y++ ) {
            if ( ax[x].p == ay[y].p ) {
                if ( ax[x].w > ay[y].w ) {
                    ax[x].w -= ay[y].w;
                    ay[y].w = 0.0;
                }
                else {
                    ay[y].w -= ax[x].w;
                    ax[x].w = 0.0;
                }
            }
        }
    }

    for ( unsigned x = 0; x < numx; x++ ) {
        while ( ax[x].w > 0.0 ) {
            if ( ay[iy].w == 0.0 ) {
                iy++;
            }
            else {
                double d = ax[x].p - ay[iy].p;
                if ( d < 0.0 ) {
                    d = -d;
                }
                if ( ax[x].w > ay[iy].w ) {
                    d *= ay[iy].w;
                    ax[x].w -= ay[iy].w;
                    ay[iy].w = 0.0;
                }
                else {
                    d *= ax[x].w;
                    ay[iy].w -= ax[x].w;
                    ax[x].w = 0.0;
                }
                emd += d;
            }
        }
    }
   
    free( ax );
    free( ay );
    return emd;
}
