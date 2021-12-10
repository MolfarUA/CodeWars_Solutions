int maze[3][3];
int dfs(int x, int y, int length, long long val)
{
    if (length == 0) return 1;
    int ret = 0;
    for (int i=0; i < 3; ++i)
        for (int j=0; j < 3; ++j) {
            if (maze[i][j]) continue;
            int a = abs(x+i), b = abs(y+j);
            maze[i][j] = 1;
            if (((a|b)&1) || maze[a>>1][b>>1]) {
                ret += dfs(i, j, length-1, (val+i)*10+j);
            }
            maze[i][j] = 0;
        }
    return ret;
}

unsigned int countPatternsFrom(char firstDot, unsigned short length) { 
    if (length <= 0 || length > 9) return 0;
    static int dp[5][10] = {0};
    firstDot -= 'A';
    firstDot = firstDot == 4 ? 4 : firstDot&1;
    int x = firstDot/3, y = firstDot%3;
    if (dp[firstDot][length]) 
        return dp[firstDot][length]; 
    maze[x][y] = 1;
    dp[firstDot][length] = dfs(x, y, length-1, 10 + firstDot);
    maze[x][y] = 0;
    return dp[firstDot][length]; 
}

####################
#include <map>
#include <set>
#include <vector>
#include <algorithm>

const std::map< char, std::vector< char > > connections =
{
    { 'A', { 'B', 'E', 'D', 'H', 'F' } }, // 5
    { 'B', { 'A', 'C', 'D', 'E', 'F', 'G', 'I' } }, // 7
    { 'C', { 'B', 'E', 'F', 'D', 'H' } }, // 5
    { 'D', { 'A', 'G', 'B', 'E', 'H', 'C', 'I' } }, // 7
    { 'E', { 'A', 'B', 'C', 'D', 'F', 'G', 'H', 'I' } }, // 8
    { 'F', { 'C', 'I', 'B', 'E', 'H', 'A', 'G' } }, // 7
    { 'G', { 'D', 'E', 'H', 'B', 'F' } }, // 5
    { 'H', { 'D', 'E', 'F', 'G', 'I', 'A', 'C' } }, // 5
    { 'I', { 'F', 'E', 'H', 'B', 'D' } } // 5
};

const std::map< std::pair< char, char >, char > connections_jumps =
{
    { {'A', 'B' }, 'C' },
    { {'A', 'E' }, 'I' },
    { {'A', 'D' }, 'G' },
    { {'C', 'B' }, 'A' },
    { {'C', 'E' }, 'G' },
    { {'C', 'F' }, 'I' },
    { {'G', 'H' }, 'I' },
    { {'G', 'E' }, 'C' },
    { {'G', 'D' }, 'A' },
    { {'I', 'F' }, 'C' },
    { {'I', 'E' }, 'A' },
    { {'I', 'H' }, 'G' },
    { {'B', 'E' }, 'H' },
    { {'D', 'E' }, 'F' },
    { {'H', 'E' }, 'B' },
    { {'F', 'E' }, 'D' }
};

unsigned int countPatternsFrom(char firstDot, unsigned short length, std::set< char > path) {
    if(length > 10) return 0;
    if(length == 0) return 0;
    if(length == 1) return 1;

    path.insert(firstDot);
    unsigned int count = 0;
    for(char connection : connections.at(firstDot)) {
        if(path.find(connection) == path.end()) { // Si no visitado
            count += countPatternsFrom(connection, length - 1, path);
        } else {
            // Si ya fue visitado, entonces intentamos traducirlo
            auto it = connections_jumps.find({ firstDot, connection });
            if(it != connections_jumps.end()) { // Si tiene un jump...
                connection = it->second;
                if(path.find(connection) == path.end()) { // Si no fue visitado
                    count += countPatternsFrom(connection, length - 1, path);
                }
            }
        }
    }
    return count;
}

unsigned int countPatternsFrom(char firstDot, unsigned short length) {
    std::set< char > path;
    return countPatternsFrom(firstDot, length, path);
}

#######################
#include <array>

// based on onother solution (using const value) but here with array and constexpr
constexpr unsigned int  countPatternsFrom(char firstDot, unsigned short length) {
  if (length < 0 || length > 9){ return 0;}
  constexpr const std::array<unsigned int, 10>ACIG = {0, 1, 5, 31, 154, 684, 2516, 7104, 13792, 13792};
  constexpr const std::array<unsigned int, 10>BDFG = {0, 1, 7, 37,188,816, 2926, 8118,15564,15564};
  constexpr const std::array<unsigned int, 10>E = {0, 1, 8, 48, 256, 1152, 4248, 12024, 23280, 23280};
  constexpr const std::array<std::array<unsigned int, 10>, 10> All = {ACIG, BDFG, ACIG, BDFG, E, BDFG, ACIG, BDFG, ACIG};
  return All[firstDot-'A'][length];
}

###############
#include <string>
#include <vector>


using namespace std;


typedef struct edge {
    char from;
    char to;
    char through;
} edge_t;


vector<edge_t> graph = {
    { 'A', 'B', 0 }, { 'A', 'C', 'B' }, { 'A', 'D', 0 }, { 'A', 'E', 0 },
    { 'A', 'F', 0 }, { 'A', 'G', 'D' }, { 'A', 'H', 0 }, { 'A', 'I', 'E' },

    { 'B', 'A', 0 }, { 'B', 'C', 0 }, { 'B', 'D', 0 }, { 'B', 'E', 0 },
    { 'B', 'F', 0 }, { 'B', 'G', 0 }, { 'B', 'H', 'E' }, { 'B', 'I', 0 },

    { 'C', 'A', 'B' }, { 'C', 'B', 0 }, { 'C', 'D', 0 }, { 'C', 'E', 0 },
    { 'C', 'F', 0 }, { 'C', 'G', 'E' }, { 'C', 'H', 0 }, { 'C', 'I', 'F' },

    { 'D', 'A', 0 }, { 'D', 'B', 0 }, { 'D', 'C', 0 }, { 'D', 'E', 0 },
    { 'D', 'F', 'E' }, { 'D', 'G', 0 }, { 'D', 'H', 0 }, { 'D', 'I', 0 },

    { 'E', 'A', 0 }, { 'E', 'B', 0 }, { 'E', 'C', 0 }, { 'E', 'D', 0 },
    { 'E', 'F', 0 }, { 'E', 'G', 0 }, { 'E', 'H', 0 }, { 'E', 'I', 0 },

    { 'F', 'A', 0 }, { 'F', 'B', 0 }, { 'F', 'C', 0 }, { 'F', 'D', 'E' },
    { 'F', 'E', 0 }, { 'F', 'G', 0 }, { 'F', 'H', 0 }, { 'F', 'I', 0 },

    { 'G', 'A', 'D' }, { 'G', 'B', 0 }, { 'G', 'C', 'E' }, { 'G', 'D', 0 },
    { 'G', 'E', 0 }, { 'G', 'F', 0 }, { 'G', 'H', 0 }, { 'G', 'I', 'H' },

    { 'H', 'A', 0 }, { 'H', 'B', 'E' }, { 'H', 'C', 0 }, { 'H', 'D', 0 },
    { 'H', 'E', 0 }, { 'H', 'F', 0 }, { 'H', 'G', 0 }, { 'H', 'I', 0 },

    { 'I', 'A', 'E' }, { 'I', 'B', 0 }, { 'I', 'C', 'F' }, { 'I', 'D', 0 },
    { 'I', 'E', 0 }, { 'I', 'F', 0 }, { 'I', 'G', 'H' }, { 'I', 'H', 0 },
};


unsigned int countPatternsFrom(char firstDot, unsigned short length, string usedDots = "") {
    unsigned int count = 0;
    
    if ((length < 1) || (length > 9)) {
        count = 0;
    }
    else if (length == 1) {
        //cout << usedDots << firstDot << endl;
        count = 1;
    }
    else {
        for (auto i : graph) {
            if ( (i.from == firstDot) && (usedDots.find(i.to) == string::npos) && ((i.through == 0) || (usedDots.find(i.through) != string::npos)) ) {
                count += countPatternsFrom(i.to, length - 1, usedDots + i.from);
            }
        }
    }

    return count;
}

#########################
#include <vector>
#include <functional>

unsigned int countPatternsFrom(char firstDot, unsigned short length) {
  if (length < 1 || length > 9) return 0;
  std::vector<bool> dots(9, true);

  auto isAllowed = [&] (auto x, auto y) {
    if (!dots[y]) return false;
    if (x < y) std::swap(x, y);
    if (x - y == 2 && y % 3 == 0 && dots[y + 1]) return false;
    if (x - y == 6               && dots[y + 3]) return false;
    if (x == 8 && y == 0         && dots[4]    ) return false;
    if (x == 6 && y == 2         && dots[4]    ) return false;
    return true;
  };
  
  std::function<unsigned int(unsigned int, unsigned int)> deep = [&] (auto step, auto point) {
    if (step == length) return 1u;
    unsigned int result = 0;
    dots[point] = false;
    for (unsigned int i = 0; i < 9; i ++) if (isAllowed(point, i)) result += deep(step + 1, i);
    dots[point] = true;
    return result;
  };
  
  return deep(1, firstDot - 'A');
}

#########################
#include <unordered_map>

using namespace std;

struct Pos {
  unsigned _r;
  unsigned _c;
  
  Pos(unsigned r, unsigned c) : _r(r), _c(c) {}
  Pos(const Pos &pos) : _r(pos._r), _c(pos._c) {}
  
  bool operator==(const Pos &pos) const { return _r == pos._r && _c == pos._c; }
};

const unordered_map<char, Pos> char2pos = {
  {'A', Pos(0,0)},
  {'B', Pos(0,1)},
  {'C', Pos(0,2)},
  {'D', Pos(1,0)},
  {'E', Pos(1,1)},
  {'F', Pos(1,2)},
  {'G', Pos(2,0)},
  {'H', Pos(2,1)},
  {'I', Pos(2,2)}
};

// global is fine because recCount sets all values back to false
array<array<bool, 3>, 3> visited;

bool linkable(Pos pos1, Pos pos2) {
  if ((pos1._r == 1 && pos1._c == 1) || (pos2._r == 1 && pos2._c == 1)) { // 1 or 2 is center dot
    return true;
  }
  if (pos1._r != 1 && pos1._c != 1) { // 1 is a corner dot
    if (pos2._r == pos1._r) { // 2 is in the same row
      return pos2._c == 1 || visited[pos1._r][1];
    }
    if (pos2._c == pos1._c) { // 2 is in the same col
      return pos2._r == 1 || visited[1][pos1._c];
    }
    if (pos2._r == 2 - pos1._r && pos2._c == 2 - pos1._c) { // 2 is the opposite corner dot
      return visited[1][1];
    }
    return true;
  }
  // 1 is a side dot
  if ((pos2._r == pos1._r && pos2._c == 2 - pos1._c) || // 1 and 2 are on opposite sides of the middle row
      (pos2._c == pos1._c && pos2._r == 2 - pos1._r)) { // 1 and 2 are on opposite sides of the middle col
    return visited[1][1];
  }  
  return true;
}

unsigned recCount(char dot, unsigned length) {
  if (length == 0) {
    return 1;
  }
  
  unsigned count = 0;
  
  Pos pos = char2pos.at(dot);
  visited[pos._r][pos._c] = true;
  
  for (char nextDot = 'A'; nextDot <= 'I'; ++nextDot) {
    if (nextDot == dot) {
      continue;
    }
    Pos nextPos = char2pos.at(nextDot);
    if (!visited[nextPos._r][nextPos._c] && linkable(pos, nextPos)) {
      count += recCount(nextDot, length - 1);
    }
  }
  
  visited[pos._r][pos._c] = false;
  
  return count;
}

unsigned int countPatternsFrom(char firstDot, unsigned short nbDots) {
  if (nbDots == 0 || nbDots > 9) {  
    return 0;
  }
  else if (nbDots == 1) {
    return 1;
  }
  
  return recCount(firstDot, nbDots - 1);
}

##########################
#include <bitset>
#include <queue>
#include <cassert>
//-----------------------------------------------------------------------------
const unsigned short N = 3;
//-----------------------------------------------------------------------------
class Pattern
{
public:
    explicit Pattern(unsigned short start_);
    void GoTo(unsigned short next_);
    unsigned short Length() const;
    bool IsTaken(unsigned short dot_) const;

private:
    std::bitset<N*N> m_dots;
    unsigned short m_last;
};
//-----------------------------------------------------------------------------
unsigned short countPatternsFrom(char firstDot_, unsigned short length_) 
{
    // Invalid input
    if ((0 == length_) || (N*N < length_) 
            || (firstDot_ < 'A') || (('A' + N*N) <=  firstDot_))
    {
        return 0;
    }

    // Find all patterns
    std::queue<Pattern> patterns;
    unsigned short first = firstDot_-'A';
    patterns.push(Pattern(first));
    while (patterns.front().Length() < length_)
    {
        Pattern patternToCont = patterns.front();
        patterns.pop();

        for (unsigned short i = 0; i < N*N; ++i)
        if (!patternToCont.IsTaken(i))
        try 
        {
            Pattern newPattern = patternToCont;
            newPattern.GoTo(i);
            patterns.push(newPattern);
        }
        catch(const std::exception& e) {}
  }
  
  return patterns.size();
}
//-----------------------------------------------------------------------------
Pattern::Pattern(unsigned short start_)
    : m_dots()
    , m_last(N*N)   // Initial invalid dot
{ 
    GoTo(start_);
}
//-----------------------------------------------------------------------------
void Pattern::GoTo(unsigned short next_)
{
    assert(next_ < N*N);
    assert(!IsTaken(next_));

    if (m_last < N*N)
    {
        short newX = next_ % 3;     short newY = next_ / 3;
        short prvX = m_last % 3;    short prvY = m_last / 3;
        short diffX = newX - prvX;  short diffY = newY - prvY;
        if ((0 == abs(diffX) % 2) && (0 == abs(diffY) % 2)
                && (false == m_dots[m_last + (diffY * 3 / 2) + (diffX / 2)]))
        {
            throw std::runtime_error("Skip un-taken point");
        }
    }

    m_dots[next_] = true;
    m_last = next_;
}
//-----------------------------------------------------------------------------
unsigned short Pattern::Length() const
{
    return m_dots.count();
}
//-----------------------------------------------------------------------------
bool Pattern::IsTaken(unsigned short dot_) const
{
    return m_dots[dot_];
}

#########################
#include <iostream>
#include <vector>
#include <math.h>
using namespace std;
int lenght;
int k=1;
int count_form_now(vector<vector<int>> dots,int x,int y,int lenght_now)
{
    //cout<<x<<ends<<y<<ends<<lenght_now<<ends<<lenght<<endl;
    dots[y][x]=lenght_now;
    if(lenght_now==lenght) {
            /*for(int i=0;i<3;++i)
            {
                for(int j=0;j<3;++j)
                cout<<dots[i][j]<<ends;
                cout<<endl;
    }
    cout<<k++<<endl;*/
            return 1;}

    int c=0;

    for(int i=0;i<3;++i)
        for(int j=0;j<3;++j)
    {
        if(y==i && x==j) continue;
        if(dots[i][j]!=0) continue;
        if(abs(x-j)!=2 && abs(y-i)!=2)
        c+=count_form_now(dots,j,i,lenght_now+1);
        else if( abs(x-j)==1 || abs(y-i)==1)
        c+=count_form_now(dots,j,i,lenght_now+1);
        else if(abs(x-j)==2 && abs(y-i)==2 ){if(dots[1][1]!=0)
        c+=count_form_now(dots,j,i,lenght_now+1);}
        else if(abs(x-j)==2 && dots[y][1]!=0)
        c+=count_form_now(dots,j,i,lenght_now+1);
        else if(abs(y-i)==2 && dots[1][x]!=0)
        c+=count_form_now(dots,j,i,lenght_now+1);

    }
    return c;
}
unsigned int countPatternsFrom(char firstDot, unsigned short length) {
  // Your code here
  if(!length) return 0;
  lenght=length;
  vector<vector<int>> dots(3);
  for(int i=0;i<3;++i)
      for(int j=0;j<3;++j)
        dots[i].push_back(0);

    int x,y;
    switch (firstDot)
        {
        case 'A':
            {
                x=0;y=0;
                break;
            }
        case 'B':
            {
                x=1;y=0;
                break;
            }
        case 'C':
            {
                x=2;y=0;
                break;
            }
        case 'D':
            {
                x=0;y=1;
                break;
            }
        case 'E':
            {
                x=1;y=1;
                break;
            }
        case 'F':
            {
                x=2;y=1;
                break;
            }
        case 'G':
            {
                x=0;y=2;
                break;
            }
        case 'H':
            {
                x=1;y=2;
                break;
            }
        case 'I':
            {
                x=2;y=2;
                break;
            }

        }



    return count_form_now(dots,x,y,1);

}

#########################
#define DOT(C) dots[C - 'A']
#define GO(C) if (!DOT(C)) res += countPatternsFrom(C, length - 1, dots)
#define GO_ACGI(C1, C2, C3, C4, C5, C6, C7, C8) do { \
    GO(C1); else GO(C2); GO(C3); GO(C4); else GO(C5); GO(C6); GO(C7); else GO(C8); \
} while (0)
#define GO_BDFH(C1, C2, C3, C4, C5, C6, C7, C8) do { \
    GO(C1); GO(C2); GO(C3); GO(C4); else GO(C5); GO(C6); GO(C7); GO(C8); \
} while (0)
constexpr unsigned int countPatternsFrom(char firstDot, unsigned short length, bool dots[9] = (bool[9]){})
{
    if (DOT(firstDot) || length > 9) return 0u;
    if (length < 2) return length;
    unsigned int res = 0u;
    DOT(firstDot) = 1;
    switch (firstDot)
    {
        case 'A': GO_ACGI('B', 'C', 'F', 'E', 'I', 'H', 'D', 'G'); break;
        case 'B': GO_BDFH('A', 'C', 'D', 'E', 'H', 'F', 'G', 'I'); break;
        case 'C': GO_ACGI('F', 'I', 'H', 'E', 'G', 'D', 'B', 'A'); break;
        case 'D': GO_BDFH('G', 'A', 'H', 'E', 'F', 'B', 'I', 'C'); break;
        case 'E': GO('A'); GO('B'); GO('C'); GO('D'); GO('I'); GO('F'); GO('G'); GO('H'); break;
        case 'F': GO_BDFH('C', 'I', 'B', 'E', 'D', 'H', 'A', 'G'); break;
        case 'G': GO_ACGI('H', 'I', 'F', 'E', 'C', 'B', 'D', 'A'); break;
        case 'H': GO_BDFH('G', 'I', 'D', 'E', 'B', 'F', 'A', 'C'); break;
        case 'I': GO_ACGI('F', 'C', 'B', 'E', 'A', 'D', 'H', 'G');
    }
    DOT(firstDot) = 0;
    return res;
}

######################
#include <set>
#include <numeric>
#include <map>
#include <utility>

using liason_table = std::map< std::pair<char, char>, char >;
using dot_table = std::set<char>;

liason_table liaisons() {
  liason_table l;
  l[{'A', 'C'}] = 'B';
  l[{'A', 'I'}] = 'E';
  l[{'A', 'G'}] = 'D';
  
  l[{'C', 'A'}] = 'B';
  l[{'C', 'G'}] = 'E';
  l[{'C', 'I'}] = 'F';
  
  l[{'G', 'I'}] = 'H';
  l[{'G', 'C'}] = 'E';
  l[{'G', 'A'}] = 'D';
  
  l[{'I', 'G'}] = 'H';
  l[{'I', 'A'}] = 'E';
  l[{'I', 'C'}] = 'F';
    
  l[{'B', 'H'}] = 'E';
  l[{'H', 'B'}] = 'E';
  l[{'D', 'F'}] = 'E';
  l[{'F', 'D'}] = 'E';
  return l;
}

unsigned int  count_sub_patterns(const liason_table& l, char dot, dot_table todo, dot_table done, int length) {
  if (length < 0 || length > 9)
    return 0u;
  
  if (length == 1)
    return 1u;
  
  todo.erase(dot);
  done.insert(dot);

  return std::accumulate(todo.begin(), todo.end(), 0u, [&](auto r, auto c) {
    auto t = l.find({dot, c});
    return  (t == l.end() ||  done.find(t->second) != done.end()) ? r + count_sub_patterns(l, c, todo, done, length-1) : r;
  });

}

unsigned int countPatternsFrom(char firstDot, unsigned short length) {  
  static const auto &l = liaisons();
  static const dot_table initial_table =  {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'};
  return count_sub_patterns(l, firstDot, initial_table, {}, length);
   
}
