#include<vector>

bool isValidWalk(std::vector<char> walk) {
  if(walk.size() != 10) return false;
  int x=0, y=0;
  for(char c : walk){
    switch(c) {
      case 'n': y++; break;
      case 's': y--; break;
      case 'e': x++; break;
      case 'w': x--; break;
    }
  }
  if(x == 0 && y == 0) return true;
  else return false;
}
__________________________________________
#include<vector>
#include <algorithm> 

bool isValidWalk(std::vector<char> walk) {
  return walk.size() == 10 and 
         std::count(walk.begin(), walk.end(), 'e') == std::count(walk.begin(), walk.end(), 'w') and
         std::count(walk.begin(), walk.end(), 'n') == std::count(walk.begin(), walk.end(), 's');
}
__________________________________________
bool isValidWalk(const std::vector<char>& walk) {
    return walk.size() == 10 &&
        std::count(begin(walk), end(walk), 'n') == std::count(begin(walk), end(walk), 's') &&
        std::count(begin(walk), end(walk), 'w') == std::count(begin(walk), end(walk), 'e');
}
__________________________________________
#include<vector>

bool isValidWalk(std::vector<char> walk) {
  if(walk.size()!=10) 
  return false;
  int xPlane=0,yPlane=0;
  for(const auto &x:walk) {
    switch(x) {
      case 'n':xPlane++;break;
      case 's':xPlane--;break;
      case 'e':yPlane++;break;
      case 'w':yPlane--;break;
    }
  }
  return !xPlane && !yPlane;
  }
