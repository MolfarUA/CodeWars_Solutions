#include <bits/stdc++.h>

bool isPerfectSquare(long double x)
{
  long double sr = sqrt(x);
  return ((sr - floor(sr)) == 0);
}

std::vector<int> res;
std::set<int> graph[1005];
std::set<int> graph_copy[1005];

bool dfs(std::vector<std::pair<int,int> > opt, int curr, int obj){
  if(curr == obj) return true;

  sort(opt.begin(),opt.end());

  int sz = opt.size();
  for(int i=0;i<sz;i++){
    int neigh = opt[i].second;

    res.push_back(neigh);
    for(int v: graph[neigh]) graph_copy[v].erase(neigh);

    std::vector<std::pair<int,int> > optx;
    for(int v: graph_copy[neigh]) optx.push_back(std::make_pair(graph_copy[v].size(),v));
    if(dfs(optx,curr+1,obj)) return true;

    for(int v: graph[neigh]) graph_copy[v].insert(neigh);
    res.pop_back();
  }

  return false;
}

std::vector<int> square_sums_row(int n)
{
  res = std::vector<int>();
  for(int i=0;i<1005;i++){
    graph[i] = std::set<int>();
    graph_copy[i] = std::set<int>();
  }


  for(int i=1;i<=n;i++){
    for(int j=i+1;j<=n;j++){
      if(isPerfectSquare(i+j)){
        graph[i].insert(j); graph_copy[i].insert(j);
        graph[j].insert(i); graph_copy[j].insert(i);
      }
    }
  }

  std::vector<std::pair<int,int> > optx;
  for(int v=1;v<=n;v++) optx.push_back(std::make_pair(graph_copy[v].size(),v));
  dfs(optx,0,n);

  return res;
}
____________________________________________________
#include <vector>
#include <algorithm>

int initial[1000] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,9,8,16,0,0,0,0,0,2,0,18,18,21,1,18,18,29,29,22,32,15,33,19,2,14,
                     19,13,18,2,2,2,34,32,47,19,47,8,50,36,19,15,26,50,55,54,23,51,43,22,24,60,64,49,66,50,50,46,
                     46,46,54,35,27,38,52,77,72,44,50,35,9,41,50,18,50,78,38,35,10,35,75,50,63,96,35,35,83,23,49,
                     24,15,5,50,50,16,84,102,73,92,19,77,57,18,116,76,11,15,5,77,50,96,2,18,94,80,80,94,129,50,19,
                     99,12,69,128,36,5,18,93,64,117,36,25,81,110,55,40,33,28,100,134,120,64,27,47,151,114,114,89,
                     106,106,133,108,97,2,13,54,141,54,157,8,33,88,18,91,112,77,150,137,74,51,11,179,96,40,57,148,
                     18,98,47,80,174,167,13,22,22,13,116,116,77,75,84,98,172,18,128,50,18,82,75,120,3,30,39,50,166,
                     166,147,85,86,91,84,161,92,187,145,18,207,221,80,107,218,198,94,221,113,181,181,181,134,134,
                     72,216,51,50,204,2,247,237,50,229,122,202,161,36,188,134,79,128,153,154,141,43,207,79,139,86,
                     102,167,11,21,112,136,258,188,107,110,242,205,146,59,102,25,25,185,169,169,275,259,62,72,194,
                     103,18,270,26,212,233,258,237,197,84,111,58,118,57,193,208,200,282,177,25,110,253,39,242,72,
                     263,51,96,78,247,211,222,32,295,291,198,60,94,171,202,308,308,315,93,43,172,252,135,50,216,
                     226,250,50,66,163,89,245,2,222,200,180,159,52,72,2,347,124,135,50,191,179,240,328,180,83,149,
                     187,13,331,247,32,323,101,52,177,80,354,261,303,157,173,89,77,123,128,329,158,164,164,128,18,
                     172,31,395,134,18,187,353,18,175,308,110,347,166,301,208,103,260,174,332,376,266,200,181,77,
                     38,230,326,242,398,240,103,336,96,58,178,330,401,426,415,174,365,94,132,281,166,299,311,221,
                     148,310,322,157,157,309,403,403,427,70,422,213,215,240,348,154,276,176,423,365,198,298,57,227,
                     110,68,251,225,141,417,432,54,292,189,322,96,54,426,325,472,139,354,98,43,358,342,51,236,419,
                     249,24,298,143,352,285,377,248,212,186,262,438,423,195,210,198,128,323,341,149,149,30,240,132,
                     282,338,345,257,299,324,50,52,352,497,289,402,484,526,302,322,109,509,132,102,376,504,366,201,
                     72,222,340,21,23,55,102,34,459,515,335,313,180,50,336,535,469,517,465,428,503,242,391,137,30,
                     174,265,241,357,222,18,248,547,337,563,563,305,137,420,139,514,508,104,100,163,307,480,83,223,
                     489,340,356,173,102,410,425,300,111,353,120,383,198,402,13,251,555,477,514,319,44,258,353,507,
                     335,103,349,50,23,384,62,56,373,378,108,220,73,624,81,256,518,363,328,78,181,507,80,530,407,545,
                     600,258,128,285,445,258,567,445,128,341,142,8,101,189,364,506,140,353,453,178,383,380,350,491,
                     408,645,573,116,163,347,330,252,353,321,440,163,102,325,182,622,338,42,534,343,103,460,272,271,
                     328,125,410,138,12,304,627,529,312,105,545,386,151,307,602,69,147,54,18,214,391,370,608,13,291,
                     456,298,403,97,520,218,112,226,403,458,458,409,685,5,666,2,135,216,595,181,21,511,550,162,623,
                     178,572,417,48,257,503,665,18,214,45,365,467,398,171,359,736,368,85,342,534,453,505,450,396,193,
                     130,520,515,398,302,537,25,504,755,299,56,140,360,770,529,419,511,765,474,649,472,674,461,593,
                     551,195,445,313,338,243,388,366,702,689,759,759,658,743,229,216,240,456,784,272,613,339,346,617,
                     137,684,339,673,177,389,404,42,800,201,188,412,811,735,313,303,496,553,458,218,422,640,730,42,
                     589,320,81,263,309,598,619,673,792,144,112,290,655,539,705,743,269,431,496,242,331,769,210,200,
                     579,646,541,597,451,836,565,615,268,329,823,547,685,50,699,382,486,491,15,875,847,655,804,667,
                     374,382,679,338,589,778,41,526,254,76,575,669,786,360,748,214,96,266,818,363,896,725,883,342,466,
                     527,830,313,871,831,529,353,363,700,260,19,542,531,375,179,220,392,256,770,134,222,525,557,763,
                     646,153,523,829,885,640,639,686,737,578,230,214,911,139,214,329,397,522,76,786,554,580,306,842,
                     469,444,342,93,467,811,850,783,108,914,205,746,240,240,817,848,971,818,323,891,568,236,591,12,679,
                     679,229,932,815,241,369,491,415,676,533,566,790,593,619,658,743,440,748,185,163};

bool step(bool state[], std::vector<int> &solution, std::vector<int> &squares, int digit, int n)
{
    state[digit-1] = false;      
    solution.push_back(digit);  
    
    if (solution.size() == n)
      return true;
      
    for(auto const& square: squares){
      int nextDigit = square - digit;
      if (state[nextDigit-1] && (nextDigit > 0) && (nextDigit<=n))
        if (step(state, solution, squares, nextDigit, n))
          return true;
    }
    
    state[digit-1] = true;
    solution.pop_back();
    return false;
}

std::vector<int> square_sums_row(int n)
{
  bool state[n];
  for (int i=0; i<n; i++)
    state[i] = true;
    
  std::vector<int> solution; 
  std::vector<int> squares;
  for (int i=45; i>1; i--)
    if (i*i < 2*n)
        squares.push_back(i*i);
  
  if (initial[n-1] != 0)
    if (step(state, solution, squares, initial[n-1], n))
      return solution;
  
  return std::vector<int>();
}
______________________________________________________________________-
#include <list>
#include <math.h>
#include <limits.h>

class Vertex
{
private:
    std::list<Vertex*> backupEdges;
public:
    int value;
    bool visited;
    bool connectivity;
    std::list<Vertex*> edges;

    Vertex(int value) : value(value), visited(false), connectivity(false){}

    void addEdge(Vertex* toVertex)
    {
        edges.push_back(toVertex);
        toVertex->edges.push_back(this);
    }

    void removeEdge(Vertex* toVertex)
    {
        for (auto boundVertex = edges.begin(); boundVertex != edges.end(); ++boundVertex)
        {
            if (toVertex == *boundVertex)
            {
                edges.erase(boundVertex);
                break;
            }
        }
    }

    void removeAllEdges()
    {
        backupEdges = edges;
        for (auto boundVertex = edges.begin(); boundVertex != edges.end(); ++boundVertex)
        {
            (*boundVertex)->removeEdge(this);
        }
        edges.clear();
    }

    void reestablishAllEdges()
    {
        for (auto boundVertex = backupEdges.begin(); boundVertex != backupEdges.end(); ++boundVertex)
        {
            addEdge(*boundVertex);
        }
    }

    void connect()
    {
        connectivity = true;
        for (auto boundVertex = edges.begin(); boundVertex != edges.end(); ++boundVertex)
        {
            if (!(*boundVertex)->connectivity)
                (*boundVertex)->connect();
        }
    }
};

std::vector<Vertex> vertices;

bool allVisited()
{
    for (int i = 0; i<vertices.size(); ++i)
    {
        if (!vertices[i].visited)
            return false;
    }
    return true;
}

bool isGraphConnectivity(Vertex* startVertex)
{
    std::vector<Vertex*> notVisited;
    for (int i = 0; i<vertices.size(); ++i)
    {
        if (!vertices[i].visited)
        {
            vertices[i].connectivity = false;
            notVisited.push_back(&vertices[i]);
        }
    }

    startVertex->connect();

    for (int i = 0; i<notVisited.size(); ++i)
    {
        if (!notVisited[i]->connectivity)
        {
            return false;
        }
    }

    return true;
}

std::vector<int> tryToFindHamiltonianPath(Vertex* startVertex)
{
    if (!isGraphConnectivity(startVertex))
        return{};

    std::vector<int> result;

    auto edgesFromStartVertex = startVertex->edges;
    startVertex->removeAllEdges();
    startVertex->visited = true;

    if (allVisited())
        return{ startVertex->value };

    while (result.empty() && !edgesFromStartVertex.empty())
    {
        Vertex* vertexWithMinEdges = nullptr;
        size_t minEdgesCount = INT_MAX;
        auto vertexWithMinEdgesIt = edgesFromStartVertex.begin();
        for (auto boundVertex = edgesFromStartVertex.begin(); boundVertex != edgesFromStartVertex.end(); ++boundVertex)
        {
            size_t boundVertexEdgesCount = (*boundVertex)->edges.size();
            if (boundVertexEdgesCount < minEdgesCount)
            {
                vertexWithMinEdges = *boundVertex;
                minEdgesCount = boundVertexEdgesCount;
                vertexWithMinEdgesIt = boundVertex;
            }
        }

        result = tryToFindHamiltonianPath(vertexWithMinEdges);
        edgesFromStartVertex.erase(vertexWithMinEdgesIt);
    }

    if (result.empty())
    {
        startVertex->reestablishAllEdges();
        startVertex->visited = false;
    }
    else
    {
        result.push_back(startVertex->value);
    }

    return result;
}

bool isSquare(int n)
{
    double root = sqrt(n);
    return root == floor(root);
}

std::vector<int> square_sums_row(int n)
{
    std::vector<int> result(n);
    
    vertices.clear();
    vertices.reserve(n + 1);
    vertices.push_back(0);

    for (int i=1; i<=n; ++i)
    {
        vertices.push_back(i);
        vertices[0].addEdge(&vertices[i]);
    }

    for (int i = 1; i <= n-1; ++i)
    {
        for (int j = i+1; j <= n; ++j)
        {
            if (isSquare(i + j))
            {
                vertices[i].addEdge(&vertices[j]);
            }
        }
    }

    result = tryToFindHamiltonianPath(&(vertices[0]));
    if (!result.empty())
        result.resize(result.size() - 1);

    return result;
}
