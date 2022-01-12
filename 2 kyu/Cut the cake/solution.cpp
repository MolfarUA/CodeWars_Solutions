std::vector<std::string> cut(std::string cake)
{
  std::vector<std::string> result;
  int lineLength=0, lines=1, raisins=0;////find meta variables
  for(char c:cake){
    if(c=='\n')lines++;
    if(lines==1)lineLength++;
    if(c=='o')raisins++;
  }
  if(lines*lineLength%raisins!=0)return {};//no pieces with exactly same size possible
  int pieceSize=lines*lineLength/raisins;
  
  //iterate for all chars in given rectangle
  auto forRect=[&](int x,int y,int w,int h,std::function<void(char&)> callback,std::function<void()> lineEnd=[](){}){
    for(int yo=0;yo<h;yo++){
        for(int xo=0;xo<w;xo++){
          if(x+xo<0||x+xo>=lineLength||y+yo<0||y+yo>=lines){//out of Bounds give '\0' as error char
            char c='\0';
            callback(c);
          }else{
            callback(cake[(y+yo)*(lineLength+1)+(x+xo)]);
          }
        }
      lineEnd();
    }
  };
  
  //search recrusive Brute-Force and add result after found a solution
  std::function<bool(int,int)> search=[&](int x, int y){
    for(int w=pieceSize;w>0;w--){//try all piece widths
      if(pieceSize%w!=0)continue; //not allowed piece size
      int h=pieceSize/w;
      
      //check if piece is available
      int pc=0;
      forRect(x,y,w,h,[&](char& c){
          if(c=='o')pc++;//allowed piece if only one raisins
          else if(c!='.')pc=2;//disabled char or out of Bounds
      });
      if(pc!=1)continue; //not exactly one raisins,  disabled chars or out of Bounds
    
      forRect(x,y,w,h,[](char& c){c++;});//disable current piece for  recursive search 
      
      //go to next enabled char or end
      int next;
      for(next=0;next<cake.size()&&cake[next]!='.'&&cake[next]!='o';next++);//find next possible piece position
      
      //recursive search. ends if the complete cake is disabled
      if(next==cake.size()||search(next%(lineLength+1),next/(lineLength+1))){//complete cake is disabled or try recursive search 
        //found a solution, add  piece to result and return true
        std::string thisPiece="";
        forRect(x,y,w,h,
          [&](char& c){thisPiece.push_back(c-1);},
          [&](){thisPiece.push_back('\n');});
        thisPiece.pop_back();
        result.push_back(thisPiece);
        return true;
      }
      
      forRect(x,y,w,h,[](char& c){c--;});//reenable current piece for next trys
    }
    return false;//no solution found return false
  };

  if(search(0,0)){//start Brute-Force and return result if a solution is founded
    std::reverse(result.begin(), result.end());
    return result;
  }else{
    return {};//no solution found
  }
}

_____________________________________________________
std::vector<std::string> cut(std::string cake)
{
  int lineLength=0, lines=1, pieces=0;
  for(char c:cake){
    if(c=='\n')lines++;
    if(lines==1)lineLength++;
    if(c=='o')pieces++;
  }
  if(lines*lineLength%pieces!=0)return {};//no pieces cut possible
  int pieceSize=lines*lineLength/pieces;
  // iterate for all chars in given rectangle
  auto forRect=[&](int x,int y,int w,int h,std::function<void(char&)> callback,std::function<void()> lineEnd=[](){}){
    for(int yo=0;yo<h;yo++){
        for(int xo=0;xo<w;xo++){
          if(x+xo<0||x+xo>=lineLength||y+yo<0||y+yo>=lines){//out of Bounds give '-' as error char
            char c='-';
            callback(c);
          }else{
            callback(cake[(y+yo)*(lineLength+1)+(x+xo)]);
          }
        }
      lineEnd();
    }
  };
  //
  std::vector<std::string> result;
  std::function<bool(int,int)> search=[&](int x, int y){//search
    for(int w=pieceSize;w>0;w--){
      if(pieceSize%w==0){//try each possible piece at x,y
        int h=pieceSize/w;
        int pc=0;
        forRect(x,y,w,h,[&](char& c){
            if(c=='o')pc++;//allow piece if only one raisins
            else if(c!='.')pc+=2;//no allow piece
        });
        if(pc==1){// piece is possible  
          forRect(x,y,w,h,[](char& c){c++;});//disable current piece for recursive search
          
          int next;//go to next unuse char or end
          for(next=y*(lineLength+1)+x;next<cake.size()&&cake[next]!='.'&&cake[next]!='o';next++);
          
          //all pieces found or recursive search 
          if(next==cake.size()||search(next%(lineLength+1),next/(lineLength+1))){
            std::string thisPiece="";//found solution, add to result and return true
            forRect(x,y,w,h,
                    [&](char& c){thisPiece.push_back(c-1);},
                    [&](){thisPiece.push_back('\n');});
            thisPiece.pop_back();
            result.push_back(thisPiece);
            return true;
          }else{//try next
            forRect(x,y,w,h,[](char& c){c--;});//enable current piece for next trys
          }
        }
      }
    }
    return false;//no solution found return false
  };

  if(search(0,0)){//start and return result if a solution is founded
    std::reverse(result.begin(), result.end());
    return result;
  }else{
    return {};//no result found
  }
}

____________________________________________________
#include <vector>
#include <string>
#include <algorithm>

unsigned int s;
unsigned int St;
unsigned int cnt_row;
unsigned int cnt_col;
unsigned int all_cnt_raisin = 0;

struct Rect {
  int x1, y1, x2, y2;
  Rect(int _x1, int _y1, int _x2, int _y2) {
    x1 = _x1;
    x2 = _x2;
    y1 = _y1;
    y2 = _y2;
  }
};

bool in_range(int i, int j) {
  return i >= 0 && i < cnt_row && j >= 0 && j < cnt_col;
}

bool empty_mask(const std::vector<char>& mask, size_t sii, size_t sjj, size_t eii, size_t ejj) {
  for (size_t ii = sii; ii <= eii; ++ii) {
    size_t idx = cnt_col * ii;
    for (size_t jj = sjj; jj <= ejj; ++jj) {
      if (mask[idx + jj] == '1') return false;
    }
  }
  return true;
}

std::vector<Rect> generate(
  const std::vector<char>& cake,
  const std::vector<unsigned int>& div, 
  std::vector<char> mask,
  unsigned int raisin) 
{
  if (raisin == 0) return {};
  size_t sii = 0;
  size_t sjj = 0;
  for (size_t ii = 0; ii < cnt_row; ++ii) {
    bool br = false;
    size_t idx = cnt_col * ii;
    for (size_t jj = 0; jj < cnt_col; ++jj) {
      if (mask[idx + jj] == '0') {
        sii = ii;
        sjj = jj;
        br = true;
        break;
      }
    }
    if (br) break;
  }
  std::vector<Rect> gen;
  for (const auto& x : div) {
    auto i = x - 1;
    auto j = St / x - 1;
    if (in_range(i + sii, j + sjj) && empty_mask(mask, sii, sjj, i + sii, j + sjj)) {
      i += sii;
      j += sjj;
      size_t cnt_raisin = 0;
      for (size_t ii = sii; ii <= i; ++ii) {
        size_t idx = cnt_col * ii;
        for (size_t jj = sjj; jj <= j; ++jj) {
          if (cake[idx + jj] == 'o') {
            ++cnt_raisin;
          }
          mask[idx + jj] = '1';
        }
      }
      if (cnt_raisin == 1) {
        gen.push_back(Rect(sjj, sii, j, i));
        auto v = generate(cake, div, mask, raisin - 1);
        if (v.size() == raisin - 1) {
          gen.insert(gen.end(), v.begin(), v.end());
          return gen;
        }
        else gen.clear();
      }
      for (size_t ii = sii; ii <= i; ++ii) {
        size_t idx = cnt_col * ii;
        for (size_t jj = sjj; jj <= j; ++jj) {
          mask[idx + jj] = '0';
        }
      }
    }
  }
  return {};
}

std::vector<std::string> cut(const std::string& cake) {
  if (cake.back() == '\n') cnt_row = 0;
  else cnt_row = 1;
  all_cnt_raisin = 0;
  for (auto& x : cake) {
    if (x == 'o') ++all_cnt_raisin;
    else if (x == '\n') ++cnt_row;
  }
  s = cake.size() - cnt_row + 1;
  St = s / all_cnt_raisin;
  cnt_col = s / cnt_row;
  std::vector<char> my_cake;
  for (auto& x : cake) {
    if (x != '\n') my_cake.push_back(x);
  }

  std::vector<unsigned int> div;
  for (size_t d = St; d >= 1; --d) {
    if (St % d == 0) {
      div.push_back(St / d);
    }
  }
  auto r = generate(my_cake, div, std::vector<char>(s, '0'), all_cnt_raisin);
  std::vector<std::string> res;
  for (const auto& x : r) {
    std::string s;
    for (size_t i = x.y1; i <= x.y2; ++i) {
      size_t idx = cnt_col * i;
      for (size_t j = x.x1; j <= x.x2; ++j) {
        s.push_back(my_cake[idx + j]);
      }
      s.push_back('\n');
    }
    s.erase(std::remove(s.end() - 1, s.end(), '\n'), s.end());
    res.push_back(s);
    s.clear();
  }

  return res;
}

_____________________________________________________
 /*
NOTE : You are provided with these functions
std::string join(const std::string &sep, const std::vector<std::string> &to_join)
std::vector<std::string> split(const std::string &to_split, char separator = '\n')
*/

#include <numeric>
#include <algorithm>
typedef std::pair<int,int> Point;
Point operator+(const Point& l,const Point& r){
  return std::make_pair(l.first+r.first-1,l.second+r.second-1);
}
std::ostream& operator<<(std::ostream& os,Point p){return os << "("<<p.first<<","<< p.second<<")";}

/**
The function convert string representation of the cake into it's dimensions and positions of rosins
return pair representing x and y coordinates of rosins, where last pair is width and height of the cake.
*/
std::vector<Point> measure_the_cake(const std::string &cake){
  std::vector<Point> rosins;
  int idx=0,idy=0,width = 0,height =0;
  for(auto c:cake)
    switch(c){
      case '.' : idx++; break;
      case '\n': width = idx;idx=0;idy++; break;
      case 'o' : rosins.push_back(std::make_pair(idx++,idy)); break;
      default: 
        throw std::invalid_argument(std::string("cake can not contain such ingridient:'") + std::string(1,c) + std::string("'"));
    }
  height = idy+1;
  rosins.push_back(std::make_pair(width,height));
  return rosins;
}

/**
  reurn all possible dimensions of boxes with determined area limited by maximal width and height
*/
std::vector<Point> variants(const int box_area, const int max_width, const int  max_height){
  
  std::vector<Point> ret;
  for(int i=1; i<= box_area  && i<=max_height;i++)
    if(box_area%i==0 && box_area/i <=max_width) ret.push_back(std::make_pair(box_area/i,i));
  return ret;
  
}
constexpr bool is_inside(const Point& a, const Point& b, const Point& point){
  
  return point.first >= a.first && point.first <= b.first && point.second >= a.second && point.second <= b.second;
  
}

struct Pice{
  
  Point upper_left;
  Point lower_right;
  std::vector<Point> rosins;
  Pice():upper_left({0,0}),lower_right({0,0}),rosins({}){}
  Pice(const Point& a,const Point& b,std::vector<Point> nrosins):upper_left(a),lower_right(b),rosins(nrosins){
    rosins.erase(std::remove_if(rosins.begin(),rosins.end(),[a,b](Point p){return !is_inside(a,b,p);}),rosins.end());
  }
  
  Point getWH() const {
      int width = lower_right.first - upper_left.first+1;
      int height = lower_right.second - upper_left.second+1;
      return std::make_pair(width,height);
  }
  bool can_be_cutted() const{
    auto [width,height] = getWH();
    bool cbc = true; 
    cbc =  cbc 
      && (rosins.size()>0) //if no rosins pice is not good
      && (width*height % rosins.size()==0); // if rosins is not divisible for everyone
    return cbc;
  }
  int pice_size() const{
      if(!can_be_cutted()) return 0;
      int width = lower_right.first - upper_left.first+1;
      int height = lower_right.second - upper_left.second+1;
      return width*height / rosins.size();
  }
  bool intersect_with(const Pice& pc){
    return !(upper_left.second    > pc.lower_right.second || 
             upper_left.first     > pc.lower_right.first  ||
                pc.upper_left.second > lower_right.second || 
                pc.upper_left.first  > lower_right.first);
    
  }
  bool intersect_with(const std::vector<Pice>& pcs){
    for(auto p: pcs)
      if(intersect_with(p))
        return true;
    return false;
  }
  std::pair<Point,Point> corners(){
    return std::make_pair(std::make_pair(upper_left.first,lower_right.second+1),std::make_pair(lower_right.first+1 , upper_left.second));
  }
  std::string serialize() const{
    
    auto [width,height] = getWH();
    std::string line(width,'.');
    std::vector lines(height,line);
    
    for(auto r: rosins) lines[r.second-upper_left.second][r.first-upper_left.first]='o';

    return join("\n",lines);
  }
  
  friend std::ostream& operator<<(std::ostream& os, const Pice& cake){
    os << " ul:" << cake.upper_left;
    os << " lr:" << cake.lower_right;
    os << " S :" << (cake.lower_right.first - cake.upper_left.first+1)*(cake.lower_right.second - cake.upper_left.second+1);
    os << " ro:" << cake.rosins.size();
    return os;    
  }
};

struct Cake{
  int cover;
  const Point ul;
  const Point lr;
  const std::vector<Point> rosins;
  std::vector<Point>corners;
  int pice_size;
  
  const std::vector<Point> boxes;
  
  std::vector<Pice> pices;
  std::vector<std::pair<Point,std::vector<std::pair<int,int>>::const_iterator>> sequence;
  
  inline int width() const {return lr.first - ul.first + 1;} 
  inline int height() const {return lr.second - ul.second + 1;} 
  inline int area() const {return width()*height();}
  
  Cake(const Point& u,const Point& l, const std::vector<Point>& r):
    cover(0),ul(u),lr(l),rosins(r),corners({ul}),
    pice_size(rosins.size()?width() * height() / rosins.size():0),
    boxes(variants(pice_size,width(),height())){}
 
  void clean_corners(){
    corners.resize(0);
    for(auto p: pices)
    {
       auto [ur,ll]  = p.corners();
       Pice pur(ur,ur,{});
       Pice pll(ll,ll,{});
       if(ur.second<height() && !pur.intersect_with(pices))
          corners.push_back(ur);
       if(ll.first<width() && !pll.intersect_with(pices))
        corners.push_back(ll);
    }
  }
  
 bool iterate_box(const Point& cor, std::vector<Point>::const_iterator& it){
   while(it!=boxes.end()){
    if(it->first+cor.first>width() || it->second+cor.second>height()){it ++; continue;}
    Pice p(cor,*it+cor,rosins);
    if(!p.intersect_with(pices)&&p.pice_size()==pice_size){
      sequence.push_back(std::make_pair(cor,it+1));
      pices.push_back(p);
      cover += pice_size;
      clean_corners();
      return true;
    }
    it++;
   }
   return step_back();
 }
  bool step_back(){
    std::cout << "SB" << std::endl;
    if(sequence.size()==0)
      return false;
    
    pices.pop_back();
    cover -= pice_size;
    auto [cor,it] = sequence.back(); sequence.pop_back();
    return iterate_box(cor,it);
  }
 bool next(){
   if(cover==area())
    return false;
   
   if(corners.size()==0)
    return step_back();
   
   std::sort(corners.begin(),corners.end(),[](auto a,auto b){return a.second==b.second?a.first>b.first:a.second>b.second;});
  
   Point cor = corners.back();corners.pop_back();
   
   std::vector<Point>::const_iterator it = boxes.begin();
   
   return iterate_box(cor,it);
   
 }
  std::vector<std::string> serialize() const{
    std::vector<std::string> ret;
    for(auto p: pices)
      ret.push_back(p.serialize());
    return ret; 
  }
};


std::vector<std::string> cut(const std::string &cake){
  std::cout << std::endl << "****Start****" << std::endl << cake << std::endl;
  
  std::vector<Point> rosins = measure_the_cake(cake);
  auto [width,height] = rosins.back(); rosins.pop_back();
  if(rosins.size()<2) return {cake};
  
  Cake c(Point({0,0}),Point({width-1,height-1}),rosins);
  while(c.next());
  
  return c.serialize();
}
