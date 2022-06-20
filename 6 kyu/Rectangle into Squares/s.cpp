55466989aeecab5aac00003e
  

using namespace std;

class SqInRect
{
  public:
  static vector<int> sqInRect(int lng, int wdth);
};

vector<int> SqInRect::sqInRect(int l, int w) {
    vector<int> ret;
    if (w == l) return ret;
    if (w > l) swap(l, w);
    while (w > 0) {
      ret.push_back(w);
      int t = w;
      w = l - w;
      l = t;
      if (w > l) swap(l, w);
    }
    return ret;
}
______________________________
#include <vector>

class SqInRect
{
  public:
  static std::vector<int> sqInRect(int lng, int wdth);
};

std::vector<int> SqInRect::sqInRect(int lng, int wdth)
{
  if (lng == wdth) return {};
  std::vector<int> arr;
  while (lng > 0 && wdth > 0)
  {
  if (lng > wdth)
  {
    arr.push_back(wdth);
    lng -= wdth;
  }
  else
  {
    arr.push_back(lng);
    wdth -= lng;
  }
  }
  return arr;
}
______________________________
class SqInRect
{
public:
  static std::vector<int> sqInRect(int lng, int wdth)
  {
    if (lng == wdth) return {};
    int sqValue = std::min(lng, wdth);
    std::vector<int> values = sqInRect(sqValue, std::max(lng, wdth) - sqValue);
    values.insert(values.begin(), sqValue);
    if (values.size() == 1) values.push_back(sqValue);
    return values;
  }
};
