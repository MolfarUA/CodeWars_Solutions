5a20eeccee1aae3cbc000090


#include <vector>
#include <iostream>
#include <climits>
#include <set>
#include <functional>
#include <queue>
using namespace std;
struct Pos{
  int y; int x;
  Pos(){ y=0; x=0; }
  Pos(int y,int x): y{y},x{x}{};
  bool operator==( const Pos& rhs)  { return x==rhs.x && y==rhs.y;  }
  Pos  operator+ ( const Pos& rhs)  { return Pos(y+rhs.y,x+rhs.x ); }
};

using  pPair=pair<int,Pos>;
bool sortMagPos( const pair<int,Pos>& p1, const pair<int,Pos>& p2){  return p1.first <p2.first; }

class cell 
{ 
  public:
    Pos parent; 
    int f, g, h; 
    cell(){ 
      parent=Pos(-1,-1);
      f=g=h=INT_MAX; 
    }
}; 

vector<Pos> findPath(vector<vector<bool>> grid, Pos src, Pos dest) 
{ 
    int n=grid.size();
    if (dest==src) 
        return{}; 
    vector<vector<cell>> cells(grid.size());
    for(size_t y=0;y<grid.size();y++){
      cells[y].resize(grid.size());
      for(size_t x=0;x<grid.size();x++) cells[y][x]=cell(); 
    }
  
    cells[src.y][src.x].f = 0; 
    cells[src.y][src.x].g = 0; 
    cells[src.y][src.x].h = 0; 
    cells[src.y][src.x].parent=src; 
  
    auto comp = [](pPair a, pPair b){ return a.first <b.first;};
    priority_queue<pPair, vector<pPair>, decltype(comp) > openQ(comp);
    openQ.push(make_pair (0, src)); 
  
    bool found = false; 
    while (!openQ.empty()) 
    { 
        pPair p = openQ.top(); 
        openQ.pop(); 
        Pos cp=p.second;
  
        int gNew, hNew, fNew; 
        vector<Pos> dirs={Pos(1,0),Pos(-1,0),Pos(0,1),Pos(0,-1)};
  
        for (Pos d:dirs){
            Pos np= cp+d;
            if (np.x>=0 && np.x<n && np.y>=0 && np.y<n && grid[np.y][np.x]==false) 
            { 
                if (dest==np) found = true; 
                gNew = cells[cp.y][cp.x].g + 1.0; 
                hNew = abs(dest.y-np.y)+abs(dest.x-np.x); 
                fNew = gNew + hNew; 

                if (cells[np.y][np.x].f > fNew) 
                { 
                    openQ.push( make_pair(fNew, np)); 
                    cells[np.y][np.x].f = fNew; 
                    cells[np.y][np.x].g = gNew; 
                    cells[np.y][np.x].h = hNew; 
                    cells[np.y][np.x].parent=cp; 
                } 
            } 
        } 
     } 
    if (found == false) return {}; 
  
    vector<Pos> res;
    Pos np=dest;
    while(!(np==src)){
      res.push_back(np);
      np=cells[np.y][np.x].parent;
    }
    reverse(res.begin(),res.end()); 
    return res;
} 

int move0(vector<vector<int>> &v, vector<Pos> &pos, Pos des){
  int vdes=v[des.y][des.x];
  v[pos[0].y][pos[0].x]=vdes;
  pos[v[des.y][des.x]]=pos[0];
  pos[0]=des;
  v[des.y][des.x]=0;
  return vdes;
}
void move(vector<vector<int>> &v,vector<vector<bool>> &f, vector<Pos> &pos, Pos src, Pos dest, vector<int> &res){
  vector<Pos> path=findPath(f,src,dest);
  int t=v[src.y][src.x];
  for(auto pd:path){
    f[pos[t].y][pos[t].x]=true;
    vector<Pos> path0=findPath(f,pos[0],pd);
    for(auto m0:path0) res.push_back(move0(v,pos,m0)); 
    f[pos[t].y][pos[t].x]=false;
    res.push_back(move0(v,pos,pos[t]));
  }
}
std::vector<int> slide_puzzle(const std::vector<std::vector<int>> &arr)
{
  vector<int> res;
  size_t n=arr.size();
  vector<Pos> pos(n*n);
  vector<vector<int>> v(n,vector<int>(n,0));
  vector<vector<bool>> f(n,vector<bool>(n,false));
  for (size_t y=0;y<n;y++){
    for (size_t x=0;x<n;x++){
      v[y][x]=arr[y][x];
      pos[v[y][x]]=Pos(y,x);
    }
  }
  for (size_t lc=0;lc<n-2;lc++){
    for (size_t x=lc;x<n-2;x++){               //Top Line
      int t=lc*n+x+1;
      move(v,f,pos,pos[t],Pos(lc,x),res);
      f[lc][x]=true;
    }
    
    int t=lc*n+n-1;                          //Move previous to last column out of the way
    Pos pt=pos[t];
    move(v,f,pos,pos[t],Pos(n-1,n-1),res);
    
    t=lc*n+n;                                //put last column number of line one box before 
    move(v,f,pos,pos[t],Pos(lc,n-2),res);
   
    f[lc][n-2]=true;                          //put previous to last last column number one line below
    t=lc*n+n-1;
    move(v,f,pos,pos[t],Pos(lc+1,n-2),res);
    f[lc+1][n-2]=true;
    vector<Pos> path0=findPath(f,pos[0],Pos(lc,n-1));
    for(auto m0:path0) res.push_back(move0(v,pos,m0));
    f[lc][n-2]=false;
    f[lc+1][n-2]=false;
    res.push_back(move0(v,pos,Pos(lc,n-2)));
    res.push_back(move0(v,pos,Pos(lc+1,n-2)));
    f[lc][n-2]=true;
    f[lc][n-1]=true;
    
    for (size_t y=lc+1;y<n-2;y++){             //arrange left column
      t=y*n+lc+1;
      move(v,f,pos,pos[t],Pos(y,lc),res);
      f[y][lc]=true;
    }
    
    t=(n-2)*n+lc+1;                           //take number previos to last in column out the way
    move(v,f,pos,pos[t],Pos(n-1,n-1),res);
    
    t=(n-1)*n+lc+1;                           //put last  number in column one line up
    move(v,f,pos,pos[t],Pos(n-2,lc),res);
    f[n-2][lc]=true; 
    
    t=(n-2)*n+lc+1;                           //put previous to last number in column one column to the right
    move(v,f,pos,pos[t],Pos(n-2,lc+1),res);
    f[n-2][lc+1]=true;
    path0=findPath(f,pos[0],Pos(n-1,lc));
    for(auto m0:path0)
        res.push_back(move0(v,pos,m0));
    f[n-2][lc]=false;
    f[n-2][lc+1]=false;
    res.push_back(move0(v,pos,Pos(n-2,lc)));
    res.push_back(move0(v,pos,Pos(n-2,lc+1)));
    f[n-1][lc]=true;
    f[n-2][lc]=true;
  }
  
  int t=(n-2)*n+n-1;                          //arange the last 4 cells in the grid
  move(v,f,pos,pos[t],Pos(n-2,n-2),res);
  res.push_back(move0(v,pos,Pos(n-1,n-1)));
  
  if (v[n-1][n-2]!=n*n-1) return {0};         //unsolvable
  
  return res;
}
__________________________________________________________________
#include <list>

size_t N;
std::vector<int> result;
std::pair<int, int> zeroPosition;
std::vector<std::vector<int>> arr;
std::vector<std::vector<bool>> fixedTiles;
std::vector<std::vector<bool>> mapToPathfinding;

std::pair<int, int> findZero()
{
    for (int i = 0; i<N; ++i)
        for (int j = 0; j<N; ++j)
            if (arr[i][j] == 0)
                return { i,j };
}

std::pair<int, int> findTile(int tile)
{
    for (int i = 0; i<N; ++i)
        for (int j = 0; j<N; ++j)
            if (arr[i][j] == tile)
            {
                return{ i,j };
            }
}

std::list<std::pair<int, int>> findPath(const std::pair<int, int>& source, const std::pair<int, int>& target, bool start = true)
{
    if (start)
        mapToPathfinding = fixedTiles;

    mapToPathfinding[source.first][source.second] = true;

    if (source == target)
        return { target };

    std::list<std::pair<int, int>> path;
    if (source.first > 0 && !mapToPathfinding[source.first - 1][source.second])
    {
        path = findPath({ source.first - 1, source.second }, target, false);
        if (!path.empty())
        {
            path.push_front(source);
            return path;
        }
    }
    if (source.second > 0 && !mapToPathfinding[source.first][source.second-1])
    {
        path = findPath({ source.first, source.second-1 }, target, false);
        if (!path.empty())
        {
            path.push_front(source);
            return path;
        }
    }
    if (source.first < N-1 && !mapToPathfinding[source.first + 1][source.second])
    {
        path = findPath({ source.first + 1, source.second }, target, false);
        if (!path.empty())
        {
            path.push_front(source);
            return path;
        }
    }
    if (source.second < N - 1 && !mapToPathfinding[source.first][source.second + 1])
    {
        path = findPath({ source.first, source.second + 1 }, target, false);
        if (!path.empty())
        {
            path.push_front(source);
            return path;
        }
    }
    return {};
}

void swapTileAndZero(const std::pair<int, int>& tilePosition)
{
    int tile = arr[tilePosition.first][tilePosition.second];
    result.push_back(tile);

    arr[zeroPosition.first][zeroPosition.second] = tile;
    arr[tilePosition.first][tilePosition.second] = 0;
    zeroPosition = tilePosition;
}

bool moveZeroToPosition(const std::pair<int, int>& targetPosition)
{
    auto zeroPath = findPath(zeroPosition, targetPosition);

    if (zeroPath.empty())
        return false;

    auto zeroPathPosition = zeroPath.begin();
    ++zeroPathPosition;
    for (; zeroPathPosition != zeroPath.end(); ++zeroPathPosition)
    {
        swapTileAndZero(*zeroPathPosition);
    }

    return true;
}

bool moveTileToPosition(int tile, const std::pair<int, int>& targetPosition)
{
    auto tilePosition = findTile(tile);

    auto tilePath = findPath(tilePosition, targetPosition);

    if (tilePath.empty())
        return false;

    auto tilePathPosition = tilePath.begin();
    ++tilePathPosition;
    for (; tilePathPosition != tilePath.end(); ++tilePathPosition)
    {
        fixedTiles[tilePosition.first][tilePosition.second] = true;
        if (!moveZeroToPosition(*tilePathPosition))
            return false;
        fixedTiles[tilePosition.first][tilePosition.second] = false;

        swapTileAndZero(tilePosition);
        tilePosition = *tilePathPosition;
    }
    return true;
}

std::vector<int> slide_puzzle(const std::vector<std::vector<int>> &in_arr)
{
    result = {};
    arr = in_arr;
    N = arr.size();
    fixedTiles = std::vector<std::vector<bool>>(N, std::vector<bool>(N, false));

    zeroPosition = findZero();

    int i = 0;
    for (; i < N - 2; ++i)
    {
        for (int j = 0; j < N - 1; ++j)
        {
            moveTileToPosition(i*N + j + 1, { i, j });
            fixedTiles[i][j] = true;
        }
        
        if (zeroPosition == std::make_pair(i, static_cast<int>(N-1)))
            swapTileAndZero({ i + 1, N - 1 });

        if (arr[i][N - 1] != (i + 1)*N)
        {
            moveTileToPosition((i + 1)*N, { i + 1, N - 1 });
            fixedTiles[i + 1][N - 1] = true;
            moveZeroToPosition({ i + 2, N - 1 });
            fixedTiles[i + 1][N - 1] = false;

            swapTileAndZero({ i + 1, N - 1 });
            swapTileAndZero({ i, N - 1 });
            swapTileAndZero({ i, N - 2 });
            swapTileAndZero({ i + 1, N - 2 });
            swapTileAndZero({ i + 1, N - 1 });
            swapTileAndZero({ i + 2, N - 1 });
            swapTileAndZero({ i + 2, N - 2 });
            swapTileAndZero({ i + 1, N - 2 });
            swapTileAndZero({ i, N - 2 });
            swapTileAndZero({ i, N - 1 });
            swapTileAndZero({ i + 1, N - 1 });
        }
        fixedTiles[i][N-1] = true;
    }

    for (int j = 0; j < N - 2; ++j)
    {
        moveTileToPosition(i*N + 1 + j, { i, j });
        fixedTiles[i][j] = true;

        if (arr[N-1][j] != (N - 1)*N + j + 1)
        {
            moveTileToPosition((N - 1)*N + j + 1, { N - 1, j + 1 });
            
            if (zeroPosition != std::make_pair( static_cast<int>(N - 1), j))
            {
                fixedTiles[N - 1][j + 1] = true;
                moveZeroToPosition({ N - 1, j + 2 });
                fixedTiles[N - 1][j + 1] = false;

                swapTileAndZero({ N - 1, j + 1 });
                swapTileAndZero({ N - 1, j });
                swapTileAndZero({ N - 2, j });
                swapTileAndZero({ N - 2, j + 1 });
                swapTileAndZero({ N - 1, j + 1 });
                swapTileAndZero({ N - 1, j + 2 });
                swapTileAndZero({ N - 2, j + 2 });
                swapTileAndZero({ N - 2, j + 1 });
                swapTileAndZero({ N - 2, j });
                swapTileAndZero({ N - 1, j });
                swapTileAndZero({ N - 1, j + 1 });
            }
            else
            {
                swapTileAndZero({ N - 1, j + 1 });
            }

            fixedTiles[N - 1][j] = true;
        }
    }

    if (!moveTileToPosition(N*N - 1, { N - 1, N - 2 }))
        return{ 0 };
    fixedTiles[N - 1][N - 2] = true;
    if (!moveTileToPosition((N-1)*N - 1, { N - 2, N - 2 }))
        return{ 0 };
    fixedTiles[N - 2][N - 2] = true;
    if (!moveTileToPosition((N - 1)*N, { N - 2, N - 1 }))
        return{ 0 };

    return result;
}
__________________________________________________________________
#include <vector>
using namespace std;
void moveUp(vector<vector<int>> &v, vector<int> &c)
{
  int k = 0;
  for (int i = 0; i<v.size(); ++i)
  {
    for (int j = 0; j<v.size(); ++j)
      if (v[i][j] == 0 && i != 0)
      {
        v[i][j] = v[i - 1][j];
        v[i - 1][j] = 0;
        c.push_back(v[i][j]);
        k++;
        break;
      }
    if (k != 0) break;
  }
}
void moveDown(vector<vector<int>> &v, vector<int> &c)
{
  int k = 0;
  for (int i = 0; i<v.size(); ++i)
  {
    for (int j = 0; j<v.size(); ++j)
      if (v[i][j] == 0 && i != v.size() - 1)
      {
        v[i][j] = v[i + 1][j];
        v[i + 1][j] = 0;
        c.push_back(v[i][j]);
        k++;
        break;
      }
    if (k != 0) break;
  }
}
void moveLeft(vector<vector<int>> &v, vector<int> &c)
{
  int k = 0;
  for (int i = 0; i<v.size(); ++i)
  {
    for (int j = 0; j<v.size(); ++j)
      if (v[i][j] == 0 && j != 0)
      {
        v[i][j] = v[i][j - 1];
        v[i][j - 1] = 0;
        c.push_back(v[i][j]);
        k++;
        break;
      }
    if (k != 0) break;
  }
}
void moveRight(vector<vector<int>> &v, vector<int> &c)
{
  int k = 0;
  for (int i = 0; i<v.size(); ++i)
  {
    for (int j = 0; j<v.size(); ++j)
      if (v[i][j] == 0 && j != v.size() - 1)
      {
        v[i][j] = v[i][j + 1];
        v[i][j + 1] = 0;
        c.push_back(v[i][j]);
        k++;
        break;
      }
    if (k != 0) break;
  }
}
void moveInPlace1(int n, vector<vector<int>> &v, vector<int> &c)
{
  int x1 = int((n - 1) / v.size());
  int y1 = (n - 1) % v.size();
  int x0=0;
  int y0=0;
  for (int i = 0; i<v.size(); ++i)
    for (int j = 0; j<v.size(); ++j)
      if (v[i][j] == n)
      {
        x0 = i;
        y0 = j;
        break;
      }
  if (x0 == v.size() - 1)
  {
    for (int i = 0; i<v.size() - y0 - 2; ++i)
      moveLeft(v, c);
    moveUp(v, c);
    moveLeft(v, c);
    moveDown(v, c);
    for (int i = 0; i<v.size() - y0 - 1; ++i)
      moveRight(v, c);
    x0--;
  }
  if (y0 <= y1)
  {
    for (int i = 0; i<v.size() - y0 - 2; ++i)
      moveLeft(v, c);
    for (int i = 0; i<v.size() - x0 - 1; ++i)
      moveUp(v, c);
    for (int i = 0; i<y1 - y0; ++i)
    {
      moveLeft(v, c);
      moveDown(v, c);
      moveRight(v, c);
      moveRight(v, c);
      moveUp(v, c);
    }
  }
  if (y0>y1)
  {
    for (int i = 0; i<v.size() - y0; ++i)
      moveLeft(v, c);
    for (int i = 0; i<v.size() - x0 - 1; ++i)
      moveUp(v, c);
    for (int i = 0; i<y0 - y1; ++i)
    {
      moveRight(v, c);
      if (i != y0 - y1 - 1)
      {
        moveDown(v, c);
        moveLeft(v, c);
        moveLeft(v, c);
        moveUp(v, c);
      }
    }
  }
  for (int i = 0; i<x0 - x1; ++i)
  {
    moveUp(v, c);
    moveLeft(v, c);
    moveDown(v, c);
    moveRight(v, c);
    moveUp(v, c);
  }
}
void moveInPlace2(int n, vector<vector<int>> &v, vector<int> &c)
{
  int x1 = int((n - 1) / v.size());
  int y1 = (n - 1) % v.size();
  if (n%v.size() != 0)
    y1++;
  else
    x1++;
  int x0=0;
  int y0=0;
  for (int i = 0; i<v.size(); ++i)
    for (int j = 0; j<v.size(); ++j)
      if (v[i][j] == n)
      {
        x0 = i;
        y0 = j;
        break;
      }
  if (n%v.size() == 0 && y1 - y0 == 1 && x1 - x0 == 1)
  {
    moveLeft(v, c);
    for (int i = 0; i<v.size() - x0 - 1; ++i)
      moveUp(v, c);
    moveRight(v, c);
    moveDown(v, c);
    moveDown(v, c);
    moveLeft(v, c);
    moveUp(v, c);
    moveRight(v, c);
    moveUp(v, c);
    moveLeft(v, c);
    for (int i = 0; i<v.size() - x0 - 1; ++i)
      moveDown(v, c);
    moveRight(v, c);
    x0++;
  }
  if (x0 == v.size() - 1)
  {
    for (int i = 0; i<v.size() - y0 - 2; ++i)
      moveLeft(v, c);
    moveUp(v, c);
    moveLeft(v, c);
    moveDown(v, c);
    for (int i = 0; i<v.size() - y0 - 1; ++i)
      moveRight(v, c);
    x0--;
  }
  if (y0<y1)
  {
    for (int i = 0; i<v.size() - y0 - 2; ++i)
      moveLeft(v, c);
    for (int i = 0; i<v.size() - x0 - 1; ++i)
      moveUp(v, c);
    for (int i = 0; i<y1 - y0; ++i)
    {
      moveLeft(v, c);
      if (i != y1 - y0 - 1)
      {
        moveDown(v, c);
        moveRight(v, c);
        moveRight(v, c);
        moveUp(v, c);
      }
    }
  }
  if (y0 == y1)
  {
    moveLeft(v, c);
    for (int i = 0; i<v.size() - x0 - 1; ++i)
      moveUp(v, c);
  }
  for (int i = 0; i<x0 - x1; ++i)
  {
    moveUp(v, c);
    moveRight(v, c);
    moveDown(v, c);
    moveLeft(v, c);
    moveUp(v, c);
  }
  if (n%v.size() == 0)
  {
    moveUp(v, c);
    moveRight(v, c);
    moveDown(v, c);
  }
}
void moveInPlace3(int n, vector<vector<int>> &v, vector<int> &c)
{
  int x1 = int((n - 1) / v.size());
  int y1 = (n - 1) % v.size();
  if ((int)((n - 1) / v.size()) == v.size() - 1)
    x1--;
  else
    y1++;
  int x0=0;
  int y0=0;
  for (int i = 0; i<v.size(); ++i)
    for (int j = 0; j<v.size(); ++j)
      if (v[i][j] == n)
      {
        x0 = i;
        y0 = j;
        break;
      }
  if ((int)((n - 1) / v.size()) != v.size() - 1 && y1 - y0 == 1 && x0 - x1 == 1)
  {
    for (int i = 0; i<v.size() - y0 - 1; ++i)
      moveLeft(v, c);
    moveUp(v, c);
    moveRight(v, c);
    moveRight(v, c);
    moveDown(v, c);
    moveLeft(v, c);
    moveUp(v, c);
    moveLeft(v, c);
    moveDown(v, c);
    for (int i = 0; i<v.size() - y0 - 1; ++i)
      moveRight(v, c);
    y0++;
  }
  if (x0 == v.size() - 1)
  {
    for (int i = 0; i<v.size() - y0 - 2; ++i)
      moveLeft(v, c);
    moveUp(v, c);
    moveLeft(v, c);
    moveDown(v, c);
    for (int i = 0; i<v.size() - y0 - 1; ++i)
      moveRight(v, c);
    x0--;
  }
  if (y0 >= y1)
  {
    for (int i = 0; i<v.size() - y0 - 1; ++i)
      moveLeft(v, c);
    for (int i = 0; i<y0 - y1; ++i)
    {
      moveLeft(v, c);
      moveUp(v, c);
      moveRight(v, c);
      moveDown(v, c);
      moveLeft(v, c);
    }
  }
  if ((int)((n - 1) / v.size()) != v.size() - 1)
  {
    moveLeft(v, c);
    moveUp(v, c);
    moveRight(v, c);
  }
}
void move0(vector<vector<int>> &v, vector<int> &c)
{
  for (int i = 0; i<v.size(); ++i)
    for (int j = 0; j<v.size(); ++j)
      if (v[i][j] == 0)
      {
        for (int k = 0; k<v.size() - i; ++k)
          moveDown(v, c);
        for (int k = 0; k<v.size() - j; ++k)
          moveRight(v, c);
        break;
      }
}
vector<int> slide_puzzle(const vector<std::vector<int>> &arr)
{
  vector<int> ans;
  vector<vector<int>> s = arr;
  for (int i=0; i<s.size(); ++i)
  {
    for (int j=0; j<s.size(); ++j)
      cout << s[i][j]<<' ';
    cout << endl;
  }
  cout << endl;
  for (int i = 1; i<=s.size()*(s.size() - 2); ++i)
  {
    if (s[(int)((i - 1) / s.size())][(i - 1) % s.size()] == i && (i - 1) % s.size()<s.size() - 2)
      continue;
    else
    {
      move0(s, ans);
      if ((i - 1)%s.size()<s.size() - 2)
        moveInPlace1(i, s, ans);
      else
        moveInPlace2(i, s, ans);
    }
  }
  for (int i = 1; i <= s.size() - 2; ++i)
  {
    move0(s, ans);
    moveInPlace3(i + s.size()*(s.size() - 1), s, ans);
    move0(s, ans);
    moveInPlace3(i + s.size()*(s.size() - 2), s, ans);
  }
  move0(s, ans);
  while (s[s.size() - 1][s.size() - 2] != s.size()*s.size() - 1)
  {
    moveUp(s, ans);
    moveLeft(s, ans);
    moveDown(s, ans);
    moveRight(s, ans);
  }
  if (s[s.size()-2][s.size()-1]!=s.size()*(s.size()-1))
    return {0};
  return ans;
}
__________________________________________________________________
#include <vector>
#include <algorithm>
#include <array>
#include <map>
#include <iostream>
#include <unordered_map>

#include <random>
#include <time.h>

using namespace std;

std::random_device rd;                        // only used once to initialise (seed) engine
std::mt19937 rng(rd());                       // random-number engine used (Mersenne-Twister in this case)
std::uniform_int_distribution<int> uni(1, 4); // guaranteed unbiased

//look-up table for factorials from 0 to 10
const array<size_t, 11> factorials = {1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800};

//State Transition Table
struct STTNode
{
    STTNode *pseq;              //link to previous node
    vector<vector<int>> puzzle; //corresponding state

    //ctor
    STTNode(vector<vector<int>> puzzle_, STTNode *pseq_ = nullptr) : puzzle(puzzle_),
                                                                     pseq(pseq_)
    {
    }

    //dtor
    ~STTNode()
    {
    }

    //overload compare operator
    bool operator==(const STTNode &node_) const noexcept
    {
        return (puzzle == node_.puzzle);
    }
};

//flatten input 2D vector
vector<int> ExpandPuzzle(const vector<vector<int>> &puzzle)
{
    vector<int> flatten_puzzle;

    for (auto i : puzzle)
        for (auto tile : i)
            flatten_puzzle.emplace_back(tile);

    return flatten_puzzle;
}

//calculate inversion count of each tile
vector<int> GetInversions(const vector<vector<int>> &puzzle, bool incz = false)
{
    vector<int> flatten_puzzle = ExpandPuzzle(puzzle);
    int sz = flatten_puzzle.size();

    vector<int> invs(sz, 0);

    for (int i = 0; i < sz - 1; i++)
        for (int j = i + 1; j < sz; j++)
        {
            if (!incz)
            {
                if (flatten_puzzle[i] > 0 && flatten_puzzle[j] > 0 && flatten_puzzle[i] > flatten_puzzle[j])
                    invs[i]++;
            }
            else
            {
                if (flatten_puzzle[i] > flatten_puzzle[j])
                    invs[i]++;
            }
        }
    return invs;
}

//specialization of hash function
namespace std
{
template <>
struct hash<STTNode>
{
    size_t operator()(const STTNode &node) const noexcept
    {
        size_t hash_value = 1;

        vector<int> invs = GetInversions(node.puzzle, true);

        vector<int> flatten_puzzle = ExpandPuzzle(node.puzzle);
        int sz = flatten_puzzle.size();

        for (int i = sz - 1; i >= 0; --i)
            hash_value += (factorials[i] * invs[sz - i - 1]);

        return hash_value;
    }
};
} // namespace std

//hash maps for STT
unordered_map<STTNode, STTNode *> STT3x2;
unordered_map<STTNode, STTNode *> STT2x3;

//solvability judgment
bool IsSolvable(const vector<vector<int>> &puzzle)
{
    int m = puzzle.size();    //rows
    int n = puzzle[0].size(); //cols

    vector<int> invs = GetInversions(puzzle);

    int invs_sum = accumulate(invs.begin(), invs.end(), 0); //total inversions of puzzle
    int bi = 0;

    for (auto vrow : puzzle)
    {
        if (find(vrow.begin(), vrow.end(), 0) != vrow.end())
            break;
        ++bi;
    }

    if (n % 2 && !(invs_sum % 2))
        return true;
    else if (!(n % 2) && ((bool)((m - bi) % 2) == !(invs_sum % 2)))
        return true;
    else
        return false;

    return true;
}

//moving method
bool Moving(int &blank_i, int &blank_j, int direction, int size_m, int size_n)
{

    switch (direction)
    {
    case 1: //upward
        blank_i--;
        if (blank_i < 0)
        {
            blank_i++;
            return false;
        }
        break;

    case 2: //leftward
        blank_j--;
        if (blank_j < 0)
        {
            blank_j++;
            return false;
        }
        break;

    case 3: //downward
        blank_i++;
        if (blank_i > size_m - 1)
        {
            blank_i--;
            return false;
        }
        break;

    case 4: //rightward
        blank_j++;
        if (blank_j > size_n - 1)
        {
            blank_j--;
            return false;
        }
        break;
    }
    return true;
}

STTNode *root3x2;
STTNode *root2x3;
//construct nodes of hash maps and filling State Transition Table
void ConstructSTT(unordered_map<STTNode, STTNode *> &STT, bool STT3x2 = true)
{
    vector<vector<int>> init_state;
    int blank_i, blank_j;
    int i, j;
    int szm, szn;

    if (STT3x2)
    {
        init_state = {{1, 2}, {3, 4}, {5, 0}};
        root3x2 = new STTNode(init_state, root3x2);
        STT.insert(make_pair(*root3x2, root3x2));
        i = blank_i = 2;
        j = blank_j = 1;
        szm = 3;
        szn = 2;
    }
    else
    {
        init_state = {{1, 2, 3}, {4, 5, 0}};
        root2x3 = new STTNode(init_state, root2x3);
        STT.insert(make_pair(*root2x3, root2x3));
        i = blank_i = 1;
        j = blank_j = 2;
        szm = 2;
        szn = 3;
    }

    do
    {
        if (Moving(i, j, uni(rng), szm, szn)) //stochastic moving of blank tile (it's simple and ugly =) )
        {
            //actually, the stochastic filling is much slower than determininig, but more simplify.
            //In this case it's about 200 msec. without chance to compilling as constexpr.
            //Btw, the code could be re-engineering for filling as constexpr and it'll boost this realization up to 0.5 msec.
            auto prev_state_key = STTNode(init_state);
            swap(init_state[blank_i][blank_j], init_state[i][j]);

            blank_i = i;
            blank_j = j;

            if (!STT.count(STTNode(init_state)) && IsSolvable(init_state))
            {
                auto prev_state_link = (*(STT.find(prev_state_key))).second;
                STT.insert(make_pair(STTNode(init_state), new STTNode(init_state, prev_state_link)));
            }
        }
    } while (STT.size() != 360);
}

//find position of tile in the puzzle
pair<int, int> FindTile(vector<vector<int>> &puzzle, int tile)
{
    int i, j;

    for (int i = 0; i < puzzle.size(); ++i)
        for (int j = 0; j < puzzle[0].size(); ++j)
            if (puzzle[i][j] == tile)
                return make_pair(i + 1, j + 1);

    return pair<int, int>();
}

vector<pair<int, int>> forbidden_pos;      //already in-place tile
vector<pair<int, int>> steps;              //already made steps
vector<pair<float, pair<int, int>>> seeds; //seeds for the next step
vector<int> MovingBlankHistory;            //history of blank tile mooving
//moving tile along the shortest path to it target position
void SolveTile(vector<vector<int>> &puzzle, int m, int n, int tile, int M, int N)
{
    //until tile not in-place
    while (puzzle[m - 1][n - 1] != tile)
    {

        auto blank_pos = FindTile(puzzle, 0);
        auto tile_pos = FindTile(puzzle, tile);

        //tile-target distance
        int ttr = tile_pos.first - m;  //row
        int ttc = tile_pos.second - n; //col

        //new blank position
        int bpr = -999, bpc = -999;

        if (ttc != 0)
        {
            bpr = tile_pos.first;
            if (ttc > 0)
            { //b-p
                bpc = tile_pos.second - 1;
            }
            else if (ttc < 0)
            { //p-b
                bpc = tile_pos.second + 1;
            }
        }
        else
        {
            bpc = tile_pos.second;
            if (ttr > 0) //vertical b-p
            {
                bpr = tile_pos.first - 1;
            }
            else if (ttr < 0)
            { //vertical p-b
                bpr = tile_pos.first + 1;
            }
        }

        //target position of blank tile
        bpr--;
        bpc--;

        //greedy strategy with minimize path
        while (pair<int, int>(bpr + 1, bpc + 1) != blank_pos) //until reached blank target pos
        {
            int ib_init = blank_pos.first - 1, jb_init = blank_pos.second - 1;
            steps.emplace_back(ib_init, jb_init); //blank pos

            for (int i = 4; i >= 1; --i) //heuristic --- prefer right/down move.
            {
                int ib = blank_pos.first - 1, jb = blank_pos.second - 1;

                if (Moving(ib, jb, i, M, N) &&                                                                  //if move can be done
                    find(steps.begin(), steps.end(), make_pair(ib, jb)) == steps.end() &&                       //if it step didn't use before
                    (pair<int, int>(ib + 1, jb + 1) != tile_pos) &&                                             //move mustn't change targte tile
                    find(forbidden_pos.begin(), forbidden_pos.end(), make_pair(ib, jb)) == forbidden_pos.end()) //move mustn't change already in-place tiles
                {
                    float dist = sqrt((bpr - ib) * (bpr - ib) + (bpc - jb) * (bpc - jb)); //estimate distance
                    seeds.emplace_back(dist, make_pair(ib, jb));
                }
            }

            //get step with min distance prefer down/right move
            pair<int, int> next_pos = make_pair(-999, -999);
            int min_dist = 999;
            for (auto v : seeds)
            {
                if (v.first < min_dist)
                {
                    next_pos = v.second;
                    min_dist = v.first;
                }
            }

            steps.emplace_back(next_pos.first, next_pos.second);
            MovingBlankHistory.emplace_back(puzzle[next_pos.first][next_pos.second]); //store blank tile move
            swap(puzzle[ib_init][jb_init], puzzle[next_pos.first][next_pos.second]);  //move blank tile

            seeds.clear();
            blank_pos = FindTile(puzzle, 0);
        }
        //exchange blank and target tile
        MovingBlankHistory.emplace_back(puzzle[tile_pos.first - 1][tile_pos.second - 1]); //store blank tile move
        swap(puzzle[bpr][bpc], puzzle[tile_pos.first - 1][tile_pos.second - 1]);

        steps.clear();
    }

    if (m == M)
        n--;
    if (n == N)
        m--;

    //exit(0);
    forbidden_pos.emplace_back(m - 1, n - 1);
}

//set blank tile to the right-down position of the current rectangle
void SetBlankTile(vector<vector<int>> &puzzle, int m, int n, vector<pair<int, int>> &mapped_pos, bool corner = true)
{
    const int M = puzzle.size();
    const int N = puzzle[0].size();
    auto blank_pos = FindTile(puzzle, 0);
    //until tile not in-place
    if (corner)
    {
        if ((blank_pos.second - 1) - (n - 1) == 0)
            return;
        else if ((blank_pos.second - 1) - n == 0)
            return;
    }
    else
    {
        if ((blank_pos.second - 1) - (n - 1) == 0)
            return;
        else if ((blank_pos.second - 1) - n == 0)
            return;
        else if ((blank_pos.second - 1) - (n - 2) == 0)
            return;
    }
    while (puzzle[m][n] != 0)
    {
        // auto blank_pos = FindTile(puzzle, 0);
        int ib_init = blank_pos.first - 1, jb_init = blank_pos.second - 1;
        steps.emplace_back(ib_init, jb_init); //blank pos
        for (int i = 4; i >= 1; --i)          //heuristic --- prefer right/down move.
        {
            int ib = blank_pos.first - 1, jb = blank_pos.second - 1;

            if (Moving(ib, jb, i, M, N) &&                                                                    //if move can be done
                find(steps.begin(), steps.end(), make_pair(ib, jb)) == steps.end() &&                         //if it step didn't use before
                find(forbidden_pos.begin(), forbidden_pos.end(), make_pair(ib, jb)) == forbidden_pos.end() && //move mustn't change already in-place tiles
                find(mapped_pos.begin(), mapped_pos.end(), make_pair(ib, jb)) == mapped_pos.end())            //move mustn't change already mapped tiles
            {
                float dist = sqrt((m - ib) * (m - ib) + (n - jb) * (n - jb)); //estimate distance
                seeds.emplace_back(dist, make_pair(ib, jb));
            }
        }

        //get step with min distance prefer down/right move
        pair<int, int> next_pos = make_pair(-999, -999);
        int min_dist = 999;
        for (auto v : seeds)
        {
            if (v.first < min_dist)
            {
                next_pos = v.second;
                min_dist = v.first;
            }
        }

        steps.emplace_back(next_pos.first, next_pos.second);
        MovingBlankHistory.emplace_back(puzzle[next_pos.first][next_pos.second]); //store blank tile move
        swap(puzzle[ib_init][jb_init], puzzle[next_pos.first][next_pos.second]);  //move blank tile

        seeds.clear();
        blank_pos = FindTile(puzzle, 0);
    }

    steps.clear();
}

map<int, int> mapping;
//forming sub-puzzle and mapping for it
vector<vector<int>> ApplyMapping(vector<vector<int>> &puzzle, int beg_m, int beg_n, bool corner, bool dir = false)
{

    vector<vector<int>> sub_puzzle;
    vector<int> residual;

    int size_m = 2, size_n = 3;

    // top-right corner 3x2 mapping
    if (corner)
    {
        sub_puzzle = {{0, 0}, {0, 0}, {0, 0}};
        sub_puzzle[0][0] = 1;
        sub_puzzle[1][1] = 2;
        residual = {3, 4, 5};
        swap(size_m, size_n);
    }
    else // last two rows 2x3 mapping
    {
        sub_puzzle = {{0, 0, 0}, {0, 0, 0}};
        sub_puzzle[0][0] = 1;
        sub_puzzle[1][1] = 4;
        residual = {2, 3, 5};
    }

    if (!dir) //mapping for residual tile (not direct)
    {
        do
        {
            next_permutation(residual.begin(), residual.end());
            int i_res = 0;
            for (int i = 0; i < size_m; ++i)
            {
                for (int j = 0; j < size_n; ++j)
                {
                    int m = i + beg_m;
                    int n = j + beg_n;
                    int tile = puzzle[m][n];

                    if (tile == 0 || (i == 0 && j == 0) || (i == 1 && j == 1)) //skip already mapped tiles
                        continue;

                    sub_puzzle[i][j] = residual[i_res++];

                    //cout<<tile<< m<<", "<<n<<", "<<beg_n <<endl;
                }
            }
        } while (!IsSolvable(sub_puzzle));

        for (int i = 0; i < size_m; ++i)
        {
            for (int j = 0; j < size_n; ++j)
            {
                int m = i + beg_m;
                int n = j + beg_n;
                int tile = puzzle[m][n];

                mapping.insert(make_pair(sub_puzzle[i][j], tile));
            }
        }
    }
    else //direct mapping (for last 2x3 puzzle)
    {
        vector<pair<int, pair<int, int>>> prep;
        prep.reserve(6);

        const int M = puzzle.size();

        for (int i = 0; i < size_m; ++i)
        {
            for (int j = 0; j < size_n; ++j)
            {
                int tile = puzzle[i + beg_m][j + beg_n];
                prep.emplace_back(make_pair(tile, FindTile(puzzle, tile)));
            }
        }

        sort(prep.begin(), prep.end(), [](const pair<int, pair<int, int>> &v1, const pair<int, pair<int, int>> &v2) { return v1.first < v2.first; });

        do
        {
            int order = 0;
            for (auto t : prep)
            {
                mapping.insert(make_pair(order, t.first));
                sub_puzzle[t.second.first - (M - 2) - 1][t.second.second - beg_n - 1] = order++;
            }

            swap(prep[3], prep[5]); //heuristic -- only one swap enough to change the solvability

        } while (!IsSolvable(sub_puzzle));
    }
    return sub_puzzle;
}

void FindSolution(vector<vector<int>> &puzzle)
{

    const int M = puzzle.size();    //rows
    const int N = puzzle[0].size(); //cols

    forbidden_pos.reserve(M * N);
    steps.reserve(M * N);
    seeds.reserve(4);
    
    MovingBlankHistory.clear();
    MovingBlankHistory.reserve(M * N * 10);

    vector<pair<int, int>> MpdPos_;

    vector<vector<int>> sub_puzzle;

    for (int m = 1; m <= M - 2; ++m)
    {
        for (int n = 1; n <= N; ++n) //include the last tile in the row
        {

            int tile = n + N * (m - 1);
            if (n != N)
                SolveTile(puzzle, m, n, tile, M, N); // for k
            else
                SolveTile(puzzle, m + 1, n, tile, M, N); //for k+1
        }                                                //n

        MpdPos_ = {pair<int, int>(m - 1, N - 2), pair<int, int>(m, N - 1)};
        SetBlankTile(puzzle, m + 1, N - 1, MpdPos_);

        sub_puzzle = ApplyMapping(puzzle, m - 1, N - 2, true);

        //solve last and second-last tiles in the row using by STT3x2
        auto begin = STT3x2[STTNode(sub_puzzle)];
        int target_1 = N - 1 + N * (m - 1); //second-last target tile => k
        int target_2 = N + N * (m - 1);     //last target tile => k+1

        while (mapping[begin->puzzle[0][0]] != target_1 || mapping[begin->puzzle[0][1]] != target_2)
        {
            auto blank_tile_pos = FindTile(begin->puzzle, 0);
            begin = begin->pseq;
            MovingBlankHistory.emplace_back(mapping[begin->puzzle[blank_tile_pos.first - 1][blank_tile_pos.second - 1]]); //store blank tile move
        }

        for (int i = 0; i < begin->puzzle.size(); ++i)
        {
            for (int j = 0; j < begin->puzzle[0].size(); ++j)
                puzzle[i + (m - 1)][j + (N - 2)] = mapping[begin->puzzle[i][j]];
        }
        mapping.clear();
    } //m

    //for the last two rows
    for (int n = 1; n <= N - 3; ++n)
    {
        for (int m = M - 1; m <= M; ++m)
        {
            int tile = n + N * (m - 1);

            if (m != M)
                SolveTile(puzzle, m, n, tile, M, N); //for s
            else
                SolveTile(puzzle, m, n + 1, tile, M, N); //for s+n tile
        }                                                //m

        MpdPos_ = {pair<int, int>(M - 2, n - 1), pair<int, int>(M - 1, n)};
        SetBlankTile(puzzle, M - 1, n + 1, MpdPos_, false);

        sub_puzzle = ApplyMapping(puzzle, M - 2, n - 1, false);

        //solve last and second-last tiles in the row using by STT3x2
        auto begin = STT2x3[STTNode(sub_puzzle)];
        int target_1 = n + N * (M - 2); //first target tile => s
        int target_2 = n + N * (M - 1); //4th target tile => s+n

        while (mapping[begin->puzzle[0][0]] != target_1 || mapping[begin->puzzle[1][0]] != target_2)
        {
            auto blank_tile_pos = FindTile(begin->puzzle, 0);
            begin = begin->pseq;
            MovingBlankHistory.emplace_back(mapping[begin->puzzle[blank_tile_pos.first - 1][blank_tile_pos.second - 1]]); //store blank tile move
        }
        for (int i = 0; i < begin->puzzle.size(); ++i)
        {
            for (int j = 0; j < begin->puzzle[0].size(); ++j)
                puzzle[i + (M - 1) - 1][j + (n - 1)] = mapping[begin->puzzle[i][j]];
        }
        mapping.clear();
    } //n

    //solve last-down 2x3 puzzle
    sub_puzzle = ApplyMapping(puzzle, M - 2, N - 3, false, true);

    auto begin = STT2x3[STTNode(sub_puzzle)];
    while (begin != root2x3)
    {
        auto blank_tile_pos = FindTile(begin->puzzle, 0);
        begin = begin->pseq;
        MovingBlankHistory.emplace_back(mapping[begin->puzzle[blank_tile_pos.first - 1][blank_tile_pos.second - 1]]); //store blank tile move
    }

    for (int i = 0; i < begin->puzzle.size(); ++i)
    {
        for (int j = 0; j < begin->puzzle[0].size(); ++j)
            puzzle[i + (M - 1) - 1][j + (N - 2) - 1] = mapping[begin->puzzle[i][j]];
    }

    
    mapping.clear();
    sub_puzzle.clear();
    forbidden_pos.clear();
}

bool is_first_lunch = true;
std::vector<int> slide_puzzle(const std::vector<std::vector<int>> &arr)
{  
    if (is_first_lunch)
    {
        ConstructSTT(STT3x2, true);
        ConstructSTT(STT2x3, false);
        is_first_lunch = false;
    }
    
    vector<vector<int>> puzzle = arr;
        
    if (!IsSolvable(puzzle)){
    mapping.clear();
    forbidden_pos.clear();
    MovingBlankHistory.clear();
    return {0};
    }

FindSolution(puzzle);
    return MovingBlankHistory;
}
