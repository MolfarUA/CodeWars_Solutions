59b47ff18bcb77a4d1000076


#include <sstream>
#include <cmath>
#include <cctype>
#include <regex>
#include <cmath>
#include <tuple>
#include <map>
#include <stack>
#include <iostream>

using namespace std;

template <typename T>
struct coord
{
    using value_type = T;
    value_type row, col;

    constexpr coord() : row(value_type()), col(value_type()) {}
    constexpr coord(const value_type& _row, const value_type& _col) : row(_row), col(_col) {}
    constexpr coord(initializer_list<value_type> li) : row(*li.begin()), col(*(li.begin() + 1)) {}

    bool operator==(const coord& val) const { return row == val.row && col == val.col; }
    coord operator+(const coord& val) const { return { row + val.row, col + val.col }; }
    coord operator-(const coord& val) const { return { row - val.row, col - val.col }; }
    coord& operator+=(const coord& val) { return *this = operator+(val); }
    coord& operator-=(const coord& val) { return *this = operator-(val); }
};

class Train;
class TrackIterator;
class Track
{
public:
    using iterator = TrackIterator;
    using position = coord<ptrdiff_t>;
    using line = string;
    using value_type = typename line::value_type;
private:
    static const value_type blank = ' ';
public:
    static const value_type station = 'S';
    static const position left;
    static const position right;
    static const position top;
    static const position bottom;
public:
    Track(const string& str) {
        istringstream is(str);
        string s;
        while (getline(is, s)) { track.push_back(s); }
        left_top = { 0, static_cast<ptrdiff_t>(track.front().find_first_not_of(' ')) };
    }
    iterator begin();
    iterator rbegin();
    position next_position(const position& cur, const position& pre) const;
    value_type& at(position& pos) { return const_cast<value_type&>(at(const_cast<const position&>(pos))); }
    const value_type& at(const position& pos) const { return track.at(pos.row).at(pos.col); }
    void print(int step, const Train& ta, const Train& tb, const Track::iterator& pa, const Track::iterator& pb) const;
    bool valid_position(const position& pos) const {
        if (pos.row < 0 || pos.row >= track.size()) { return false; }
        if (pos.col < 0 || pos.col >= track.at(pos.row).size()) { return false; }
        return true;
    }
private:
    bool check_hori(const position& pos) const { return valid_position(pos) && (at(pos) == '-' || at(pos) == '+' || at(pos) == station); }
    bool check_vert(const position& pos) const { return valid_position(pos) && (at(pos) == '|' || at(pos) == '+' || at(pos) == station); }
    bool check_slas(const position& pos) const { return valid_position(pos) && (at(pos) == '/' || at(pos) == 'X' || at(pos) == station); }
    bool check_bksl(const position& pos) const { return valid_position(pos) && (at(pos) == '\\' || at(pos) == 'X' || at(pos) == station); }
private:
    vector<string> track;
    position left_top;
};
const Track::position Track::left{ 0, -1 };
const Track::position Track::right{ 0, 1 };
const Track::position Track::top{ -1, 0 };
const Track::position Track::bottom{ 1, 0 };

class TrackIterator
{
    using difference_type = ptrdiff_t;
public:
    TrackIterator(Track& _track, const Track::position& _cur, const Track::position& _next, const Track::position& _pre)
        : track(_track), cur(_cur), next(_next), pre(_pre) {}
    TrackIterator operator+(difference_type diff) const {
        TrackIterator tmp = *this;
        for (; diff != 0; --diff) { ++tmp; }
        return tmp;
    }
    TrackIterator operator-(difference_type diff) const {
        TrackIterator tmp = *this;
        for (; diff != 0; --diff) { --tmp; }
        return tmp;
    }
    TrackIterator& operator++() {
        auto&& tmp = track.next_position(next, cur);
        pre = cur; cur = next; next = tmp;
        return *this;
    }
    TrackIterator& operator--() {
        auto&& tmp = track.next_position(pre, cur);
        next = cur; cur = pre; pre = tmp;
        return *this;
    }
    bool operator==(const TrackIterator& val) const {
        return cur == val.cur && next == val.next && pre == val.pre;
    }
    bool operator!=(const TrackIterator& val) const { return !operator==(val); }
    Track::value_type& operator*() { return track.at(cur); }
    Track::position value() const { return cur; }
    void reverse() {
        auto tmp = next;
        next = pre;
        pre = tmp; }
private:
    Track& track;
    Track::position cur, next, pre;

    friend void Track::print(int step, const Train& ta, const Train& tb, const Track::iterator& pa, const Track::iterator& pb) const;
};

class Train
{
public:
    static const char express_name = 'x';
public:
    string name;
    size_t length;
    bool express;
    bool clockwise;
public:
    Train(const string& str)
        : name(str), length(str.size()), express(tolower(str.front()) == express_name), pause_time(0), clockwise(str.back() >= 'A' && str.back() <= 'Z') {}
    void run_cycle(Track::iterator& pos) {
        if (express) { ++pos; return; }
        if (pause_time != 0) {
            --pause_time;
            if (pause_time == 0) { ++pos; }
            return;
        }
        if (*pos == Track::station) { pause_time = length - 1; return; }
        ++pos;
    }
private:
    int pause_time;

    friend int train_crash(const string& track_str, const string& a_train_str, int a_train_pos, const string& b_train_str, int b_train_pos, int limit);
};

inline Track::iterator Track::begin()
{
    position&& r0 = left_top + right;
    position&& r1 = left_top + bottom;
    if (!check_vert(r1)) { r1 += left; }
    return iterator(*this, left_top, r0, r1);
}

inline Track::iterator Track::rbegin()
{
    position&& r0 = left_top + right;
    position&& r1 = left_top + bottom;
    if (at(r1) == blank) { r1 += left; }
    return iterator(*this, left_top, r1, r0);
}

Track::position Track::next_position(const position& cur, const position& pre) const {
    const auto& land = at(cur);
    const auto&& dir = cur - pre;

    if (land == '|' || land == '-' || land == '+' || land == 'X' || land == 'S') { return cur + dir; }
    if (land == '/') {
        if (check_hori(cur + left) && (dir == bottom || dir == bottom + left)) { return cur + left; }
        if (check_hori(cur + right) && (dir == top || dir == top + right)) { return cur + right; }
        if (check_vert(cur + top) && (dir == right || dir == top + right)) { return cur + top; }
        if (check_vert(cur + bottom) && (dir == left || dir == bottom + left)) { return cur + bottom; }
        if (check_slas(cur + top + right) && (dir == right || dir == top || dir == top + right)) { return cur + top + right; }
        if (check_slas(cur + bottom + left) && (dir == left || dir == bottom || dir == bottom + left)) { return cur + bottom + left; }
    }
    else if (land == '\\') {
        if (check_hori(cur + left) && (dir == top || dir == top + left)) { return cur + left; }
        if (check_hori(cur + right) && (dir == bottom || dir == bottom + right)) { return cur + right; }
        if (check_vert(cur + top) && (dir == left || dir == top + left)) { return cur + top; }
        if (check_vert(cur + bottom) && (dir == right || dir == bottom + right)) { return cur + bottom; }
        if (check_bksl(cur + top + left) && (dir == left || dir == top || dir == top + left)) { return cur + top + left; }
        if (check_bksl(cur + bottom + right) && (dir == right || dir == bottom || dir == bottom + right)) { return cur + bottom + right; }
    }
    return position();
}

template <typename T>
bool in_range(T beg, const T& end, const T& val)
{
    for (; beg != end; ++beg) {
        if (beg.value() == val.value()) { return true; }
    }
    return false;
}

void Track::print(int step, const Train& ta, const Train& tb, const Track::iterator& pa, const Track::iterator& pb) const
{
    cout << "step = " << step << endl;
    for (size_t r = 0; r < track.size(); ++r) {
        for (size_t c = 0; c < track.at(r).size(); ++c) {
            Track::position pos(r, c);
            bool flag = false;
            if (pos == pa.cur) { cout << (char)toupper(ta.name.front()); continue; }
            if (pos == pb.cur) { cout << (char)toupper(tb.name.front()); continue; }
            for (auto it = pa - ta.length + 1; it != pa + 1; ++it) {
                if (pos == it.cur) {
                    cout << (char)tolower(ta.name.front());
                    flag = true;
                    break;
                }
            }
            if (flag) { continue; }
            for (auto it = pb - tb.length + 1; it != pb + 1; ++it) {
                if (pos == it.cur) {
                    cout << (char)tolower(tb.name.front());
                    flag = true;
                    break;
                }
            }
            if (flag) { continue; }
            cout << at(pos);
        }
        cout << endl;
    }
    cout << endl;
//     system("pause");
}

int train_crash(const string& track_str, const string& a_train_str, int a_train_pos, const string& b_train_str, int b_train_pos, int limit)
{
    cout << track_str << endl;
    cout << a_train_str << endl;
    cout << a_train_pos << endl;
    cout << b_train_str << endl;
    cout << b_train_pos << endl;
    cout << limit << endl;

    Track track(track_str);
    Train a_train(a_train_str), b_train(b_train_str);

    auto&& beg = track.begin();
    auto&& a = beg + a_train_pos;
    //auto a = beg;
    auto&& b = beg + b_train_pos;
    //for (int i = 0; i < a_train_pos; ++i, ++a) {
    //    track.print(i, a_train, b_train, a, beg);
    //}
    if (!a_train.clockwise) { a.reverse(); }
    if (!b_train.clockwise) { b.reverse(); }
    for (auto it = a - a_train.length + 1; it != a; ++it) {
        if (in_range(it + 1, a + 1, it)) { return 0; }
        if (in_range(b - b_train.length + 1, b + 1, it)) { return 0; }
    }
    for (auto it = b - b_train.length + 1; it != b; ++it) {
        if (in_range(it + 1, b + 1, it)) { return 0; }
    }
    
    if (*a == Track::station) { a_train.pause_time = 1; }
    if (*b == Track::station) { b_train.pause_time = 1; }
    for (int step = 0; step <= limit; ++step) {
        if(step>=1912)track.print(step, a_train, b_train, a, b);
        if (in_range(a - a_train.length + 1, a, a) ||
            in_range(a - a_train.length + 1, a + 1, b) ||
            in_range(b - b_train.length + 1, b + 1, a) ||
            in_range(b - b_train.length + 1, b, b))
        { return step; }
        a_train.run_cycle(a);
        b_train.run_cycle(b);
    }
    return -1;
}


#################################################
#include <vector>
#include <cctype>
#include <ios>

class TrainC;
class TrackC;
class TrackPoint;

class TrainC{
  friend class TrackC;
  private:
    size_t next_track_point = 0;
  public:
    int carriages = 1;
    bool express = false;
    int direction = 0;
    const int speed = 1;
    int pos = -1;
    int waiting_at_station = 0;
    TrainC(std::string, int);
};

TrainC::TrainC(std::string t, int p){
  pos = p;
  carriages = t.size() - 1;
  if(std::isupper(t[0])){  // engine on left
    direction = -1;
    express = (t[0] == 'X');
  }
  if(std::isupper(t[t.size()-1])){// engine on right
    direction = 1;
    express = (t[t.size()-1] == 'X');
  }
}

class TrackPoint{
  public:
    int x;
    int y;
    int pos = -1;
    int pos_c = -1;
    size_t index_c = 0;
    bool isstation = false;
    bool isoccupied = false;
    TrackPoint(int, int, int, char);
    bool operator== (const TrackPoint& b);
};

TrackPoint::TrackPoint(int col, int row, int p, char c){
  x = col;
  y = row;
  pos = p;
  isstation = (c == 'S');
}

bool TrackPoint:: operator== (const TrackPoint& b){
  return (x == b.x) && (y == b.y);
}

class TrackC{
    std::string padded_track(const std::string&, size_t&);
    bool trains_crashed_already = false;
     
  public:  
    std::vector<TrackPoint> stations_and_crossings ={};
    int length = 0;
    std::vector<TrainC> trains = {};
    
    TrackC(const std::string&);
    void trains_add(std::string t, int p);
    bool trains_crashed();
    bool station(TrainC t);
    bool crossing(TrainC t);
    bool station(int p);
};

TrackC::TrackC(const std::string& track){  
  size_t i, start_i, jx, jy, j, row_len;
  char c;
  int col, row; 
  int dir_x = 1, dir_y = 0;
  std::string s = padded_track(track, row_len);
  // find start
  i = row_len + 1;
  while(s[i]==' '){++i;}
  start_i = i; 
  col = i + 1 ; row = 1; // count rows and columns starting at 0 or at 1 ??!!
  stations_and_crossings.push_back(TrackPoint(col, row, 0, ' ')); // create a track point to prevent empty list
  
  // follow track
  auto neighbour = [&](int dx, int dy){ // works only on padded track!
    return i + (size_t)dx + (size_t)dy*row_len;};
  do{
    j = neighbour(dir_x, dir_y);
    //if((dir_x != 0) && (dir_y != 0)){ 
    if((s[i] == '/') || (s[i] == '\\')){ // direction changes only at '/' or '\'
      jx = neighbour(dir_x, 0);
      jy = neighbour(0, dir_y);
      if((j != i) && (dir_x == dir_y)
                        && ((s[j] == '\\') 
                         || (s[j] == 'X')
                         || (s[j] == 'S'))){;}
      else if ((j != i) && (dir_x == -1 * dir_y)
                        && ((s[j] == '/') 
                         || (s[j] == 'X')
                         || (s[j] == 'S'))){;} 
      else if((jx != i) && ((s[jx] == '-') 
                         || (s[jx] == '+')
                         || (s[jx] == 'S'))){j = jx; dir_y = 0;} // connection horizontal
      else if((jy != i) && ((s[jy] == '|')
                         || (s[jy] == '+')
                         || (s[jy] == 'S'))){j = jy; dir_x = 0;} // connection vertical
    }
    c = s[j];
    row += dir_y; // update position;
    col += dir_x;
    ++length;
    
    switch (c){
        case '/': {if(dir_y == 0){dir_y = -1 * dir_x;} // direction changes
                   if(dir_x == 0){dir_x = -1 * dir_y;}
                   break;}
        case '\\':{if(dir_y == 0){dir_y = dir_x;}
                   if(dir_x == 0){dir_x = dir_y;}               
                   break;}
        case '+': // direction does not change at crossings
        case 'X': 
        case 'S': {stations_and_crossings.push_back(TrackPoint(col, row, length, c));
                   for(size_t k = 0; k < stations_and_crossings.size()-1; ++k){
                      if (stations_and_crossings[k] == stations_and_crossings.back()){
                        stations_and_crossings[k].pos_c = stations_and_crossings.back().pos;  
                        stations_and_crossings.back().pos_c = stations_and_crossings[k].pos;
                        stations_and_crossings[k].index_c = stations_and_crossings.size()-1;  
                        stations_and_crossings.back().index_c = k;
                      } 
                   }
                   break;}
    }
    i = j;
  } while(i != start_i);
}

std::string TrackC::padded_track(const std::string& s, size_t& max_line){ // put spaces around and make all lines equal in lenghtt
  max_line = 0; 
  std::string r = "";
  size_t cur_line = 0, s_size = s.size() ;
  char c = ' ';
  for(size_t i = 0; i < s_size; ++i){ // determine lenght of longest row
    c = s[i];
    if(c == '\n'){
      max_line = cur_line > max_line ? cur_line : max_line;
      cur_line = 0;
    }
    ++cur_line; // don't count '\n'
  }
  cur_line = 0;
  max_line += 2; // one space in front and one in back
  r.append(max_line, ' ');
  r += "\n ";
  for(size_t i = 0; i < s_size; ++i){ // determine lenght of longest row
    c = s[i];
     ++cur_line; // now count '\n' because one additional space is in front of line
    if(c == '\n'){
      r.append(max_line-cur_line, ' ');
      r += "\n ";
      cur_line = 0;
    }
    else{
      r += c;
    }
  }
  r.append(max_line, ' '); // one final line of spaces
  r += "\n";
  max_line++; // now count '\n'
  std::cout << r <<"\n";
  return r;
}

bool TrackC::trains_crashed(){
  if (trains_crashed_already) return true;
  int ie, je, ic, ix, jx, t;
  for(size_t i = 0; i < trains.size(); ++i){
    ie = trains[i].pos; // engine position of train i
    ix = (trains[i].pos - trains[i].direction * trains[i].carriages + length)%length; // position of last carriage
    if(crossing(trains[i])){
      ic = stations_and_crossings[trains[i].next_track_point].pos_c; // train i is at crossing; ic crossing track position
      trains[i].next_track_point += trains[i].direction + stations_and_crossings.size();  // advance next_track_point 
      trains[i].next_track_point %= stations_and_crossings.size(); // avoid going to negatives, because next_track_point is unsigned int
    }
    else{
      ic = -1; // train i is not at crossing
    }
    for(size_t j = 0; j < trains.size(); ++j){
      je = trains[j].pos;  // engine position of train j
      jx = trains[j].pos - trains[j].direction * trains[j].carriages; // position of last carriage
      if(je < jx){t = je; je = jx; jx = t;} // for trains running left, flip values   
      
      if((jx < 0) || (je > length)){ // train j overlaps zero position
        if(jx < 0){jx += length;}
        if(je > length){je -= length;}
        if(i != j && 
           (ie <= je || ie >= jx ||  // crash with engine
            ix <= je || ix >= jx))  return true; // crash with tail
        if(ic > -1 && 
           (ic <= je || ic >= jx)) return true; // crash at crossing
      }
      else{
        if(i != j && 
           ((ie <= je && ie >= jx) ||  // crash with engine
            (ix <= je && ix >= jx))) return true;  // crash with tail
        if(ic > -1 && (ic <= je && ic >= jx)) return true; // crash at crossing
      }
    }
  }
  return false;
}

bool TrackC::station(int p){ // unused overload station()
  for(size_t i = 0; i < stations_and_crossings.size(); ++i){
    if((stations_and_crossings[i].pos == p) && stations_and_crossings[i].isstation){return true;}
  }
  return false;
}

bool TrackC::station(TrainC t){
  return (t.pos == stations_and_crossings[t.next_track_point].pos) 
         && stations_and_crossings[t.next_track_point].isstation;
}

bool TrackC::crossing(TrainC t){
  return t.pos == stations_and_crossings[t.next_track_point].pos;
}

void TrackC::trains_add(std::string t, int p){
  trains.push_back(TrainC(t,p));
  size_t i = 0;
  //size_t j = 0;
  if (! empty(stations_and_crossings)){ // find first track_point for train
    if (trains.back().direction > 0){   // train moving to right
      while(stations_and_crossings[i].pos <= trains.back().pos){
        ++i;
        if (i == stations_and_crossings.size()){
          i = 0;
          break;
        }
      }
      //j = (i + stations_and_crossings.size() - 1) % stations_and_crossings.size(); // preceeding track_point;
    }
    else if(trains.back().direction < 0){ // train moving to left
      i = stations_and_crossings.size()-1;
      while(stations_and_crossings[i].pos >= trains.back().pos){
        if (i == 0){
          i = stations_and_crossings.size()-1;
          break;
        }
        --i;
      }
    } 
    trains.back().next_track_point = i;
    
    // check if train overlaps any track_points
    // if so, check if track_point already occupied -> trains already crashed before start
    //       mark track_points as occupied
    // p = engine position of train
    int t;
    int x = p - trains.back().direction * trains.back().carriages; // position of last carriage 
    if(p < x){t = p; p = x; x = t;} // for trains running left, flip values
    for(i = 0; i < stations_and_crossings.size(); ++i){ // iterate over track_points 
      if(x < 0 || p > length){ // train j overlaps zero position
        if(x < 0) x += length;
        if(p > length) p -= length;
        if (stations_and_crossings[i].pos <= p || stations_and_crossings[i].pos >= x){
          if (stations_and_crossings[i].isoccupied) trains_crashed_already = true; // crash at crossing
          stations_and_crossings[i].isoccupied = true;
          if (stations_and_crossings[i].pos_c > -1) stations_and_crossings[stations_and_crossings[i].index_c].isoccupied = true;
      }}
      else{
        if (stations_and_crossings[i].pos <= p && stations_and_crossings[i].pos >= x){
          if (stations_and_crossings[i].isoccupied) trains_crashed_already = true; // crash at crossing
          stations_and_crossings[i].isoccupied = true;
          if (stations_and_crossings[i].pos_c > -1) stations_and_crossings[stations_and_crossings[i].index_c].isoccupied = true;
      }}  
    }
  }
  
  return;  
}


int train_crash(const std::string &track, const std::string &a_train, int a_train_pos, const std::string &b_train, int b_train_pos, int limit){
  
  TrackC t(track);
  t.trains_add(a_train, a_train_pos);
  t.trains_add(b_train, b_train_pos);
  
  /*std::cout << t.length << "  length "  << "\n";
  std::cout << t.stations_and_crossings.size() << "\n";
  std::cout << a_train << " " << t.trains[0].pos << "\n";
  std::cout << b_train << " " << t.trains[1].pos << "\n";*/
  
  int i = 0;
  ++ limit; // otherwise it does one iteration too few
  while ((! t.trains_crashed()) && (i < limit)){
    ++i;
    for(size_t j = 0; j < t.trains.size(); ++j){
      if(t.trains[j].waiting_at_station > 0){ // train is waiting at a station
        --t.trains[j].waiting_at_station;
      }
      else{
        t.trains[j].pos += t.trains[j].direction * t.trains[j].speed + t.length; // advances the train
        t.trains[j].pos %= t.length;
        if(t.station(t.trains[j])){
          if(! t.trains[j].express){ // express trains don't stop at stations
            t.trains[j].waiting_at_station = t.trains[j].carriages; // stops for number of carriages time units
      } } }
    }
  }
    
  if(i == limit){return -1;} // no crash has occured
  return i;
}
###########################################
#include <bits/stdc++.h>
#include <set>
#include <unordered_map>
#include <algorithm> 
#include <vector>
#include <string>
#include <stdio.h>

using namespace std;

class Train {
  public: int i, l, d, e, w ,f;
};

bool intersects(set<pair<int, int>> a, set<pair<int, int>> b);
void update_train(Train& train, unordered_map<int, pair<int, int>> plot, vector<vector<char>> grid, int it);
set<pair<int, int>> get_train_coords(Train train, unordered_map<int, pair<int, int>> plot);
bool train_self_collides(Train train, unordered_map<int, pair<int, int>> plot);
Train make_train(const string &train, int i);
unordered_map<int, pair<int, int>> plot_track(vector<vector<char>> grid, pair<int, int> p0);
pair<int, int> find_start(vector<vector<char>> grid);
vector<vector<char>> make_grid(const string &track);

// =======================================
// Blaine is a pain, and that is the truth
// =======================================

int train_crash(const string &track, const string &a_train, int a_train_pos, const string &b_train, int b_train_pos, int limit) {
  auto grid = make_grid(track);
  auto p0 = find_start(grid);
  auto plot = plot_track(grid, p0);
  auto ta = make_train(a_train, a_train_pos);
  auto tb = make_train(b_train, b_train_pos);
  int it = 0;
  while (it <= limit) {
    if (train_self_collides(ta, plot) || train_self_collides(tb, plot) || intersects(get_train_coords(ta, plot), get_train_coords(tb, plot))) {
      return it;
    }
    update_train(ta, plot, grid, it);
    update_train(tb, plot, grid, it);
    it++;
  }
  return -1;
}

bool intersects(set<pair<int, int>> a, set<pair<int, int>> b) {
  for (auto x : a)
    for (auto y : b)
      if (x.first == y.first && x.second == y.second) return true;
  return false;
}

void update_train(Train& train, unordered_map<int, pair<int, int>> plot, vector<vector<char>> grid, int it) {
  if (train.w > 0) {
    train.w = train.w - 1;
    train.f = train.w == 0 ? 1 : 0;
  } else {
    auto p = plot[train.i];
    int y = p.first;
    int x = p.second;
    if (train.e == 0 && it > 0 && train.f == 0 && grid[y][x] == 'S') {
      train.w = train.l - 2;
      train.f = train.w == 0 ? 1 : 0;
    } else {
      train.i = ((train.i + train.d) + plot.size()) % plot.size();
      train.f = 0;
    }
  }
}

set<pair<int, int>> get_train_coords(Train train, unordered_map<int, pair<int, int>> plot) {
  set<pair<int, int>> coords;
  for (int j=0; j<train.l; j++) {
    int k = ((train.i - (j * train.d)) + plot.size()) % plot.size();
    auto p = plot[k];
    coords.insert(p);
  }
  return coords;
}

bool train_self_collides(Train train, unordered_map<int, pair<int, int>> plot) {
  set<pair<int, int>> coords;
  for (int j=0; j<train.l; j++) {
    int k = ((train.i - (j * train.d)) + plot.size()) % plot.size();
    auto p = plot[k];
    if (coords.find(p) != coords.end()) return true;
    coords.insert(p);
  }
  return false;
}

Train make_train(const string &train, int i) {
  Train t;
  t.i = i; t.l = train.length(); t.w = 0; t.f = 0;
  char h = train[0];
  t.d = (h >= 'a' && h <= 'z') ? 1 : -1;
  t.e = (h == 'x' || h == 'X') ? 1 : 0;
  return t;
}

unordered_map<int, pair<int, int>> plot_track(vector<vector<char>> grid, pair<int, int> p0) {
  unordered_map<int, pair<int, int>> plot;
  int x0 = p0.second, y0 = p0.first, i = 0, dx = 1, dy = -1;
  int x = x0, y = y0;
  string s = "-|+XS";
  while (plot.size() == 0 || !(x == x0 && y == y0)) {
    plot.insert({i, {y,x}});
    char t = grid[y][x];
    if (s.find(t) == string::npos) {
      if (t == '/') {
        if (dy == 0) dy = -dx;
        else if (dx == 0) dx = -dy;
      } else if (t == '\\') {
        if (dy == 0) dy = dx;
        else if (dx == 0) dx = dy;
      }
      char u = grid[y+dy][x+dx];
      if ((t != u) && (t != 'X')) {
        char h = grid[y][x+dx];
        if (h == '-') {
          dy = 0;
        } else {
          char v = grid[y+dy][x];
          if (v == '|') {
            dx = 0;
          } else if (u != 'S') {
            if (h == 'S') dy = 0;
            else if (v == 'S') dx = 0;
          }
        }
      }
    }
    y+=dy; x+=dx; i++;
  }
  return plot;
}

pair<int, int> find_start(vector<vector<char>> grid) {
  string s = "-|/\\+XS";
  for (unsigned long i=0; i<grid.size(); i++)
    for (unsigned long j=0; j<grid[i].size(); j++)
      if (s.find(grid[i][j]) != string::npos)
        return {i,j};
  return {-1,-1};
}

vector<vector<char>> make_grid(const string &track) {
  vector<vector<char>> grid, res;
  vector<char> bf, a, b;
  bf.push_back(' ');
  unsigned long n = 0;
  for (auto c : track) {
    if (c == '\n') {
      bf.push_back(' ');
      if (bf.size() > n) n = bf.size();
      vector<char> row;
      for (auto r : bf) row.push_back(r);
      grid.push_back(row);
      bf.clear();
      bf.push_back(' ');
    } else {
      bf.push_back(c);
    }
  }
  grid.insert(grid.begin(), a);
  grid.push_back(b);
  for (auto v : grid) {
    while (v.size() < n) v.push_back(' ');
    res.push_back(v);
  }
  return res;
}
