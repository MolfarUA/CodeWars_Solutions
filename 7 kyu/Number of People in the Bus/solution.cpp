#include<vector>

unsigned int number(const std::vector<std::pair<int, int>>& busStops){
  int passengers = 0;
  for(auto i: busStops)  passengers += i.first - i.second;
  return passengers;
}
_____________________________________
#include<vector>
using namespace std;


unsigned int number(const vector<pair<int, int>>& busStops) {
    unsigned int answer = 0;
    for (pair<int, int> b: busStops) {
        answer += b.first;
        answer -= b.second;
    }
    return answer;
}
_____________________________________
#include<vector>
#include <numeric>

unsigned int number(const std::vector<std::pair<int, int>>& busStops){
  return std::accumulate(busStops.begin(), busStops.end(), 0, [](unsigned int sum, auto i) { return sum + i.first - i.second; });
}
_____________________________________
#include <numeric>

unsigned int number(const std::vector<std::pair<int, int>>& busStops) {
    return std::accumulate(begin(busStops), end(busStops), 0u,
        [](auto a, auto b) { return a + b.first - b.second; });
}
