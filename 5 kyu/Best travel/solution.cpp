using namespace std;

class BestTravel
{
public:
    static int chooseBestSum(int t, int k, const vector<int>& ls);
};

int BestTravel::chooseBestSum(int t, int k, const vector<int>& ls) {
    //cout << t << ' ' << k << endl;
    int n = ls.size();
    if (n < k) return -1;
    int ret{0};
    string bitmask(k, 1);
    bitmask.resize(n, 0);
    do {
      //for (int b:bitmask) cout << b << ' ';
      //cout << endl;
      int sum{0};
      for (int i = 0; i < n; ++i)
        if (bitmask[i]) sum += ls[i];
      if (sum <= t && sum > ret) ret = sum; 
    } while (prev_permutation(bitmask.begin(), bitmask.end()));
    if (ret > 0) return ret;
    return -1;
}
_______________________________________
/*  
 *  Stop giving me classes with only
 *  one static method! Geez....
 */
namespace BestTravel
{

void getBestValue(std::vector<int> &dist, int max, int depth,
        int curValue, int lastIdx, int &sum)
{
    // start in the begining
    int i = 0;
    // generic name, waiting for the code review
    int value;

    // let's go!
    for (std::vector<int>::iterator it = dist.begin();
            it < dist.end(); it++, i++)
    {
        // there is no looking back now
        if (i <= lastIdx)
            continue;

        // best result achieved, get out of here!
        if (sum == max && sum != -1)
            break;

        // maybe I should store this
        value = curValue + (*it);

        // nah, too big
        if (value > max)
            continue;

        // should I go deeper?
        if (depth > 1)
            getBestValue(dist, max, depth - 1, value, i, sum);

        // I hope this is the one!
        if (depth == 1 && value > sum)
            sum = value;
    }
}

int chooseBestSum(int t, int k, std::vector<int>& ls)
{
    // final result
    int sum = -1;
    // start BIG!
    std::sort(ls.rbegin(), ls.rend());

    // did i say recursion?
    getBestValue(ls, t, k, 0, -1, sum);

    //gg
    return sum;
}

};
_______________________________________
class BestTravel
{
public:
  static int chooseBestSum(int t, int k, std::vector<int>& ls);
};

int BestTravel::chooseBestSum(int t, int k, std::vector<int>& ls) {
  // We need to find subsets of ls with k elements.
  // We do this by counting and applying the Bijection Rule 
  // to map equivalent bitsets(integers) to ls and get our subsets.
  
  if((ls.size() >= sizeof(unsigned int) * 8) || (k > ls.size())) {
    return -1;
  }
  
  int best = -1;
  
  // Bijection to bitset(usize integer) with n elements.
  // Iterate all possible subsets, with all sizes, 1..n.
  for(unsigned int i = 1; i < 1u << ls.size(); i++) {
    // We are only interested in subsets with k-elements.
    if(__builtin_popcount(i) == k) {
      int sum = 0;
      
      // Map bits to elemets in ls.
      for(int j = 0; j < ls.size(); j++) {
        if((i >> j) & 0x1) {
          sum += ls[j];
        }
      }
      
      // Ignore subsets larger then t
      if(sum <= t && sum > best) {
        best = sum;
      }
    }
  }
  
  return best;
}
_______________________________________
#include <vector>
#include <algorithm>

class BestTravel
{
public:
    static int chooseBestSum(int t, int k, std::vector<int>& ls);
};

int BestTravel::chooseBestSum(int t, int k, std::vector<int>& ls)
{
    unsigned int n = ls.size();
    if ((unsigned int)k > n) return -1;
    int mx = -1, sm;
    std::string bitmask(k, 1);
    bitmask.resize(n, 0);
    do {
        sm = 0;
        for (unsigned int i = 0; i < n; ++i)
            if (bitmask[i]) sm += ls[i];
        if ((sm >= mx) && (sm <= t)) mx = sm;
    } while (std::prev_permutation(bitmask.begin(), bitmask.end()));
    return mx;
}

_______________________________________
#include <vector>
#include <algorithm>

class BestTravel
{
public:
    static int chooseBestSum(int t, int k, std::vector<int>& ls);
};

int BestTravel::chooseBestSum(int t, int k, std::vector<int>& ls)
{
    unsigned int n = ls.size();
    if ((unsigned int)k > n) return -1;
    int mx = -1, sm;
    std::string bitmask(k, 1);
    bitmask.resize(n, 0);
    do {
        sm = 0;
        for (unsigned int i = 0; i < n; ++i)
            if (bitmask[i]) sm += ls[i];
        if ((sm >= mx) && (sm <= t)) mx = sm;
    } while (std::prev_permutation(bitmask.begin(), bitmask.end()));
    return mx;
}
_______________________________________
#include <algorithm>
#include <vector>
#include <limits.h>

class BestTravel
{
public:
    static int chooseBestSum(int t, int k, std::vector<int> &ls)
    {
        int result = combinations(t, k, ls, 0);
        return result > 0 ? result : -1;
    }

    static int combinations(int t, int k, std::vector<int> &ls, size_t i)
    {
        if (k == 0 && t >= 0)
        {
            return 0;
        }
        else if (k < 0 || i >= ls.size())
        {
            return INT_MIN;
        }
        else
        {
            return std::max(combinations(t, k, ls, i + 1), ls[i] + combinations(t - ls[i], k - 1, ls, i + 1));
        }
    }
};
_______________________________________
#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>

using namespace std;

class BestTravel
{
public:
    static int chooseBestSum(int limit, int k, std::vector<int> &ls)
    {
        if (k > (int)ls.size())
            return -1;
        int dSum = -1 ;
        size_t N = ls.size();  
        vector<bool> sig (k,true); 
        sig.resize (N, false); 
        do
        {
            int sum = 0; 
            for (size_t i = 0; i < N; i++)
            {
                if (sig[i]){
                    sum += ls[i];
                    if (sum > limit) break ; 
                }
            }
            if (sum > dSum && sum <=limit) dSum = sum;  

        } while (std::prev_permutation(sig.begin(), sig.end()));

        return dSum;
    }
};
