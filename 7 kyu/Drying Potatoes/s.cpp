int potatoes(int p0, int w0, int p1) {
  return w0 * (100 - p0) / (100 - p1);
}int potatoes(int p0, int w0, int p1) {
  return w0 * (100 - p0) / (100 - p1);
}
_______________________________________________
using namespace std;

int potatoes(int p0, int w0, int p1)
{
    return static_cast<int>(static_cast<double>(w0) * (100.0 - static_cast<double>(p0)) / (100.0 - static_cast<double>(p1)));
}
_______________________________________________
using namespace std;

double potatoes(int p0, int w0, int p1)
{
  p0=100-p0;
  p1=100-p1;
  double w = (double)p0/(double)p1*w0;
  return (int)w;
}
_______________________________________________
#include <cmath>

int potatoes(int p0, int w0, int p1)
{
    return floor(w0 * abs(100 - p0) / abs(100 - p1));
}
_______________________________________________
using namespace std;

int potatoes(int p0, int w0, int p1)
{
  int dryMass = w0 * 100 - w0 * p0;
  float ret = dryMass / (100 - p1);
  return int(ret);
}
_______________________________________________
#include<cmath>
using namespace std;

int potatoes(int p0, int w0, int p1)
{
  double w1 = (w0*(p0 - p1))/(double)(100 - p1);
  return w0 - w1;
}
