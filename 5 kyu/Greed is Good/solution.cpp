#include <vector>

int score(const std::vector<int>& dice) {
  unsigned cs[7] = {};
  for (auto d : dice)
    cs[d]++;
  return
    cs[1] / 3 * 1000 + cs[6] / 3 * 600 + cs[5] / 3 * 500 +
    cs[4] / 3 * 400 + cs[3] / 3 * 300 + cs[2] / 3 * 200 +
    cs[1] % 3 * 100 + cs[5] % 3 * 50;
}
_____________________________________________
#include <vector>

int score(const std::vector<int>& dice) 
{
  int score = 0;
  int count[7] = { 0 };
  for (auto v : dice)
    if (++count[v] == 3)
    {
      score += (v == 1) ? 1000 : v * 100;
      count[v] = 0;
    }
  score += count[1] * 100;
  score += count[5] * 50;
  return score;
}
_____________________________________________
#include <vector>

using namespace std;

int score(const std::vector<int>& dice) {
    int one = 0, two = 0, three = 0, four = 0, five = 0, six = 0, total = 0;
    for (unsigned long i = 0; i < dice.size(); i++) {
        switch (dice[i]) {
            case 1: one++; break;
            case 2: two++; break;
            case 3: three++; break;
            case 4: four++; break;
            case 5: five++; break;
            case 6: six++; break;
        }
    }
    one >= 3 ? total += 1000, one -= 3, total += one * 100 : total += one * 100;
    five >= 3 ? total += 500, five -= 3, total += five * 50 : total += five * 50;
    if (two >= 3) total += 200;
    if (three >= 3) total += 300;
    if (four >= 3) total += 400;
    if (six >= 3) total += 600;

    return total;
}
_____________________________________________
#include <algorithm>
#include <iostream>
#include <vector>

const int sidesCount = 6;

struct DiceCounterGenerator {
  std::vector<int> dices;
  int index;
  
  DiceCounterGenerator(std::vector<int> dices) : dices(dices) { index = 0; }
  
  int operator()() { return std::count(dices.begin(), dices.end(), ++index); }
  
};

struct PointCounter {
  int total;
  int index;
  int* triple_points;
  int* single_points;
  
  PointCounter(int* triple_points, int* single_points) :
    triple_points(triple_points),
    single_points(single_points)
  {
    total = 0;
    index = 0;
  }
  
  void operator()(int n) {
    total += (n / 3) * triple_points[index];
    total += (n % 3) * single_points[index];
    
    ++index;
  }
};

int score(const std::vector<int>& dice) {

  std::vector<int> values(sidesCount);
  std::generate(values.begin(), values.end(), DiceCounterGenerator(dice));

  int triple_points[] = { 1000, 200, 300, 400, 500, 600 };
  int single_points[] =  { 100, 0, 0, 0, 50, 0 };

  auto points = std::for_each(values.begin(), values.end(), PointCounter(triple_points, single_points));
  
  return points.total;

}
_____________________________________________
#include <vector>
#include <unordered_map>

int score(const std::vector<int>& dice) 
{   
    std::unordered_map<int,int> counters;
    for(auto value : dice) {
        ++counters[value];
    }        
    int sum = 0;    
    for(auto cnt : counters)  {
        sum += cnt.second / 3 * cnt.first * 100 * (cnt.first == 1 ? 10 : 1);                               //1000 200 300 400 500 600 ?
        sum += (cnt.first == 1 ? cnt.second % 3 * 100 : 0) + (cnt.first == 5 ? cnt.second % 3 * 50 : 0);   // 100 500 ?           
    }        
    return sum;
}
