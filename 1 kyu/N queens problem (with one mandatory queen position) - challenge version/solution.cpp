#include <string>
#include <utility>
#include <vector>
#include <random>

namespace nQueens
{

    std::string solveNQueens(int n, std::pair<int, int> mandatoryQueenCoordinates)
    {
      std::vector<int> X(2 * n, 0), Y(2 * n, 0);
      struct Col { int q = 0, dx = 0, dy = 0, x = 0, y = 0;};
      std::vector<Col> board(n);
      
      auto set_dx = [&] (int i, int _dx) {
        auto& col = board[i];
        col.dx = _dx;
        col.dy = n - 1 - _dx;
      };
      
      auto set_q = [&] (int i, int _q) {
        auto& col = board[i];
        col.q = _q;
        col.x  = col.q + col.dx;
        col.y  = col.q + col.dy;
        X[col.x]++;
        Y[col.y]++;
      };
      
      int quality = 0;
      
      auto correct = [&] (int i, int delta) {
        auto& col = board[i];
        if (X[col.x] > 1) quality -= X[col.x] - 1;
        X[col.x] += delta;
        if (X[col.x] > 1) quality += X[col.x] - 1;
        
        if (Y[col.y] > 1) quality -= Y[col.y] - 1;
        Y[col.y] += delta;
        if (Y[col.y] > 1) quality += Y[col.y] - 1;
      };
      
      auto change_q = [&] (int i, int _q) {
        auto& col = board[i];
        correct(i, -1);
        col.q = _q;
        col.x  = col.q + col.dx;
        col.y  = col.q + col.dy;
        correct(i, 1);
      };
      
      auto swap = [&] (int x, int y) {
        int old_x = board[x].q;
        change_q(x, board[y].q);
        change_q(y, old_x);
      };
      
      auto print = [&] (void) {
        std::string result(n * (n + 1), '.');
        for (unsigned i = n; i < result.size(); i += n + 1) result[i] = '\n';
        for (int i = 0; i < n; i ++) {
          result[board[i].q * (n + 1) + board[i].dx] = 'Q';
        }  
        return result;
      };
      
      set_dx(0, mandatoryQueenCoordinates.first);
      set_q (0, mandatoryQueenCoordinates.second);
      
      for (int i = 1, j = 0, k = 0; i < n; i++, j++, k++) {
        if (j == mandatoryQueenCoordinates.first)  j++;
        if (k == mandatoryQueenCoordinates.second) k++;
        set_dx(i, j);
        set_q(i, k);
      }
      
      for (int i = 0; i < 2 * n; i++) {
        if (X[i] > 1) quality += X[i] - 1;
        if (Y[i] > 1) quality += Y[i] - 1;
      }
      
      
      std::mt19937 engine;
      std::random_device device;
      engine.seed(device());
      std::uniform_int_distribution<int> figure(1, std::max(1, n - 1));
      std::uniform_real_distribution<float> distribution(0., 1.);
      
      float limit = 0.01 / n;
      int iMax = 100 * (n + 1000);
      for (auto i = 0; i < iMax; i ++) {
        if (quality == 0) return print();
        int x = figure(engine), y = figure(engine);
        if (x == y) continue;
        
        int old = quality;
        swap(x, y);
        if (quality > old && (distribution(engine) > limit)) swap(x, y);
      }
      
      return "";
    }
}


###################################
#include<algorithm>
#include<iostream>
#include<cstring>
#include<string>
#include<cstdio>
#include<cmath>
#include<ctime>
using namespace std;
#define clr(a) memset(a,0,sizeof(a))

namespace nQueens
{    

    int sn,mt[1010][1010],ps[1010],pm[1010],dpm[1010],stm[1010];char ans[2000010];
    bool gmp(int a,int b){
        return dpm[a-1]<dpm[b-1];
    }
    void gpm(int n,int r=-1,int c=-1){
        int i;for(i=0;i<n;++i)pm[i]=i+1,dpm[i]=rand();sort(pm,pm+n,gmp);
        if(r>=0){
            for(i=0;pm[i]!=r+1;++i);swap(pm[i],pm[c]);
        }
    }
    inline bool v2ck(int a,int b,int c,int d){return a==c||b==d||(abs(c-a)==abs(d-b));};
    
    void makeans(int n){
        int i,j,k,d,t;for(clr(ans),i=d=0;i<n;++i,ans[d++]='\n')for(j=0;j<n;++j){
            ans[d++]=mt[i][j]?'Q':'.';
        }
    }
    
    int __cl(int r,int c,int dt,bool zt,bool lz,int n){
        int i,j,k,d,t,rs=0;bool fg=0;if(lz)mt[r][c]=zt?0:dt,ps[dt]=zt?-1:r;
        for(i=1;i<=n;++i)if(ps[i]>=0&&i!=dt&&v2ck(r,c,ps[i],i-1)){
            if(!stm[i]&&!zt)++rs;
            if(stm[i]==1&&zt)--rs;
            if(lz&&zt)stm[i]--,stm[dt]--;
            if(lz&&!zt)stm[i]++,stm[dt]++;
            fg=1;
        }
        if(fg){
            rs+=zt?-1:1;
        }
        return rs;
    }
    
    string _cl(int n,int dq=-1,int dp=-1){
        int i,j,k,d,t,q,o,h,zn,qn,dqn=10,dn=50*n;clr(mt);
        for(sn=n,qn=1;sn&&qn<dqn;++qn){
            for(i=1;i<=n;stm[i++]=0)mt[max(0,ps[i])][i-1]=0;
            for(i=1;i<=n;ps[i++]=-1);
            for(gpm(n,dq,dp),sn=0,i=1;i<=n;++i){
                t=pm[i-1]-1;sn+=__cl(t,i-1,i,0,1,n),ps[i]=t;
            }
            for(zn=1;sn&&zn<=dn;++zn){
                for(gpm(n),i=0;i<n;++i){
                    if(pm[i]-1==dp)continue;
                    if(stm[pm[i]])break;
                }
                if(n==i)break;
                i=pm[i];sn+=__cl(q=ps[i],i-1,i,1,1,n);
                for(gpm(n),t=n+1,j=0;j<n;++j){
                    if(q==pm[j]-1)continue;
                    d=__cl(pm[j]-1,i-1,i,0,0,n);
                    if(d<t)t=d,k=pm[j]-1;
                }
                sn+=__cl(k,i-1,i,0,1,n);
            }
        }
        if(qn<dqn)makeans(n);else{ans[0]=0;}
        return (string)ans;
    };    
      
    std::string solveNQueens(int n, std::pair<int, int> mandatoryQueenCoordinates)
    {
      return _cl(n,mandatoryQueenCoordinates.second,mandatoryQueenCoordinates.first);
    }
}

##################################
#include <string>
#include <algorithm>
#include <array>
#include <numeric>
#include <vector>
#include <unordered_map>
#include <ctime>

// Adaptation of the algorithm from the paper "Fast Search Algorithms for the N-Queens Problem"
// https://pdfs.semanticscholar.org/79d2/fa13d4a5cfc02ff6936b6083bb620e4e0ce1.pdf

namespace nQueens
{
  class QS2
  {
  public:
    QS2(int n, int fixedRow, int fixedCol) : n(n), fixedRow(fixedRow), queens(n), diags(4 * n), attack(n)
    {
      std::iota(queens.begin(), queens.end(), 0);
      queens[fixedRow] = fixedCol;
      queens[fixedCol] = fixedRow;
    }

    bool search()
    {
      permutation();
      int collisions = computeCollisions();
      if (collisions <= 0) return true;
      int limit = (int)(c1 * collisions);
      int numberOfAttacks = computeAttacks();
      for (int r = 0; r <= c2 * n; r += numberOfAttacks)
      {
        for (int k = 0; k < numberOfAttacks; k++)
        {
          const int i = attack[k];
          const int j = std::rand() % n;
          if (i == fixedRow || j == fixedRow || i == j) continue;
          const int dc = swapCollisions(i, j);
          if (dc < 0)
          {
            performSwap(i, j);
            collisions += dc;
            if (collisions <= 0) return true;
            if (collisions < limit)
            {
              limit = (int)(c1 * collisions);
              numberOfAttacks = computeAttacks();
            }
          }
        }
      }
      return false;
    }

    std::string findSolution()
    {
      while (!search());
      return std::accumulate(queens.begin(), queens.end(), std::string(""), [&](std::string v, int q) {
        return std::move(v) + std::string(q, '.') + "Q" + std::string(n - q - 1, '.') + "\n";
      });
    }

  private:
    inline int dn(int i, int j) const
    {
      return i + queens[j];
    }

    inline int dp(int i, int j) const
    {
      return i - queens[j] + 3 * n;
    }

    void permutation()
    {
      for (int i = n - 1; i > 0; i--)
      {
        int j = std::rand() % i;
        if (i != fixedRow && j != fixedRow && i != j)
        {
          std::swap(queens[i], queens[j]);
        }
      }
    }

    int computeCollisions()
    {
      std::fill(diags.begin(), diags.end(), 0);
      int collisions = 0;
      for (int i = 0; i < n; i++)
      {
        if (++diags[dn(i, i)] >= 2) collisions++;
        if (++diags[dp(i, i)] >= 2) collisions++;
      }
      return collisions;
    }

    int computeAttacks()
    {
      int attacks = 0;
      for (int i = 0; i < n; i++)
      {
        if (diags[dn(i, i)] > 1 || diags[dp(i, i)] > 1)
        {
          attack[attacks++] = i;
        }
      }
      return attacks;
    }

    int swapCollisions(int i, int j) const
    {
      if (i == j) return 0;
      int c = 0;
      const int i1[] = {dn(i, i), dp(i, i), dn(j, j), dp(j, j)};
      const int i2[] = {dn(i, j), dp(i, j), dn(j, i), dp(j, i)};
      for (int k = 0; k < 4; k++)
      {
        if (diags[i1[k]] >= 2) c--;
        if (diags[i2[k]] >= 1) c++;
      }
      if (i1[0] == i1[2] && diags[i1[0]] == 2) c++;
      if (i1[1] == i1[3] && diags[i1[1]] == 2) c++;
      if (i2[0] == i2[2] && diags[i2[0]] == 0) c++;
      if (i2[1] == i2[3] && diags[i2[1]] == 0) c++;
      return c;
    }

    void performSwap(int i, int j)
    {
      if (i == j) return;
      --diags[dn(i, i)];
      --diags[dp(i, i)];
      --diags[dn(j, j)];
      --diags[dp(j, j)];
      std::swap(queens[i], queens[j]);
      ++diags[dn(i, i)];
      ++diags[dp(i, i)];
      ++diags[dn(j, j)];
      ++diags[dp(j, j)];
    }

    const int n;
    const int fixedRow;
    std::vector<int> queens;
    std::vector<int> diags;
    std::vector<int> attack;
    const double c1 = 0.45;
    const int c2 = 32;
  };

  const std::unordered_map<int, std::vector<std::pair<int, int>>> noSolutions {
    {4, {{0, 0}, {0, 3}, {1, 1}, {1, 2}, {2, 1}, {2, 2}, {3, 0}, {3, 3}}},
    {6, {{0, 0}, {0, 5}, {1, 1}, {1, 4}, {2, 2}, {2, 3}, {3, 2}, {3, 3}, {4, 1}, {4, 4}, {5, 0}, {5, 5}}}
  };

  std::string solveNQueens(const int n, std::pair<int, int> mandatoryQueenCoordinates) 
  {
    auto it = noSolutions.find(n);
    if (it != noSolutions.end() && std::find(it->second.begin(), it->second.end(), mandatoryQueenCoordinates) != it->second.end()) 
    {
      return "";
    }
    if (n == 2 || n == 3) return "";

    QS2 qs2(n, mandatoryQueenCoordinates.second, mandatoryQueenCoordinates.first);
    return qs2.findSolution();
  }
}


#########################################
using namespace std;
#define MAX_SIZE 1000
#include <bits/stdc++.h>
int n;
int board[MAX_SIZE];
int label[MAX_SIZE];
int ru[MAX_SIZE * 2];
int rd[MAX_SIZE * 2];
int ii, jj;
void RandArray()
{
    random_shuffle(board, board + n);
    for (int i = 0; i < n; i++)
    {
        if (board[i] == jj)
        {
            swap(board[ii], board[i]);
            break;
        }
    }
}
int Conflict()
{
    int i, r = 0;
    memset(ru, 0, sizeof(ru));
    memset(rd, 0, sizeof(rd));
    for (i = 0; i < n; i++)
    {
        ru[board[i] - i + n]++;
        rd[board[i] + i]++;
        if (ru[board[i] - i + n] > 1)
            r++;
        if (rd[board[i] + i] > 1)
            r++;
    }
    return r;
}
namespace nQueens
{
    int i, j, temp, now, t1, t2, fnow;
    std::string solveNQueens(int nn, std::pair<int, int> Q)
    {
        int T;
        n = nn;
        for (int i = 0; i < n; i++)
            board[i] = i;
        if (n <= 200)
            T = 100;
        else if (n <= 500)
            T = 10;
        else
            T = 1;
        jj = Q.first;
        ii = Q.second;
        string ans;
        while (T--)
        {
        E:
            RandArray();
            now = Conflict();
            if (now >
                ((n <= 500) ? (1e9)
                            : (n <= 600 ? (300)
                                        : (n <= 900 ? (n / 2 - 27)
                                                    : (450)))))
                goto E;
        next:
            if (now == 0)
                goto over;
            for (i = 0; i < n - 1; i++)
            {
                if (i == ii)
                    continue;
                for (j = i + 1; j < n; j++)
                {
                    if (j == ii)
                        continue;
                    fnow = now;
                    ru[board[i] - i + n]--;
                    if (ru[board[i] - i + n])
                        fnow--;
                    ru[board[j] - j + n]--;
                    if (ru[board[j] - j + n])
                        fnow--;
                    ru[board[i] - j + n]++;
                    if (ru[board[i] - j + n] != 1)
                        fnow++;
                    ru[board[j] - i + n]++;
                    if (ru[board[j] - i + n] != 1)
                        fnow++;
                    rd[board[i] + i]--;
                    if (rd[board[i] + i])
                        fnow--;
                    rd[board[j] + j]--;
                    if (rd[board[j] + j])
                        fnow--;
                    rd[board[i] + j]++;
                    if (rd[board[i] + j] != 1)
                        fnow++;
                    rd[board[j] + i]++;
                    if (rd[board[j] + i] != 1)
                        fnow++;
                    swap(board[i], board[j]);
                    if (fnow < now)
                    {
                        now = fnow;
                        goto next;
                    }
                    swap(board[i], board[j]);
                    ru[board[i] - i + n]++;
                    ru[board[j] - j + n]++;
                    ru[board[i] - j + n]--;
                    ru[board[j] - i + n]--;
                    rd[board[i] + i]++;
                    rd[board[j] + j]++;
                    rd[board[i] + j]--;
                    rd[board[j] + i]--;
                }
            }
        }
        if (T <= 0)
            return "";
    over:
        for (i = 0; i < n; i++)
        {
            for (j = 0; j < n; j++)
            {
                if (board[i] == j)
                    ans += 'Q';
                else
                    ans += '.';
            }
            ans += '\n';
        }
        return ans;
    }
}


#####################################
#include <string>
#include <utility>
#include <vector>
#include <random>
#include <set>
#include <bits/stdc++.h>

namespace nQueens {
  using namespace std;
  const int MAXN = 2e3 + 10;
  int s[MAXN];
  set<int> f1[MAXN], f2[MAXN];
  int total_collision, N;
  const int kCntLimit = 10;
  
  void remove(int x) {
    f1[s[x] + N - x].erase(x);
    if (f1[s[x] + N - x].size() != 0) total_collision--;
    f2[s[x] + x].erase(x);
    if (f2[s[x] + x].size() != 0) total_collision--;
  }

  void add(int x) {
    if (f1[s[x] + N - x].size() != 0) total_collision++;
    f1[s[x] + N - x].insert(x);
    if (f2[s[x] + x].size() != 0) total_collision++;
    f2[s[x] + x].insert(x);
  }
  
  bool solve(int n, int x, int y) {
    for (int i = 1; i <= n; i++) s[i] = i;
    total_collision = 0;
    random_shuffle(s + 1, s + n + 1);
    for (int i = 1; i <= n; i++) {
      if (s[i] == y && i != x) {
        swap(s[i], s[x]);
      }
    }
    // 1 - n, n - 1 -> 1, 2 * n - 1
    // 2,     2 * n -> 1, 2 * n - 1
    for (int i = 1; i <= 2 * n; i++) {
      f1[i].clear(); f2[i].clear();
    }
    for (int i = 1; i <= n; i++) {
      f1[s[i] + n - i].insert(i);
      f2[s[i] + i].insert(i);
    }
    for (int i = 1; i <= 2 * n; i++) {
      if (f1[i].size() > 1) total_collision += f1[i].size() - 1;
      if (f2[i].size() > 1) total_collision += f2[i].size() - 1;
    }
    for (int cnt = 0; cnt < kCntLimit && total_collision > 0; cnt++) {
      int swap_count = 0;
      for (int i = 1; i <= n; i++) if (i != x) {
        for (int j = i + 1; j <= n; j++) if (j != x) {
          int tmp_collision = total_collision;
          remove(i); remove(j);
          swap(s[i], s[j]);
          add(i); add(j);
          if (total_collision < tmp_collision) 
            swap_count++;
          else {
            remove(i); remove(j);
            swap(s[i], s[j]);
            add(i); add(j);
          }
        }
      }
      // cout << cnt << ' ' << total_collision << ' ' << swap_count << endl;
      if (swap_count == 0) {
        break;
      }
    }
    return total_collision == 0;
  }
  
  std::string solveNQueens(int n, std::pair<int, int> mandatoryQueenCoordinates) {
    srand(time(0));
    N = n;
    int x = mandatoryQueenCoordinates.first + 1, y = mandatoryQueenCoordinates.second + 1;
    for (int i = 1; i <= 50; i++) {
      if (solve(n, x, y)) {
        std::string res;
        for (int p = 1; p <= n; p++) {
          for (int q = 1; q <= n; q++) {
            if (s[q] == p) res.push_back('Q');
            else res.push_back('.');
          }
          res.push_back('\n');
        }
        return res;
      }
    }
    return "";
  }
}


########################################
#include <vector>
#include <random>
#include <algorithm>

using namespace std;

random_device rd;  //Will be used to obtain a seed for the random number engine
mt19937 gen(rd()); //Standard mersenne_twister_engine seeded with rd()

class Qdata {
        vector<int> rows, d1, d2;
        int N;
    public :
        Qdata (int size) {
            N = size;
            rows.resize(N), d1.resize (2 * N - 1), d2.resize (2 * N - 1);
        }

        void reset (vector<int> board) {

            fill (begin(rows), end(rows), 0);
            fill (begin(d1), end(d1), 0);
            fill (begin(d2), end(d2), 0);

            for (int i = 0; i < N; i++) {
                rows[board[i]]++;
                d1[N + i - board[i] - 1]++;
                d2[i + board[i]]++;
            }
        }

        int attack (int x, int y) { return rows[y] + d1[N + x - y - 1] + d2[x + y]; }
      };

namespace nQueens {
    string format (vector<int> &board) {
        string os;
        const int end = board.size();
        for (int y = 0; y < end; y++) {
            for (int x = 0; x < end; x++) {
                os += (board[x] == y) ? 'Q' : '.';
            }
            os += '\n';
        }
        return os;
    }
    vector<int> generate (int N) {
        vector<int> board (N);

        while (N-->0) board[N] = N;

        shuffle (begin(board), end(board), gen);

        return board;
    }

    int rnd_walk (const vector<int> &hist, int val) {
        vector<int> V;

        for (size_t i = 0; i < hist.size(); i++)
        if (hist[i] == val)
        V.push_back (i);

        uniform_int_distribution<> dist (0, V.size() - 1);

        return V[dist(gen)];
      }
    vector<int> min_conflict (const int N, pair<int,int> pos) {

        int x, y, max_iter  = N * 50;
        int cnt, sum, val;
        vector<int> board(N), hist (N);
        Qdata actual (N);

        board = generate (N);
        board[pos.first] = pos.second;
        actual.reset (board);
        
        while (max_iter-->0) {

            sum = 0, val = 0;
            
            for (x = 0; x < N; x++) {
                cnt = (x == pos.first) ? 0 : actual.attack (x, board[x]) - 3;

                val = max (val, cnt);
                hist[x] = cnt;
                sum += cnt;
            }
            
            if (sum == 0) return board;
            
            x = rnd_walk (hist, val);
            val = N;
            for (y = 0; y < N; y++) {
                cnt = actual.attack (x, y);

                val = min (val, cnt);
                hist[y] = cnt;
            }
            
            y = rnd_walk (hist, val);
            
            board[x] = y;
            actual.reset(board);
        }
        
        return {};
    }

    string solveNQueens (int N, pair<int,int> pos) {

          int index = 4;
          vector<int> res;

          while (index-->0) {
              res = min_conflict (N, pos);
              if (res.size() != 0)
                  return format(res);
          }
          
          return "";
      }
      
}


##########################################
#include<bits/stdc++.h>
using namespace std;
#define clr(a) memset(a,0,sizeof(a))
namespace nQueens
{    
    int sn,mt[1010][1010],ps[1010],pm[1010],dpm[1010],stm[1010];char ans[2000010];
    bool gmp(int a,int b){
        return dpm[a-1]<dpm[b-1];
    }
    void gpm(int n,int r=-1,int c=-1){
        int i;for(i=0;i<n;++i)pm[i]=i+1,dpm[i]=rand();sort(pm,pm+n,gmp);
        if(r>=0){
            for(i=0;pm[i]!=r+1;++i);
            swap(pm[i],pm[c]);
        }
    }
    inline bool v2ck(int a,int b,int c,int d){return a==c||b==d||(abs(c-a)==abs(d-b));};
    void makeans(int n){
        int i,j,k,d,t;for(clr(ans),i=d=0;i<n;++i,ans[d++]='\n')for(j=0;j<n;++j){
            ans[d++]=mt[i][j]?'Q':'.';
        }
    }
    int __cl(int r,int c,int dt,bool zt,bool lz,int n){
        int i,j,k,d,t,rs=0;bool fg=0;if(lz)mt[r][c]=zt?0:dt,ps[dt]=zt?-1:r;
        for(i=1;i<=n;++i){
          if(ps[i]>=0&&i!=dt&&v2ck(r,c,ps[i],i-1)){
            if(!stm[i]&&!zt)
              ++rs;
            if(stm[i]==1&&zt)
              --rs;
            if(lz&&zt){
              stm[i]--;
              stm[dt]--;
            }
            if(lz&&!zt){
              stm[i]++;
              stm[dt]++;
            }
            fg=1;
           }
        }
        if(fg){
            rs+=zt?-1:1;
        }
        return rs;
    }
    string _cl(int n,int dq=-1,int dp=-1){
        int i,j,k,d,t,q,o,h,zn,qn,dqn=10,dn=50*n;clr(mt);
        for(sn=n,qn=1;sn&&qn<dqn;++qn){
            for(i=1;i<=n;stm[i++]=0)mt[max(0,ps[i])][i-1]=0;
            for(i=1;i<=n;ps[i++]=-1);
            for(gpm(n,dq,dp),sn=0,i=1;i<=n;++i){
                t=pm[i-1]-1;sn+=__cl(t,i-1,i,0,1,n),ps[i]=t;
            }
            for(zn=1;sn&&zn<=dn;++zn){
                for(gpm(n),i=0;i<n;++i){
                    if(pm[i]-1==dp)continue;
                    if(stm[pm[i]])break;
                }
                if(n==i)break;
                i=pm[i];
                sn+=__cl(q=ps[i],i-1,i,1,1,n);
                for(gpm(n),t=n+1,j=0;j<n;++j){
                    if(q==pm[j]-1)
                      continue;
                    d=__cl(pm[j]-1,i-1,i,0,0,n);
                    if(d<t){
                      t=d;
                      k=pm[j]-1;
                    }
                }
                sn+=__cl(k,i-1,i,0,1,n);
            }
        }
        if(qn<dqn){
          makeans(n);
        }else{
          ans[0]=0;
        }
        return (string)ans;
    };     
    std::string solveNQueens(int n, std::pair<int, int> mandatoryQueenCoordinates)
    {
      return _cl(n,mandatoryQueenCoordinates.second,mandatoryQueenCoordinates.first);
    }
}


#############################
#include <bits/stdc++.h>

namespace nQueens
{
    using namespace std;
    typedef long double ld;
    const ld ai = 0.9991, e = 2.7182818284, eps = 1e-3;
    const ld MAXX = 30000;
    pair<int, int> mqp;
    short a1[4000], a2[2000];

    void init() {
      srand(time(0));
    }

    ld decr(ld T) {
      return T * ai;
    }

    vector<int> next(const vector<int> &s) {
      int i = rand() % s.size(),
      j = rand() % s.size();
      while (s.size() != 1 && (i == mqp.second || j == mqp.second)) {
        i = rand() % s.size();
        j = rand() % s.size();
      }
      vector<int> ans = s;
      swap(ans[i], ans[j]);
      return ans;
    }

    int E(const vector<int> &s) {
      int ans = 0;
      memset(a1, 0, 4000 * sizeof(short));
      memset(a2, 0, 2000 * sizeof(short));
      for (int i = 0; i < (int)s.size(); i++) {
        ans += a1[i - s[i] + 2000] + a2[i + s[i]];
        a1[i - s[i] + 2000]++;
        a2[i + s[i]]++;
      }
      return ans;
    }

    int prob(ld dE, ld T) {

      ld p = pow(e, -(dE) / T);
      ld cur = (rand() * 1.) / RAND_MAX;
      return cur < p;
    }

    string solve(int n) {
      vector<int> s(n);
      for (int i = 0; i < n; i++) {
        s[i] = i;
      }
      swap(s[0], s[mqp.first]);
      random_shuffle(s.begin() + 1, s.begin() + n);
      swap(s[0], s[mqp.second]);
      ld T = MAXX;
      for (int i = 0; i < 5e5; i++) {
        //cout << T << "\n";
        vector<int> sn = next(s);
        int E1 = E(s),
        E2 = E(sn);
        if (E1 == 0) {
          break;
        }
        if (E2 < E1) {
          s = std::move(sn);
          if (E2 == 0) {
            break;
          }
        } else {
          if (prob(E2 - E1, T)) {
            s = std::move(sn);
          }
        }
        T = decr(T);
      }
      //cout << E(s) << "\n";
      
      
      string res;
      for (int i = 0; i < n; i++) {
        for (int j = 0; j < s[i]; j++) {
          res += ".";
        }
        res += "Q";
        for (int j = s[i] + 1; j < n; j++) {
          res += ".";
        }
        res += "\n";
      }
      //cout << res;
      //cout << "\n\n";
      if (E(s) > 0) {
        return "";
      }
      return res;
    }

    string solveNQueens(int n, pair<int, int> mandatoryQueenCoordinates)
    {
      init();
      mqp = mandatoryQueenCoordinates;
      return solve(n);
    }
}
