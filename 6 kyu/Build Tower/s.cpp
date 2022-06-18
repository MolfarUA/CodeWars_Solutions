576757b1df89ecf5bd00073b


#include <string>
#include <vector>

using namespace std;

vector<string> towerBuilder(unsigned nFloors) {
  vector <string> vect;
  for(unsigned i = 0, k = 1; i < nFloors; i++, k+=2)
    vect.push_back(string(nFloors-i-1, ' ') + string(k, '*') + string(nFloors-i-1, ' '));
  return {vect};
}
_____________________________
#include <string>
#include <vector>

std::vector<std::string> towerBuilder(unsigned nFloors) {
  std::vector<std::string> tower;
  for(unsigned i = 1; i <= nFloors; i++){
     std::string floor = std::string(nFloors - i, ' ') + std::string(i*2 - 1, '*') + std::string(nFloors - i, ' ');
     tower.push_back(floor);
   }
   return tower;    
};
_____________________________
#include <string>
#include <vector>

std::vector<std::string> towerBuilder(unsigned nFloors) {
  std::string floor="";
  std::vector<std::string> res(nFloors);
  for(int i=1;i<=nFloors;++i)
  {
    floor+=std::string(nFloors-i,' ');
    floor+=std::string(1+(i-1)*2,'*');
    floor+=std::string(nFloors-i,' ');
    res[i-1]=floor;
    floor="";
  }
  return res;
}
_____________________________
#include <string>
#include <vector>
using namespace std;

std::vector<std::string> towerBuilder(unsigned nFloors) {
  vector<string> res;
  if (nFloors==0) return res;
  if (nFloors==1) return {"*"};
  
  //if nFloors>1
  string left,mid{"*"},right;
  
  unsigned len=nFloors-1;
  left.resize (len,' ');
  right.resize(len,' ');
  
  res.push_back(left+mid+right); //Init Floor=1
  for (unsigned i=0;i<len;++i){
    left[len-1-i]='*';
    right[i]='*';
    res.push_back(left+mid+right);
  }
  return res;
}
_____________________________
#include <string>
#include <vector>

std::vector<std::string> towerBuilder(unsigned nFloors) {
  std::vector<std::string> result;
  int w = nFloors*2 - 1;
  std::string floor(w, ' ');
  for (unsigned i = 0; i < nFloors; ++i) {
    int c = w/2;
    floor[c-i] = floor[c+i] = '*';
    result.push_back(floor);
  }
  return result;
}
_____________________________
class Kata
{
public:
    std::vector<std::string> towerBuilder(int nFloors)
    {
      const int rCol = 2 * nFloors - 1;
      std::vector<std::string> field(nFloors, std::string(rCol, ' '));
      for (int i = 0; i < nFloors; i++) {
        for (int j = rCol / 2 - i; j <= rCol / 2 + i; j++) {
          field[i][j] = '*';
        }
      }
      return field;
    }
};
