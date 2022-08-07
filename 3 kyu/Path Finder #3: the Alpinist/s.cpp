576986639772456f6f00030c
  
  
#include <cmath>
#include <queue>
// solve the shortest path --> Dijkstra algorithm
int V; // real nums of vertices
const int NUM = 50000;  // set the maximum nums of vertices is 50000
int go[4][2] = {
    0, 1,
    1, 0,
    0, -1,
    -1, 0
};

struct node{  
    int next, c; 
    bool operator<(const node &o) const{
        return c > o.c;
    }
};    

int dijkstra(std::vector<node> edge[NUM], int src) { 
    std::priority_queue<node> Q; 
    std::vector<int>dist(V, -1);
    dist[src] = 0; 
    node tmp;
    tmp.next = src;
    tmp.c = dist[src];
    Q.push(tmp);
    
    while ( !Q.empty() ) { 
        tmp = Q.top();
        Q.pop();
        int u = tmp.next;
        if ( u == V - 1 ) return dist[u];
        for (int i = 0; i < edge[u].size(); i++) {
            int v = edge[u][i].next;
            int c = edge[u][i].c;
            if (dist[v] == -1 || dist[u] + c < dist[v]){
                dist[v] = dist[u] + c; 
                tmp.c = dist[v], tmp.next = v;
                Q.push(tmp);
            }
        }
     } 
     return dist[V - 1];
}

int path_finder(std::string maze) {
    int length = std::floor( std::sqrt( (double) maze.size() ) );
    std::cout << length << std::endl;
    V = length * length;
    std::vector<node> edge[NUM];
    for ( int i = 0; i < V; i++ ) edge[i].clear();
    for ( int x = 0; x < length; x++ ) {
        for ( int y = 0; y < length; y++ ) {
            for ( int i = 0; i < 4; i++ ) {
                int nx = x + go[i][0];
                int ny = y + go[i][1];
                if ( nx < 0 || nx >= length || ny < 0 || ny >= length ) continue;
                node tmp;
                tmp.next = nx * length + ny;
                tmp.c = std::abs(maze[nx * ( length + 1 )+ ny] - maze[x * ( length + 1 ) + y]);
                edge[x * length + y].push_back(tmp);
            }
        }
    }
    
    int src = 0;
    return dijkstra(edge, src); 
}
_____________________________
#include <string>
#include <vector>
#include <queue>

using namespace std;


struct Node {
    int row;
    int col;
    int val;
};

class CompareByValue
{
public:
    bool operator() (Node left, Node right)
    {
        return left.val>right.val;
    }
};


int path_finder(std::string maze)
{
  
  if (maze.size()==1) return 0;

  int n=maze.find("\n");   
  vector<vector<int>> heightMap(n, vector<int>(n, -1));
  vector<vector<int>> visited(n, vector<int>(n, 0));
  
  int row = 0, col = 0;
  for (auto& c : maze) {
    if (c=='\n'){
      row++; 
      col = 0;
    }else{
      heightMap[row][col] = c - '0';
      col++;
    }
  }  
  
  priority_queue<Node, vector<Node>, CompareByValue> pq;  
  pq.push({0,0,0});  
    
  // Coord-offsets:   E,  S,  W,  N
  const int drow[] = {0,  1,  0, -1};
  const int dcol[] = {1,  0, -1,  0};
    
  while(!pq.empty()){
    
    Node node = pq.top();
    pq.pop();
    
    if (node.row==n-1 && node.col==n-1){
      return node.val;
    }
      
    visited[node.row][node.col]=1;     
     
    for (int k = 0; k < 4; ++k) {
       int row = node.row + drow[k];
       int col = node.col + dcol[k];
        
       if (row >= 0 && col >= 0 && row < n && col < n && visited[row][col] == 0) {
         int newVal = node.val + abs(heightMap[node.row][node.col]-heightMap[row][col]);
         pq.push({row,col,newVal});
       }
    }
     
     
  }
  
  
  return 0;
}
_____________________________
#include <iostream>
#include <vector>
#include <limits>
#include <string>

using namespace std;

int path_finder(std::string maze)
{
        int N = 0, gSize =0; // maze dimentions   
        vector <int> c_maze; // maze
        
        for (char &c : maze)
        {
                if (c == '\n'){
                        N++;
                        continue;
                }
                c_maze.push_back (c - '0'); // convert char to int 
        }
        N++ ; // one more 
        gSize = c_maze.size();

        struct vertex
        {
                vector <int> nIndx; // neighbors (indexes) 
                vector <int> nDist; // distances (value diff)
        };
        
        vector<vertex> graph (gSize);    
        
        for (int i = 0; i < gSize; i++)
        {
                vector <int> indxs; 
                if (i - N >= 0) indxs.push_back(i-N); 
                if (i - 1 >= 0 && (i%N != 0)) indxs.push_back(i-1); 
                if (i + N < gSize) indxs.push_back(i+N); 
                if (i + 1 < gSize && ((i+1)%N != 0)) indxs.push_back(i+1); 

                for (int j : indxs){
                        graph[i].nIndx.push_back(j);
                        int d = c_maze[i] - c_maze[j];
                        d = (d < 0) ? d * (-1) : d; // like abs func
                        graph[i].nDist.push_back(d);
                }
        }

        // distance vector. expecte to get solution on last element 
        vector<int> dist (gSize, INT32_MAX);
        vector<bool> mark (gSize, false);         
        dist [0] = 0; 

        for (int i = 0; i < gSize; i++)
        {       
                int v = -1 ; 
                for (int j = 0; j < gSize; j++) {
                        if (!mark[j] && (v == -1 || dist[j] < dist[v]) )
                                v=j; 
                }
                if (dist[v] == INT32_MAX) break; 
                mark [v] = true;

                vertex &vtx = graph[v];
                for (size_t j = 0; j < vtx.nIndx.size(); j++)
                {
                        int to = vtx.nIndx[j]; 
                        int len = vtx.nDist[j]; 
                        if (dist[v] + len < dist[to])
                                dist[to] = dist[v] + len;  
                }
                
        }

        return dist.back() ;
}
