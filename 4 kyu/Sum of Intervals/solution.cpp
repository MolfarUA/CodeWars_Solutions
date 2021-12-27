#include <vector>
#include <utility>
#include <algorithm>

using namespace std;

int sum_intervals(vector<pair<int, int>> v) {
  sort(v.begin(), v.end(), [](auto x, auto y){return x.first != y.first ? x.first < y.first : x.second < y.second;});
  int r = 0, last = v[0].first;
  for (auto p : v) {
    int x = p.first, y = p.second;
    if (y <= last) continue;
    r += y - max(x, last);
    last = y;
  }
  return r;
}

_________________________
#include <vector>
#include <numeric>

int sum_intervals(std::vector<std::pair<int, int>> intervals) { 
  std::sort(intervals.begin(), intervals.end());
  return std::accumulate(intervals.begin(), intervals.end(), 0, [boundary = intervals[0].first] (auto sum, const auto &p) mutable 
      { if (boundary < p.second) { sum += p.second - std::max(boundary, p.first); boundary = p.second; } return sum; });
}

_________________________
#include <vector>
#include <utility>
#include <unordered_set>

int sum_intervals(std::vector<std::pair<int, int>> intervals) {
  
  std::unordered_set<int> ints;
  for (auto interv = intervals.begin(); interv != intervals.end(); ++interv){
    for (int i = interv->first; i < interv->second; i++){
      ints.insert(i);
    }
  }

return ints.size();
}

_________________________
#include <vector>
#include <utility>

int sum_intervals(std::vector<std::pair<int, int>> interavls) {
  sort(interavls.begin(), interavls.end());
  int ret = 0;
  int max_right = interavls[0].first;
  for (auto &i : interavls)
       if (i.second >= max_right) {
           ret += i.second - std::max(max_right, i.first);
           max_right = i.second;
       }
  return ret;
}

_________________________
#include <vector>
#include <set>

int sum_intervals(std::vector<std::pair<int, int>> intervals) {
  std::set<int> s;
    for(const auto& it : intervals)
        for(int cnt = it.first; cnt != it.second; ++cnt)
            s.insert(cnt);
    return s.size();
}

_________________________
#include <vector>
#include <utility>

bool check(const std::vector<std::pair<int, int>>& itvs, int num) {
  for (const auto& pair : itvs) {
    if (num >= pair.first && num < pair.second) {
      return true;
    }
  }
  return false;
}

int sum_intervals(std::vector<std::pair<int, int>> itvs) {
  int sum {0};
  int min {itvs[0].first};
  int max {itvs[0].second};
  
  for (unsigned long i = 0; i < itvs.size(); i++) {
    std::cout << itvs[i].first << " " << itvs[i].second << std::endl;
    if (itvs[i].first <= min) {
      min = itvs[i].first;
    }
    if (itvs[i].second > max) {
      max = itvs[i].second;
    }
  }
  
  for (int i = min; i <= max; i++) {
    if (check(itvs, i)) {
      sum++;
    }
  }
  std::cout << std::endl;
  return sum;
}
