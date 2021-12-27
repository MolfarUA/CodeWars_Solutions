#include <algorithm>
#include <array>
#include <bitset>
#include <cassert>
#include <iomanip>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <vector>

static constexpr bool s_debug = false;
static constexpr bool s_print_challenge = false;
static constexpr bool s_emit_code = false;

using height = unsigned;

static size_t constexpr N = 7;
enum : height { none, h1, h2, h3, h4, h5, h6, h7 };
using clue = unsigned;
using seq  = std::array<height, N>;

using option   = std::bitset<N>;
using option_seq = std::array<option, N>;

namespace utility {
  size_t forward(size_t i) { return i; }
  size_t reverse(size_t i) { return N-1-i; }

  unsigned long hint_to_mask(height h) { return h? 1ul << (h - 1) : 0; }

  static clue calc_clue(seq s) {
    height cur = none;
    clue result = none;
    auto b = s.begin(), e = s.end();
    while (b!=e) {
      result += (*b > cur);
      cur = std::max(cur, *b);
      ++b;
    }
    return result;
  }

  static clue calc_clue(option_seq s) {
    unsigned long cur = none;
    clue result = none;
    auto b = s.begin(), e = s.end();
    while (b!=e) {
      result += (b->to_ulong() > cur);
      cur = std::max(cur, b->to_ulong());
      ++b;
    }
    return result;
  }

  using SolutionSpace = std::multimap<clue, seq>;
#if 1 || defined(GENERATE_SOLUTION_SPACE)
  static SolutionSpace const solutionspace = []{
      SolutionSpace r;
      seq s;
      std::iota(begin(s), end(s), height(h1));
      
      do r.emplace(calc_clue(s), s);
      while (std::next_permutation(s.begin(), s.end()));
      if (s_emit_code) {
        std::cout << "    static SolutionSpace const solutionspace\n";
        std::cout << "    {\n";
        for (auto& c : r) {
          std::cout
            << "    { {" << c.first << "u}, "
            << "{{" 
            << c.second[0] << "u," << c.second[1] << "u," << c.second[2] << "u," 
            << c.second[3] << "u," << c.second[4] << "u," << c.second[5] << "u," 
            << c.second[6] << "u}} }," << std::endl;
        }
        std::cout << "    };\n";
      }

      return r;
  }();

  auto const hint_options = []{
    std::array<option_seq, N+1> result;

    for (auto& all : result.at(0))
      all.flip();

    for (size_t i = 1; i<N+1; ++i) {
      auto range = solutionspace.equal_range(i);
      result[i] = std::accumulate(range.first, range.second, option_seq{}, 
        [](option_seq accum, auto const&s) {
          for(auto i=0u; i<N; ++i) accum[i] |= hint_to_mask(s.second[i]);
          return accum;
        });
    }

    if (s_emit_code) {
      std::cout << "    std::array<option_seq, N+1> const hint_options = {{\n";
      for (size_t i = 0; i<N+1; ++i) {
        std::cout << "    /*" << i << "*/ {{";
        for (auto& x : result.at(i))
          std::cout << "option{\"" << x << "\"}, ";

        std::cout << "}}, \n";
      }
      std::cout << "    }};\n";
    }

    return result;
  }();
#else
    std::array<option_seq, N+1> const hint_options = {{
      /*0*/ {{option{"1111111"}, option{"1111111"}, option{"1111111"}, option{"1111111"}, option{"1111111"}, option{"1111111"}, option{"1111111"}, }}, 
      /*1*/ {{option{"1000000"}, option{"0111111"}, option{"0111111"}, option{"0111111"}, option{"0111111"}, option{"0111111"}, option{"0111111"}, }}, 
      /*2*/ {{option{"0111111"}, option{"1011111"}, option{"1111111"}, option{"1111111"}, option{"1111111"}, option{"1111111"}, option{"1111111"}, }}, 
      /*3*/ {{option{"0011111"}, option{"0111111"}, option{"1111111"}, option{"1111111"}, option{"1111111"}, option{"1111111"}, option{"1111111"}, }}, 
      /*4*/ {{option{"0001111"}, option{"0011111"}, option{"0111111"}, option{"1111111"}, option{"1111111"}, option{"1111111"}, option{"1111111"}, }}, 
      /*5*/ {{option{"0000111"}, option{"0001111"}, option{"0011111"}, option{"0111111"}, option{"1111111"}, option{"1111111"}, option{"1111111"}, }}, 
      /*6*/ {{option{"0000011"}, option{"0000111"}, option{"0001111"}, option{"0011111"}, option{"0111111"}, option{"1111111"}, option{"1111111"}, }}, 
      /*7*/ {{option{"0000001"}, option{"0000010"}, option{"0000100"}, option{"0001000"}, option{"0010000"}, option{"0100000"}, option{"1000000"}, }}, 
    }};
#endif

  struct puzzle {
    std::array<option_seq, N> field{{{{0}}}};
    struct clues { int forward, backward; };
    std::array<clues, N> colclues, rowclues;

    template <typename Clues>
    puzzle(Clues const& input) 
      : colclues {{
        clues {input[0], input[3*N-1]},
        clues {input[1], input[3*N-2]},
        clues {input[2], input[3*N-3]},
        clues {input[3], input[3*N-4]}, 
        clues {input[4], input[3*N-5]}, 
        clues {input[5], input[3*N-6]}, 
        clues {input[6], input[3*N-7]}, 
        }},
        rowclues {{
        clues {input[4*N-1], input[N+0]},
        clues {input[4*N-2], input[N+1]},
        clues {input[4*N-3], input[N+2]},
        clues {input[4*N-4], input[N+3]},
        clues {input[4*N-5], input[N+4]},
        clues {input[4*N-6], input[N+5]},
        clues {input[4*N-7], input[N+6]},
        }}
    { 
      for (auto& r : field) for (auto& c : r) c.flip(); // start with all options
      if (s_debug) { std::cout << "-- INITIALIZED\n"; dump(); }
    }

    void preapply_hints() {
      enum { phase1, phase2, phase3, phase4 };
      for (int x : {phase1,phase2,phase3,phase4}) {
        for (size_t ri = 0; ri<N; ++ri) for (size_t ci = 0; ci<N; ++ci) {
          assert(&row(ri).at(ci) == &col(ci).at(ri));

          {
            auto& cell = row(ri).at(ci);
            if (x==phase1) cell &= hint_options.at(rowclues.at(ri).forward).at(ci);
            if (x==phase3) cell &= hint_options.at(colclues.at(ci).forward).at(ri);
          }

          {
            auto& cell = row(ri).at(reverse(ci));
            if (x==phase2) cell &= hint_options.at(rowclues.at(ri).backward).at(ci);
          }
          {
            option& cell = col(ci).at(reverse(ri));
            if (x==phase4) cell &= hint_options.at(colclues.at(ci).backward).at(ri);
          }
        }

        char const* names[] = {"row (L)", "row (R)", "col (T)", "col (B)" };
        if (s_debug) { std::cout << "-- APPLIED HINTS PHASE " << names[x] << "\n"; dump(); }
      }
      if (s_debug) { std::cout << "-- APPLY HINTS\n"; dump(); }
    }

    bool solve_exclusive_options() {
      auto isolate = [](auto&& group) {
                // count options
                int counts[N] = {0};

                {
                    option test(1);
                    for (unsigned i = 0; i < N; ++i, test<<=1) {
                        counts[i] = std::count_if(group.begin(), group.end(), [&test](option& c) { return (c & test).to_ulong(); });
                    }
                }

                // build mask of singletons
                option singletons;
                {
                    option test(1);
                    for (unsigned i = 0; i < N; ++i, test<<=1)
                        if (counts[i] == 1)
                            singletons |= test;
                }

        bool effect = false;
                option non_singletons = ~singletons;
                for (auto& c : group) {
                    if ((c & singletons).any() && (c & non_singletons).any()) {
                        effect = true;
                        c &= singletons;
                    }
                }

        return effect;
      };

      for (bool effect = true; effect;) {
        effect = false;
        for (size_t ri = 0; ri<N; ++ri) {
          if ((effect |= isolate(row(ri))) && s_debug) {
            std::cout << "EXC at row " << ri << " effect:\n";
            dump();
          }
        }
        for (size_t ci = 0; ci<N; ++ci) {
          if ((effect |= isolate(col(ci))) && s_debug) {
            std::cout << "EXC at col " << ci << " effect:\n";
            dump();
          }
        }
            }

      return false;
    }

    bool solve_isolated_groups() {
      auto isolate = [](auto& cell, auto&& group) {
        bool effect = false;
        if (std::count(group.begin(), group.end(), cell) + 0ul == cell.count()) {
          for (auto& other : group) {
            if (other != cell) {
              if ((other & cell).count()) {
                if (s_debug) {
                  if (!effect)
                    std::cout << " - exclusive group of " << cell.count() << " times " << cell << "\n";
                  std::cout << "   -> affecting other cell from " << other << " to " << (other & ~cell) << "\n";
                }
                effect = true;
                other &= ~cell;
              }
            }
          }
        }
        return effect;
      };

      for (bool effect = true; effect;) {
        effect = false;
        for (size_t ri = 0; ri<N; ++ri) {
          auto& all = row(ri);
          bool local_effect = false;
          if (s_debug) std::cout << "At row " << ri << "\n";
          for (auto& c : all) local_effect |= isolate(c, all);

          if (s_debug && local_effect) {
            std::cout << "At row " << ri << " effect:\n";
            dump();
          }

          effect |= local_effect;
        }
        for (size_t ci = 0; ci<N; ++ci) {
          auto all = col(ci);
          bool local_effect = false;
          if (s_debug) std::cout << "At col " << ci << "\n";
          for (auto& c : all) local_effect |= isolate(c, all);

          if (s_debug && local_effect) {
            std::cout << "At col " << ci << " effect:\n";
            dump();
          }

          effect |= local_effect;
        }
        if (s_debug && effect) { std::cout << "REDUCTION RUN\n"; dump(); }
        return effect;
      }
      return false;
    }

    bool eliminate_hinted_skylines() {
      auto eliminate = [=](auto& clues, auto&& actual, std::string caption) {
        auto _elim = [](clue hint, auto&& actual, auto index_order, std::string caption) {
          if (!hint) return false;
          bool effect = false;

          auto range = solutionspace.equal_range(hint);
          if (s_debug) std::cout << caption << ": solutionspace is " << solutionspace.size() << " entries, hinted " << hint << ": " << std::distance(range.first, range.second) << "\n";

          std::set<seq const*> viable;
          for (; range.first!=range.second; ++range.first) {
            auto& candidate = range.first->second;
            //auto htm = [](height h) { return option{hint_to_mask(h)}; };
            //std::cout
              //<< " *** next candidate "
              //<< "{" << htm(candidate[0]) << "," << htm(candidate[1]) << "," << htm(candidate[2]) << "," << htm(candidate[3]) << "}\n";
            bool isviable = true;

            for(auto i=0u; i<N && isviable; ++i)
            {
              auto& actual_cell = actual[index_order(i)];
              //std::cout << "Matching index " << i << " actual_cell " << actual_cell << " against candidate " << option{hint_to_mask(candidate[i])} << "\n";
              //std::cout << "Matching index " << i << " actual_cell " << actual_cell.to_ulong() << " against candidate " << hint_to_mask(candidate[i]) << "\n";
              isviable &= !!(actual_cell.to_ulong() & hint_to_mask(candidate[i])); 
            }

            //std::cout << (isviable?"VIABLE":"NOT VIABLE") << "\n";

            if (isviable)
              viable.insert(&candidate);
          }

          if (viable.empty())
            return effect; // TODO THROW

          if (s_debug) std::cout << caption << ": There are " << viable.size() << " viable matches (for clue " << hint << ") in solutionspace\n";

          auto room = std::accumulate(begin(viable), end(viable), option_seq{}, 
              [](option_seq accum, seq const*s) {
                for(auto i=0u; i<N; ++i) accum[i] |= hint_to_mask((*s)[i]);
                return accum;
              });

          if (s_debug) std::cout << caption << ": Combined room remaining: " 
            << room[0] << ", " << room[1] << ", " << room[2] << ", " << room[3] << ", " << room[4] << ", " << room[5] << ", " << room[6] << "\n";

          for(auto i=0u; i<N; ++i) {
            auto& cell = actual[index_order(i)];
            auto newval = cell & room[i];
            if (newval != cell) {
              effect = true;
              cell = newval;
            }
          }

          return effect;
        };

        bool effect = false;
        effect |= _elim(clues.forward, actual, forward, caption + " (FWD)");
        //std::cout << "FORWARD ELIMINATED\n"; dump();
        effect |= _elim(clues.backward, actual, reverse, caption + " (BCK)");
        //std::cout << "BACKWARD ELIMINATED\n"; dump();
        return effect;
      };

      bool effect = false;
      for (size_t ri = 0; ri<N; ++ri) {
        if (eliminate(rowclues.at(ri), row(ri), "Row #" + std::to_string(ri))) {
          effect = true;
          if (s_debug) { std::cout << "ELIMINATED FOR ROW " << ri << "\n"; dump(); }
        }
      }
      for (size_t ci = 0; ci<N; ++ci) {
        if (eliminate(colclues.at(ci), col(ci), "Col #" + std::to_string(ci))) {
          effect |= true;
          if (s_debug) { std::cout << "ELIMINATED FOR COL " << ci << "\n"; dump(); }
        }
      }

      return effect;
    }

    void solve() {
      preapply_hints();

      for (bool effect = true; effect;) {
        effect = false;
        effect |= solve_exclusive_options();
        effect |= solve_isolated_groups();
        effect |= eliminate_hinted_skylines(); // using hints again
      }
      if (s_debug) { dump(); }
    }

    void dump() {
      std::cout << "======== rows\n";
      std::cout << "     ";
      for (size_t ci = 0; ci<N; ++ci) 
        std::cout << std::setw(N+1) << ("[" + std::to_string(colclues.at(ci).forward) + "]     ");
      std::cout << "\n";
      for (size_t ri = 0; ri<N; ++ri)
      {
        std::cout << "[" << rowclues.at(ri).forward << "]  ";
        for(auto& cell : row(ri)) std::cout << cell << " ";
        std::cout << "  [" << rowclues.at(ri).backward << "]\n";
      }
      std::cout << "     ";
      for (size_t ci = 0; ci<N; ++ci) 
        std::cout << std::setw(N+1) << ("[" + std::to_string(colclues.at(ci).backward) + "]     ");
      std::cout << "\n";
    }

    option_seq&     row(size_t i)     { return field.at(i); }
    option_seq const& row(size_t i) const { return field.at(i); }

    struct colproxy {
      puzzle* _p;
      size_t _col;

      size_t size() const { return N; }

      option&     at    (size_t i)     { return _p->row(i).at(_col); }
      option const& at    (size_t i) const { return _p->row(i).at(_col); }
      option&     operator[](size_t i)     { return _p->row(i).at(_col); }
      option const& operator[](size_t i) const { return _p->row(i).at(_col); }

      struct it : std::iterator<std::bidirectional_iterator_tag, option> {
        it(colproxy* p, size_t i) : _p(p), _i(i){}

        using difference_type = std::ptrdiff_t;
        colproxy* _p;
        size_t _i;

        it& operator++() { ++_i; return *this; }
        it& operator--() { --_i; return *this; }
        bool operator==(it const& other) const { return _p == other._p && _i == other._i; }
        bool operator!=(it const& other) const { return _p != other._p || _i != other._i; }
        option& operator*() { return _p->at(_i); }
        option* operator->() { return &_p->at(_i); }
      };

      it begin() { return {this, 0}; }
      it end()   { return {this, N}; }
    };

    colproxy col(size_t i) { return { this, i }; }
  };
}

height decode(option const& cell) {
  switch(cell.to_ulong()) {
    case 1ul<<0: return h1;
    case 1ul<<1: return h2;
    case 1ul<<2: return h3;
    case 1ul<<3: return h4;
    case 1ul<<4: return h5;
    case 1ul<<5: return h6;
    case 1ul<<6: return h7;
    default: return none;
  }
}

std::vector<std::vector<int>> SolvePuzzle(std::vector<int> const& clues) {
  if (s_print_challenge) {
    std::cout << "{";
    for (auto i : clues) std::cout << i << ",";
    std::cout << "}\n";
  }

  using namespace utility;
  puzzle p(clues);
  p.solve();
  std::vector<std::vector<int> > r;

  for (auto& row : p.field) {
    r.emplace_back();
    for (auto& cell : row) {
      r.back().emplace_back(decode(cell));
    }
  }
  return r;
}
_______________________________________________________________________
#include <vector>
using namespace std;
typedef __uint64_t ui64;

// Permutations and masks are 64 bit numbers, with 8 bits for each cell.  1 = could be, 0 = is not
#define GET_MASK_ELEMENT( mask, n ) (((mask) >> ((ui64)8*(n)))&0xff)
#define SET_MASK_ELEMENT( mask, n, elem )  ((mask & ~((ui64)0xff << ((ui64)8*(n)))) | ((((ui64)elem) & 0xff) << ((ui64)8*((ui64)n))))

struct Permutation
{
   ui64 Mask;  // 00000000 for each cell, with a 1 in the (1<<number) 
   int LeftClue;
   int RightClue;
   int ClueMask;
};

static const int Size = 7;

Permutation Permutations[5040];
int         NextPermutationIndex = 0;

void FillPermutations( ui64 mask, int currentN )
{
  if (currentN == Size)
  {
    Permutations[NextPermutationIndex].Mask = mask;
    Permutations[NextPermutationIndex].LeftClue = 0;
    Permutations[NextPermutationIndex].RightClue = 0;
    ui64 LastMax = 0; 
    
    
    for (int i = 0; i < Size; i++)
    {
      ui64 elem = GET_MASK_ELEMENT(mask, i);
      if (elem >= LastMax) { LastMax = elem; Permutations[NextPermutationIndex].LeftClue++; }      
    }

    LastMax = 0;
    for (int i = Size-1; i >= 0; i--)
    {
      ui64 elem = GET_MASK_ELEMENT(mask, i);
      if (elem >= LastMax) { LastMax = elem; Permutations[NextPermutationIndex].RightClue++; }      
    }      
    
    NextPermutationIndex++;
    return;
  }

  for (int i = 0; i < Size; i++)
  {    
    int j = 0;
    for (j = 0; j < currentN; j++)
    {      
        if ( (1<<i) == GET_MASK_ELEMENT(mask, j)) break;        
    }
    // already have #i in the mask    
    if (j != currentN) continue;
    
    FillPermutations( SET_MASK_ELEMENT(mask, currentN, (1<<i)), currentN+1);    
  }
}

int boardClues[Size*2][2]; // clues for each of the Size*2 lines
int remainingPerms[Size*2];

bool ReconcileBoard(ui64 *board)
{
  bool moreToReconcile = true;
 
  while (moreToReconcile)
  {
    moreToReconcile = false;
   
    // reconcile the board based on the competing masks
    for (int i = 0; i < Size; i++)
      for (int j = 0; j < Size; j++)
      {
          ui64 mask1 = GET_MASK_ELEMENT(board[i], j);
          ui64 mask2 = GET_MASK_ELEMENT(board[j + Size], i);        
          ui64 combinedMask = mask1 & mask2;
          
          if (combinedMask == 0)
          { 
               // unsolvable
               return false; 
          }         
            
          board[i] = SET_MASK_ELEMENT( board[i], j, combinedMask );
          board[j + Size] = SET_MASK_ELEMENT( board[j + Size], i, combinedMask );        
      }
    
    // reconcile based on the clues and permutations
    for (int i = 0; i < Size * 2; i++) 
    {
      remainingPerms[i] = 0;
      ui64 maskReplace = 0;
      
      for (int j = 0; j < NextPermutationIndex; j++)
      {
        if (((Permutations[j].Mask & ~board[i]) == 0) &&
            ((boardClues[i][0] == 0) || (boardClues[i][0] == Permutations[j].LeftClue)) &&
            ((boardClues[i][1] == 0) || (boardClues[i][1] == Permutations[j].RightClue)))
        {
           remainingPerms[i]++;
           maskReplace |= Permutations[j].Mask;
        }
      }
      
      if (remainingPerms[i] == 0)
      {
          // no solution!
          return false;
      }
         
      if ( board[i] != maskReplace ) 
      {
        moreToReconcile = true;
        board[i] = maskReplace;
      }
      
    }
  }
  
  // still a valid board left!
  return true;
}

int FindNextRecursionLine()
{
  int mostRestrictedIndex = 0;
  int mostRestrictedAvailPerms = remainingPerms[0];
  
  for (int i = 1; i < Size*2; i++)
  {
    if ( remainingPerms[i] < mostRestrictedAvailPerms)
    {
      mostRestrictedIndex = i;
      mostRestrictedAvailPerms = remainingPerms[i];
    }
  }
  
  return mostRestrictedIndex;
}



vector<vector<int>> SolvePuzzle(const vector<int> &clues)
{
   ui64 board[Size*2];
   if (NextPermutationIndex == 0)  FillPermutations(0,0);
   for (int i = 0; i < Size*2; i++)  board[i] = (ui64)0xffffffffffffffff;
   for (int i = 0; i < Size*2; i++) boardClues[i][0] = boardClues[i][1] = 0;
   for (int i = 0; i < Size*2; i++) remainingPerms[i] = NextPermutationIndex;
   for (int i = 0; i < Size; i++)
   {
     boardClues[i][0] = clues[i];
     boardClues[i][1] = clues[Size*3-1-i];
     boardClues[Size+i][0] = clues[Size*4-1-i];
     boardClues[Size+i][1] = clues[Size+i];
   }   
   
  // Interestingly, we never have to recursively solve
  // Because there are only single solutions and they are made to solve by humans, 
  // We can just logic it to the end (reconciling and iterating until it stabilizes)
   if (ReconcileBoard(board) == false)
       return {};
   
   // convert our fast bitmask structure back into a board
   vector<vector<int>> rtn;  
   for (int i = 0; i < Size; i++)
   {
      vector<int> line;
      for (int j = 0; j < Size; j++)
      {
          int elem = GET_MASK_ELEMENT(board[i+Size], j); 
          int k = 0;
          
          // quick and dirty log2
          for (k = 0; k < Size; k++) if ((elem & (1 << k)) == elem) break;        
          
          line.push_back(k+1);        
      }      
      rtn.push_back(line);
   }      
  
   return rtn;
}
_________________________________________________________
#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <map>
#include <vector>

const int N = 7;
const int SIDES = 4;
const int MASK = (1 << N) - 1;
const int s[SIDES * N] = { 0,1,2,3,4,5,6,6,13,20,27,34,41,48,48,47,46,45,44,43,42,42,35,28,21,14,7,0 };
const int inc[SIDES * N] = { 7,7,7,7,7,7,7,-1,-1,-1,-1,-1,-1,-1,-7,-7,-7,-7,-7,-7,-7,1,1,1,1,1,1,1 };
int possible[N * N], results[N][N];
bool vis[N * N];
std::vector<int> cl;

void print(const std::vector<std::vector<int>>& v) {
  for (auto& x : v) {
    for (auto& y : x) {
      std::cout << y << " ";
    }
    std::cout << "\n";
  }
  std::cout << "\n--------------\n";
}

void set_value(int x, int v) {
  int m = MASK ^ (1 << v);
  int s_row = x - x % N;
  int s_col = x % N;
  for (int i = 0; i < N; i++) {
    possible[s_row + i] &= m;
    possible[s_col + i * N] &= m;
  }
  possible[x] = 1 << v;
}

int check_unique() {
  int n_decides = 0;
  for (int i = 0; i < SIDES / 2 * N; i++) {
    std::map<int, std::vector<int> > possible_indices;
    for (int j = s[i], k = 0; k < N; j += inc[i], k++) {
      for (int l = 0; l < N; l++)
        if ((1 << l) & possible[j]) {
          possible_indices[l].push_back(j);
        }
    }

    for (auto const& iter : possible_indices) {
      int val = iter.first;
      if (iter.second.size() == 1) {
        int idx = iter.second[0];
        if (possible[idx] != (1 << val)) {
          n_decides++;
          set_value(idx, val);
        }
      }
    }
  }
  return n_decides;
}

int f() {
  int cnt = 0;
  for (int i = 0; i < SIDES * N; i++) {
    if (cl[i] == 2) {
      int mask = MASK;
      for (int l = N - 1; l >= 0; l--) {
        int m = (1 << l) & possible[s[i]];
        mask ^= 1 << l;
        if (m) break;
      }

      for (int j = s[i] + inc[i], k = 1; k < N; j += inc[i], k++) {
        int m = (1 << (N - 1)) & possible[j];
        if (m) break;
        if ((possible[j] | mask) != mask) {
          possible[j] &= mask;
          cnt++;
        }
      }
    }
  }
  return cnt;
}

int count_possible(int val) {
  int n = 0;
  while (val) {
    n += val & 1;
    val >>= 1;
  }
  return n;
}

bool valid() {
  for (int i = 0; i < SIDES * N; i++) {
    if (cl[i] == 0) continue;

    bool is_decided = true;
    for (int j = s[i], k = 0; k < N; j += inc[i], k++) {
      if (count_possible(possible[j]) != 1) {
        is_decided = false;
        break;
      }
    }

    if (is_decided) {
      int largest = 0, n_clue = 0;
      for (int j = s[i], k = 0; k < N; j += inc[i], k++) {
        if (largest < possible[j]) {
          n_clue++;
          largest = possible[j];
        }
      }
      if (n_clue != cl[i]) return false;
    }
  }

  return true;
}

void write_results() {
  for (int i = 0; i < N * N; i++) {
    int x = i / N, y = i % N;
    for (int j = 0; j < N; j++) {
      if ((1 << j) == possible[i]) {
        results[x][y] = j + 1;
        break;
      }
    }
  }
}

bool dfs(int idx) {
  int i = -1, tmp = 10000;
  for (int _i = 0; _i < N * N; _i++) {
    int c = count_possible(possible[_i]);
    if (tmp > c && !vis[_i]) {
      tmp = c;
      i = _i;
    }
  }

  if (i == -1) {
    if (valid()) {
      write_results();
      return true;
    }
    return false;
  }

  int possible_bak[N * N];
  memcpy(possible_bak, possible, sizeof(int) * N * N);

  for (int j = N - 1; j >= 0; j--) {

    int m = (1 << j) & possible[i];
    if (m == 0) continue;

    vis[i] = true;
    set_value(i, j);
    bool found = false;
    if (valid()) {
      found = dfs(idx + 1);
    }
    vis[i] = false;
    memcpy(possible, possible_bak, sizeof(int) * N * N);
    if (found) {
      return true;
    }
  }
  return false;
}

void init() {
  for (int i = 0; i < N * N; i++) {
    possible[i] = MASK;
    vis[i] = true;
  }
}

void pre_process() {
  for (int i = 0; i < SIDES * N; i++) {
    if (cl[i] == 0) continue;
    for (int j = s[i], k = 0; k < N; j += inc[i], k++) {
      int m = MASK;
      for (int l = N + k - cl[i] + 1; l < N; l++) m ^= 1 << l;
      possible[j] &= m;
    }
  }

  while (check_unique() > 0);
  f();
}

std::vector< std::vector<int> > SolvePuzzle(const std::vector<int>& clues) {
  std::vector< std::vector<int> > r;
  init();
  cl = clues;

  pre_process();

  std::vector< std::pair<int, int> > idx_npos;
  for (int i = 0; i < N * N; i++) {
    int n_possible = count_possible(possible[i]);
    if (n_possible > 1) {
      vis[i] = false;
    }
  }

  dfs(0);

  for (int i = 0; i < N; i++) {
    std::vector<int> vec;
    for (int j = 0; j < N; j++) vec.push_back(results[i][j]);
    r.push_back(vec);
  }
  return r;
}
