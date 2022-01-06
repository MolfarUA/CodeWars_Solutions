#include <vector>
using namespace std;

int sum(vector<int> numbers)
{
    if (numbers.size() < 2) return 0;
    int sum = 0;
    int low = numbers[0], high = numbers[0];
    for (int n : numbers) {
      if (n < low) low = n;
      else if (n > high) high = n;
      sum += n;
    }
    return sum - high - low;
}
________________________________________
#include<vector>
#include<numeric>
#include<algorithm>
using namespace std;

int sum(vector<int> numbers)
{
    if (numbers.size()<=1)
        return 0;
    return accumulate(numbers.begin(),numbers.end(),0)-*max_element(numbers.begin(),numbers.end())-*min_element(numbers.begin(),numbers.end());
}
________________________________________
#include<vector>
#include <algorithm>

using namespace std;

int sum(vector<int> numbers)
{
    std::sort(numbers.begin(), numbers.end());
    int sum=0;
    
    for (int i=1; i<numbers.size()-1; i++)
      sum+=numbers[i];
    
    return sum;
}
