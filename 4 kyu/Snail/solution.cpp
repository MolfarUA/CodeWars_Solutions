#include <cstddef>
#include <vector>

std::vector<int> snail(const std::vector<std::vector<int>>& xs) {
  std::vector<int> res;
  if (xs[0].empty())
    return res;
  const std::size_t ny = xs.size(), nx = xs[0].size();
  res.reserve(ny * nx);
  std::ptrdiff_t x0 = 0, y0 = 0, x1 = nx - 1, y1 = ny - 1, x = 0, y = 0;
  while (y0 <= y1) {
    while (x < x1) res.push_back(xs[y][x++]); y0++;
    while (y < y1) res.push_back(xs[y++][x]); x1--;
    while (x > x0) res.push_back(xs[y][x--]); y1--;
    while (y > y0) res.push_back(xs[y--][x]); x0++;
  }
  res.push_back(xs[y][x]);
  return res;
}

#################
#include <vector>
using namespace std;
inline vector<int> snail(vector<vector<int>> array) {
  int leftlimit=0, uplimit=0, rightlimit=array[0].size()-1, downlimit=rightlimit, cx=-1, cy=-1;
  vector <int> ans;
  while (leftlimit<=rightlimit){
    for (cy++, uplimit++,    cx++; cx <= rightlimit; cx++) ans.push_back(array[cy][cx]); 
    for (cx--, rightlimit--, cy++; cy <= downlimit ; cy++) ans.push_back(array[cy][cx]);
    for (cy--, downlimit--,  cx--; cx >= leftlimit ; cx--) ans.push_back(array[cy][cx]);
    for (cx++, leftlimit++,  cy--; cy >= uplimit   ; cy--) ans.push_back(array[cy][cx]);
  } 
  return ans;
}

######################
#include <vector>

std::vector<int> snail(const std::vector<std::vector<int>> &snail_map)
{
    size_t n = snail_map[0].size();
    std::vector<int> snail_vec(n*n);
  
    int i = 0, j = 0, k = 0, margin = 0;
    while(k < n*n)
    {
        //right:
        for ( ; j < n - margin; j++, k++)
            snail_vec[k] = snail_map[i][j];
      
        //down:
        for (i++, j-- ; i <= j; i++, k++)
            snail_vec[k] = snail_map[i][j];
     
        //left:
        for (i--, j-- ; j >= margin; j--, k++)
            snail_vec[k] = snail_map[i][j];

        //top:
        for (i--, j++ ; i > j; i--, k++)
            snail_vec[k] = snail_map[i][j];

        i++; j++; margin++;
    }

    return snail_vec; //return {}
}

##############
#include <vector>
using namespace std;

vector<int> snail(const vector<vector<int>> &snail_map) {
    if(snail_map[0].size() == 0){
      return {};
    } else {
      int top = 0, right = snail_map[0].size(), left = -1, bottom = snail_map.size();
      bool t = false, r = true, l = false, b = false;
      int size = snail_map[0].size() * snail_map.size();
      vector<int> answer;
      answer.push_back(snail_map[0][0]);
      int c = 0, j = 1;
      for(int i = 1; i < size; i++){
          answer.push_back(snail_map[c][j]);
          if(r){
              if(j + 1 != right){
                  j++;
              } else{
                  b = true;
                  r = false;
                  right = j;
                  c++;
              }
          } else if(b){
              if(c + 1 != bottom){
                  c++;
              } else{
                  l = true;
                  b = false;
                  bottom = c;
                  j--;
              }
          } else if(l){
              if(j - 1 != left){
                  j--;
              } else{
                  t = true;
                  l = false;
                  left = j;
                  c--;
              }
          } else if(t){
              if(c - 1 != top){
                  c--;
              } else{
                  r = true;
                  t = false;
                  top = c;
                  j++;
              }    
          }
      }
      return answer;
    }
}

#######################
#include <vector>

std::vector<int> snail(const std::vector<std::vector<int>> &snail_map) {
  std::vector<int> ans;
  int n = snail_map.size();
  if (n == 0 || snail_map[0].size() == 0) return ans;
  for (int i = 0; i < n/2; ++i) {
    int end = n - 1 - i;
    for (int j = i; j < end; ++j) ans.push_back(snail_map[i][j]);
    for (int j = i; j < end; ++j) ans.push_back(snail_map[j][end]);
    for (int j = end; j > i; --j) ans.push_back(snail_map[end][j]);
    for (int j = end; j > i; --j) ans.push_back(snail_map[j][i]);
  }
  
  if (n % 2 == 1) {
    ans.push_back(snail_map[n/2][n/2]);
  }
  
  return ans;
}
