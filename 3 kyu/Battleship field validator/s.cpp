52bb6539a4cf1b12d90005b7


using namespace std;
bool validate_battlefield(vector< vector<int> > field) {
  int shiplengthnumber[5], row=0, col=0, length=0;
  for (int i=0; i<=4;i++) shiplengthnumber[i]=0; //initialize array
  for (int i=0; i <10; i++)
    for (int j=0; j<10; j++,length=0){
      if (field[i][j]==0)continue;
      if (j+1==10 || field[i][j+1]==0) //if ship does not go right then it goes down or is submarine
        for (row=i, col=j; field[row][col]; row++){
          length++;
          field[row][col]=0;
          if ((row+1<10&&col-1>=0&&field[row+1][col-1])||(row+1<10&&col+1<10&&field[row+1][col+1])) return false;//?touching ships
        }
      else // ship goes right
        for (row=i, col=j; field[row][col]; col++){
          length++;
          field[row][col]=0;
          if ((row+1<10&&col-1>=0&&field[row+1][col-1])||(row+1<10&&col+1<10 &&field[row+1][col+1])) return false;//?touching ships
        }
      if (length >= 5) return false;
      shiplengthnumber[length]++;
    }
  if (shiplengthnumber[1]==4&&shiplengthnumber[2]==3&&shiplengthnumber[3]==2&&shiplengthnumber[4]==1)  return true;
  return false;
}
____________________________________________________________
#include <iostream>
#include <vector>

using namespace std;

enum ShipType {
  BattleShip = 4,
  Cruiser = 3,
  Destroyer = 2,
  Submarine = 1
};

bool validate_battlefield(vector< vector<int> > field) {
  std::map<ShipType, int> ships{
    { BattleShip,   1 },
    { Cruiser,      2 },
    { Destroyer,    3 },
    { Submarine,    4 }
  };

  for (int i = 0; i < 10; i++) {
    field[i].insert(field[i].begin(), 0);
    field[i].insert(field[i].end(), 0);
  }
  field.insert(field.begin(), { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 });
  field.insert(field.end(), { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 });

  //hor find
  int count = 0;
  for (int i = 1; i < 11; i++) {
    for (int j = 1; j < 11; j++) {
      if (field[i][j] == 1) {
        if (field[i + 1][j] == 0 && field[i - 1][j] == 0)
          count++;
      }
      else {
        if (count > 1 && count < 5)
          ships[(ShipType)count] --;
        count = 0;
      }
    }
  }

  //ver find
  count = 0;
  for (int i = 1; i < 11; i++) {
    for (int j = 1; j < 11; j++) {
      if (field[j][i] == 1) {
        if (field[j][i + 1] == 0 && field[j][i - 1] == 0)
          count++;
      }
      else {
        if (count > 1 && count < 5) 
          ships[(ShipType)count] --;
        count = 0;
      }
    }
  }

  //find Submarine
  count = 0;
  for (int i = 1; i < 11; i++) {
    for (int j = 1; j < 11; j++) {
      if (field[i][j] == 1) {
        if (field[i + 1][j] == 0 && field[i - 1][j] == 0 && field[i][j + 1] == 0 && field[i][j - 1] == 0
          && field[i + 1][j + 1] == 0 && field[i - 1][j - 1] == 0 && field[i - 1][j + 1] == 0 && field[i + 1][j - 1] == 0) {
          ships[Submarine] --;
        }
      }
    }
  }

  bool result = true;
  for (auto sh : ships)
    if (sh.second != 0)
      result = false;

  return result;
}
____________________________________________________________
using namespace std;

bool validate_battlefield(vector<vector<int>> field)
{
 vector<int> x;
 
 for(unsigned i=0; i != 10; i++)
   for(unsigned j=0; j != 10; j++)
     if( field[i][j] == 1 )
     {
       // A 1-cell cannot be adjacent to other 1-cells either diagonally,
       // or orthogonally in both directions (L-shape):
       if(   i != 0 && j != 0 && (field[i-1][j-1] || field[i][j-1] && field[i-1][j])
          || i != 0 && j != 9 && (field[i-1][j+1] || field[i][j+1] && field[i-1][j])
          || i != 9 && j != 0 && (field[i+1][j-1] || field[i][j-1] && field[i+1][j])
          || i != 9 && j != 9 && (field[i+1][j+1] || field[i][j+1] && field[i+1][j]) )
         return false;
       
       // Note this 1-cell's position in its ship:
       field[i][j] = 1 + max(i==0 ? 0 : field[i-1][j], j==0 ? 0 : field[i][j-1]);
       x.push_back(field[i][j]);
     }
 
 return count(x.begin(), x.end(), 1) == 10 // should have exactly 10 1-cells occupying the first position in their ships 
     && count(x.begin(), x.end(), 2) == 6  // and 6 occupying the second position in their ships
     && count(x.begin(), x.end(), 3) == 3  // and 3 in 3rd position
     && count(x.begin(), x.end(), 4) == 1; // and 1 in the unique battleship's 4th position
}
____________________________________________________________
#include <vector>
bool validate_battlefield(std::vector< std::vector<int> > a) {
int ship[] =  {4,3,2,1};
for (int r=0;r<10;r++)
  for(int c=0;c<10;c++){
    if(a[r][c]==0)continue;
    int n=1, m=1;
    while(c+n<10 && a[r][c+n]==1)n++;
    while(r+m<10 && a[r+m][c]==1)m++;
    if (n>4 || m>4 || (n>1 && m>1))return false;
    if (m==1 && r<9) for(int i=c-1;i<=c+n;i++) if (i>=0 && i<=9 && a[r+1][i]==1)return false;
    if (n==1 && c<9) for(int i=r-1;i<=r+m;i++) if (i>=0 && i<=9 && a[i][c+1]==1)return false;
    int size= n==1?m-1: n-1;
    ship[size]--;
    if (ship[size]<0)return false;
    for (int i=r;i<r+m;i++) for (int j=c;j<c+n;j++) a[i][j]=0;
  }
  return ship[0]==0 && ship[1]==0 && ship[2]==0 && ship[3]==0 ;
}
