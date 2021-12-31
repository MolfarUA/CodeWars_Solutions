#include <algorithm>
#include <set>
#include <vector>

namespace DoubleLinear
{
   int dblLinear(const int n)
   {
     std::set<int> s { 1 };
     for (int i = 0; i < n; ++i) {
       auto x = *(s.begin());
       s.erase(s.begin());
       auto ins = s.insert(x + x + 1);
       s.insert(ins.first, x + x + x + 1);
     }
     return *(s.begin());
   }
}

__________________________________________________
#include <queue>
#include <functional>

class DoubleLinear
{
public:
    static int dblLinear(int n)
    {
        std::priority_queue<int, std::vector<int>, std::greater<int>> u;
        
        u.push(1);
        for (int i = 0; i < n; i++) {
            // Pop the smallest one
            int x = u.top();
            u.pop();
            
            // If there are repeated value following, just skip them!
            while (!u.empty() && u.top() == x)
                u.pop();
            
            // Push y to the priority queue
            int y = 2 * x + 1;
            u.push(y);
            
            // Push z to the priority queue
            int z = 3 * x + 1;
            u.push(z);
        }
        
        return u.top();
    }
};

__________________________________________________
#include <set>

class DoubleLinear
{
public:
    static int dblLinear(int n)
    {
      std::set<int>  seq;
      
      seq.insert(1);
      std::set<int>::iterator it = seq.begin();
      for (int i = 0; i < n; ++it, ++i)
      {
        int current = *it;
        seq.insert(2 * current + 1);
        seq.insert(3 * current + 1);
      }
      
      return *it;
    }
};

__________________________________________________
#include <set>

class DoubleLinear{
public:
    static int dblLinear(int n);
};

int DoubleLinear::dblLinear(int n){
    std::set<int> res({1});
    auto it = res.begin();
    while(n--){
        res.insert(*it*2 + 1);
        res.insert(*it*3 + 1);
        ++it;
    }
    return *it;
}
