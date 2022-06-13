#include <map>
#include <iterator>
#include <cmath>
using namespace std;

double earth_movers_distance(const vector<double> &x, const vector<double> &px,
                             const vector<double> &y, const vector<double> &py)
{
  std::map<double, double> probability; 
  for (unsigned i = 0; i < x.size(); i ++) probability[x[i]] += px[i];
  for (unsigned i = 0; i < y.size(); i ++) probability[y[i]] -= py[i];
  double distance = 0.;
  for (auto it = probability.begin(); it != probability.end(); it ++) {
    if (it->second != 0.) {
      auto it_next = next(it);
      distance += fabs((it->first - it_next->first) * it->second);
      it_next->second += it->second;
      it -> second = 0.;
    } 
  };
  
  return distance;
}
_________________________________________________
#include <cmath>
#include <iterator>
#include <map>
#include <vector>
#include <utility>

using std::pair;
using std::vector;

double earth_movers_distance(const vector<double>& x, const vector<double>& px,
                             const vector<double>& y, const vector<double>& py)
{
  std::map<double, double> xmap, ymap;
  for (std::size_t i = 0; i < x.size(); i++) {
    xmap[x[i]] = px[i];
    if (!ymap.count(x[i])) ymap[x[i]] = 0;
  }
  for (std::size_t i = 0; i < y.size(); i++) {
    ymap[y[i]] = py[i];
    if (!xmap.count(y[i])) xmap[y[i]] = 0;
  }
  vector<pair<double, double>> xs {xmap.begin(), xmap.end()},
                               ys {ymap.begin(), ymap.end()};
  double dist = 0.0;
  std::size_t i = 0, j = 0;
  while (i < xs.size() && j < ys.size()) {
    auto& [kx, vx] = xs[i];
    auto& [ky, vy] = ys[j];
    if (kx == ky) {
      if (vy >= vx) {
        vy -= vx;
      } else {
        dist += (xs[i + 1].first - kx) * (vx - vy);
        xs[i + 1].second += vx - vy;
        j++;
      }
      i++;
    } else if (vy > vx) {
      dist += (kx - ky) * vx;
      vy -= vx;
      i++;
    } else {
      dist += (kx - ky) * vy;
      vx -= vy;
      j++;
    }
  }
  return dist;
}
_________________________________________________
using namespace std;

vector<pair<double, double>> zipSort(const vector<double> &u, const vector<double> &v) {
  vector<pair<double, double>> res (u.size());
  transform(u.cbegin(), u.cend(), v.cbegin(), res.begin(), 
            [](double a, double b){return make_pair(a, b);});
  sort(res.begin(), res.end());
  return res;
}

double earth_movers_distance(const vector<double> &x, const vector<double> &px,
                             const vector<double> &y, const vector<double> &py) {  
  double res = 0;
  auto xx = zipSort(x, px);
  auto yy = zipSort(y, py);
  
  pair<double, double> xx_;
  pair<double, double> yy_;
  
  yy_ = yy.back();
  yy.pop_back();
  
  while (xx.size() > 0) {
    xx_ = xx.back();
    xx.pop_back();
    
    while (true) {
      res += abs(xx_.first - yy_.first) * min(xx_.second, yy_.second);
      if (yy_.second < xx_.second) {
        xx_.second -= yy_.second;
        yy_ = yy.back();
        yy.pop_back();
      } else {
        yy_.second -= xx_.second;
        break;
      }
    }
  }
  
  return res;
}
_________________________________________________
#include<cmath>
using namespace std;

struct Atom
{
 double x,p;
  
 Atom(double x, double p) : x(x), p(p) {}
 bool operator<(const Atom &other) { return x < other.x; }
};

double earth_movers_distance(const vector<double> &x, const vector<double> &px,
                             const vector<double> &y, const vector<double> &py)
{
 vector<Atom> d;
  
 for(unsigned i=0; i != x.size(); i++)
   d.emplace_back(x[i], px[i]);
 for(unsigned i=0; i != y.size(); i++)
   d.emplace_back(y[i], -py[i]);
                  
 sort(d.begin(), d.end());
                  
 double f = 0.0, sum = 0.0, last = 0.0;
 for( const Atom &a : d )
 {
   sum += fabs(f) * (a.x - last);
   f += a.p;
   last = a.x;
 }
   
 return sum;
}
