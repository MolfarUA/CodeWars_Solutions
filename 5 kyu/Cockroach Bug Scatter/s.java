59aac7a9485a4dd82e00003e


public class Dinglemouse {

  public static int[] cockroaches(final char[][] room) {
    int[] roachesInHole = new int[10];
    for(int y = 1; y < room.length-1; y++){
      for(int x = 1; x < room[y].length-1; x++){
        //Scan the room for roaches
        if(room[y][x] != ' '){
          //Roach found... let's see where it goes to
          roachesInHole[findRoachHole(y,x,room)]++;
        }
      }
    }
    return roachesInHole;
  }
  
  private static int findRoachHole(int y, int x, char[][] room){
    switch(room[y][x]){
      case 'U':
        return runAlongEdgeUntilHoleFound(0,x,room);
      case 'D':
        return runAlongEdgeUntilHoleFound(room.length-1,x,room);
      case 'L':
        return runAlongEdgeUntilHoleFound(y,0,room);
      case 'R':
        return runAlongEdgeUntilHoleFound(y,room[y].length-1,room);
    }
    return -1;
  }
  
  private static int runAlongEdgeUntilHoleFound(int y, int x, char[][] room){
    while(!Character.isDigit(room[y][x])){
      if(y == 0 && x > 0) x--;
      else if(x == 0 && y < room.length-1) y++;
      else if(y == room.length-1 && x < room[y].length-1) x++;
      else if(x == room[y].length-1 && y > 0) y--;
    }
    return Character.getNumericValue(room[y][x]);
  }
  
}
________________________________
import java.util.List;
import java.util.ArrayList;
import java.util.LinkedList;

public class Dinglemouse {

  public static int[] cockroaches(final char[][] room) {
    
    List<LinkedList<Integer>> walls = new ArrayList<>(4);
    for (int i = 0; i < 4; i++) {
      walls.add(new LinkedList<>());
    }
      
      int[] resultArray = new int[10];
      int width = room[0].length;
      int height = room.length;
      boolean endSearch;
      
      //search digits on upper wall
      for (int j = width - 1; j >= 0; j--) {
        if (room[0][j] >= 48 && room[0][j] <= 57) {
          walls.get(0).add(j);
        }
      }
      
      //search digits on left wall
      for (int i = 0; i < height; i++) {
        if (room[i][0] >= 48 && room[i][0] <= 57) {
          walls.get(1).add(i);
        }
      }
      
      //search digits on lower wall
      for (int j = 0; j < width; j++) {
        if (room[height - 1][j] >= 48 && room[height - 1][j] <= 57) {
          walls.get(2).add(j);
        }
      }
      
    //search digits on right wall
      for (int i = height - 1; i >= 0; i--) {
        if (room[i][width - 1] >= 48 && room[i][width - 1] <= 57) {
          walls.get(3).add(i);
        }
      }
      
      //search cockroaches and count its amount in holes
      for (int i = 1; i < height - 1; i++) {
        for (int j = 1; j < width - 1; j++) {
          endSearch = false;
          if (room[i][j] == 'U') {
            if (walls.get(0).size() > 0) {
              for (int index : walls.get(0)) {
                if (j >= index) {
                  resultArray[room[0][index] - 48]++;
                  endSearch = true;
                  break;
                }
              }
              
            }
            if (walls.get(1).size() > 0 && !endSearch) {
              resultArray[room[walls.get(1).getFirst()]
                  [0] - 48]++;
              endSearch = true;
            }
            if (walls.get(2).size() > 0 && !endSearch) {
              resultArray[room[height - 1]
                  [walls.get(2).getFirst()] - 48]++;
              endSearch = true;
            }
            if (walls.get(3).size() > 0 && !endSearch) {
              resultArray[room[walls.get(3).getFirst()]
                  [width - 1] - 48]++;
              endSearch = true;
            }
            if (!endSearch) {
              resultArray[room[0]
                  [walls.get(0).getFirst()] - 48]++;
            }
          } else if (room[i][j] == 'L') {
            if (walls.get(1).size() > 0) {
              for (int index : walls.get(1)) {
                if (i <= index) {
                  resultArray[room[index][0] - 48]++;
                  endSearch = true;
                  break;
                }
              }
              
            }
            if (walls.get(2).size() > 0 && !endSearch) {
              resultArray[room[height - 1]
                  [walls.get(2).getFirst()] - 48]++;
              endSearch = true;
            }
            if (walls.get(3).size() > 0 && !endSearch) {
              resultArray[room[walls.get(3).getFirst()]
                  [width - 1] - 48]++;
              endSearch = true;
            }
            if (walls.get(0).size() > 0 && !endSearch) {
              resultArray[room[0]
                  [walls.get(0).getFirst()] - 48]++;
              endSearch = true;
            }
            if (!endSearch) {
              resultArray[room[walls.get(1).getFirst()]
                  [0] - 48]++;
            }
          } else if (room[i][j] == 'D') {
            if (walls.get(2).size() > 0) {
              for (int index : walls.get(2)) {
                if (j <= index) {
                  resultArray[room[height - 1][index] - 48]++;
                  endSearch = true;
                  break;
                }
              }
              
            }
            if (walls.get(3).size() > 0 && !endSearch) {
              resultArray[room[walls.get(3).getFirst()]
                  [width - 1] - 48]++;
              endSearch = true;
            }
            if (walls.get(0).size() > 0 && !endSearch) {
              resultArray[room[0]
                  [walls.get(0).getFirst()] - 48]++;
              endSearch = true;
            }
            if (walls.get(1).size() > 0 && !endSearch) {
              resultArray[room[walls.get(1).getFirst()]
                  [0] - 48]++;
              endSearch = true;
            }
            if (!endSearch) {
              resultArray[room[height - 1]
                  [walls.get(2).getFirst()] - 48]++;
            }
          } else if (room[i][j] == 'R') {
            if (walls.get(3).size() > 0) {
              for (int index : walls.get(3)) {
                if (i >= index) {
                  resultArray[room[index][width - 1] - 48]++;
                  endSearch = true;
                  break;
                }
              }
              
            }
            if (walls.get(0).size() > 0 && !endSearch) {
              resultArray[room[0]
                  [walls.get(0).getFirst()] - 48]++;
              endSearch = true;
            }
            if (walls.get(1).size() > 0 && !endSearch) {
              resultArray[room[walls.get(1).getFirst()]
                  [0] - 48]++;
              endSearch = true;
            }
            if (walls.get(2).size() > 0 && !endSearch) {
              resultArray[room[height - 1]
                  [walls.get(2).getFirst()] - 48]++;
              endSearch = true;
            }
            if (!endSearch) {
              resultArray[room[walls.get(3).getFirst()]
                  [width - 1] - 48]++;
            }
          }

        }
      }
      return resultArray;
  }
}
________________________________
public class Dinglemouse {

  public static int[] cockroaches(final char[][] room) {
    char[] walls = new char[2 * room.length + 2 * room[0].length];
    int[] res = new int[10];
    
    for (int i = room[0].length - 1; i >= 0; i--) {
      walls[room[0].length - 1 - i] = room[0][i];
    }
    for (int i = 0; i < room.length; i++) {
      walls[room[0].length + i] = room[i][0];
    }
    for (int i = 0; i < room[0].length; i++) {
      walls[room[0].length + room.length + i] = room[room.length - 1][i];
    }
    for (int i = room.length - 1; i >= 0; i--) {
      walls[2 * room[0].length + room.length + room.length - 1 - i] = room[i][room[0].length - 1];
    }
    
    for (int i = 0; i < room.length; i++) {
      for (int j = 0; j < room[i].length; j++) {
        if (room[i][j] == 'U') {
          int a = room[0].length - 1 - j;
          while(true) {
            if (Character.isDigit(walls[a])) {
              res[walls[a] - '0']++;
              break;
            }
            a++;
            if (a == walls.length) {
              a = 0;
            }
          }
        }
        else if (room[i][j] == 'L') {
          int a = room[0].length + i;
          while(true) {
            if (Character.isDigit(walls[a])) {
              res[walls[a] - '0']++;
              break;
            }
            a++;
            if (a == walls.length) {
              a = 0;
            }
          }
        }
        else if (room[i][j] == 'D') {
          int a = room[0].length + room.length + j;
          while(true) {
            if (Character.isDigit(walls[a])) {
              res[walls[a] - '0']++;
              break;
            }
            a++;
            if (a == walls.length) {
              a = 0;
            }
          }
        }
        else if (room[i][j] == 'R') {
          int a = walls.length - i - 1;
          while(true) {
            if (Character.isDigit(walls[a])) {
              res[walls[a] - '0']++;
              break;
            }
            a++;
            if (a == walls.length) {
              a = 0;
            }
          }
        }
      }
    }
    return res;
  }
}
