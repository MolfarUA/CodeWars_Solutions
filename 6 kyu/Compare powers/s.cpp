55b2549a781b5336c0000103
  
  
#include <math.h>

int comparePowers(std::pair<long, long> n1, std::pair<long, long> n2) {
  double l = n1.second * log(n1.first);
  double r = n2.second * log(n2.first);
  return l == r ? 0 : l < r ? 1 : -1;
}
________________________________
#include <cmath>
int comparePowers(std::pair<long, long> n1, std::pair<long, long> n2){
  return (log2(n1.first)*n1.second == log2(n2.first)*n2.second)? 0: (log2(n1.first)*n1.second > log2(n2.first)*n2.second)? -1: 1;
}
________________________________
#include<math.h>
int comparePowers(std::pair<long, long> n1, std::pair<long, long> n2){
  return (n1.second*log2(n1.first)> n2.second*log2(n2.first)) ? -1 : (n1.second*log2(n1.first) == n2.second*log2(n2.first))? 0: 1;
}
