52bb6539a4cf1b12d90005b7


public class BattleField {
        
    private static int xy(int[][] arr, int x, int y) {
      return (x < 0 || x >= arr[0].length || y < 0 || y >= arr.length) ? 0 : arr[y][x];
    }
    
    public static boolean fieldValidator(int[][] f) {
    
        // Validate the ship's surroundings
        // --------------------------------
        for (int y = 0; y < f.length; y++) {
          for (int x = 0; x < f[y].length; x++) {
          
            if (xy(f, x, y) == 1) {
              // Cannot allow a mix of horizontal and vertical
              final boolean v = xy(f, x, y-1) != 0 || xy(f, x, y+1) != 0; // look up/down
              final boolean h = xy(f, x-1, y) != 0 || xy(f, x+1, y) != 0; // look left/right
              if (h && v) return false;
              if (v) f[y][x] = -1; // using -1 to represent "vertical" ships
            
              // Cannot be anything diagonally adjacent this cell
              if (xy(f, x-1, y-1) != 0 || xy(f, x+1, y-1) != 0 || xy(f, x+1, y+1) != 0 || xy(f, x-1, y+1) != 0) return false;
            }
          }
        }
        
        // Count ships of various expected lengths
        // ---------------------------------------
        final int[] shipCounts = {0, 4, 3, 2, 1};
        // horizontal ships
        for (int y = 0; y < f.length; y++) {
          for (int x = 0; x < f[y].length; x++) {
            if (xy(f, x, y) == 1) {
              int len = 1;
              while (xy(f, ++x, y) == 1) len++;
              if (len > 4) return false; // ship too big
              shipCounts[len]--;
            }
          }
        }
        // vertical ships
        for (int x = 0; x < f[0].length; x++) {
          for (int y = 0; y < f.length; y++) {
            if (xy(f, x, y) == -1) {
              int len = 1;
              while (xy(f, x, ++y) == -1) len++;
              if (len > 4) return false; // ship too big
              shipCounts[len]--;
            }
          }
        }        
        // Check expected ship counts
        for (int count : shipCounts) if (count != 0) return false;
        return true;
    }
}
____________________________________________________________
public class BattleField {
    public static boolean fieldValidator(int[][] field) {
        return new FieldValidator(field).validate();
    }
}
class FieldValidator {
    private int[][] field;
    private int[] ships = {0,4,3,2,1};
    
    public FieldValidator(int[][] field) {this.field = field;}
    public boolean validate() { 
        for (int i = 0; i < 10; i++) 
            for (int j = 0; j < 10; j++) 
                if(field[i][j] == 1) 
                    if (!isShipValid(i,j)) return false;
        return java.util.Arrays.equals(ships, new int[]{0,0,0,0,0});
    }
    
    private boolean isShipValid(int i, int j) {
        boolean isHorisontal = j<9 && field[i][j+1]==1;
        int length = getShipLength(i, j, isHorisontal);
        if (length > 4) return false;
        ships[length]--;
        if (!isLineEmpty(i-1, true, j-1, isHorisontal ? length+1 : 2)) return false;
        return isLineEmpty(j-1, false, i-1, isHorisontal ? 2 : length+1);
    }
    
    private int getShipLength(int i, int j, boolean isHorisontal) {
        int n = 0;
        while(i < 10 && j < 10 && field[i][j] == 1) {
            n++;
            field[i][j] = 2;
            if (isHorisontal) j++; else i++;
        }
        return n;
    }
    
    private boolean isLineEmpty(int line, boolean isHorisontal, int start, int length){
        if (line == -1) return true;
        int end = (start + length) < 9 ? start + length : 9;
        for (int i = (start > 0) ? start : 0; i <= end; i++) 
            if (field [isHorisontal ? line : i] [isHorisontal ? i : line] !=0) return false;
        return true;
    }
}
____________________________________________________________
import java.util.*;

public class BattleField {
    
    public static boolean fieldValidator(int[][] field) {

        int battleShip = 1;
        int cruiser = 2;
        int destroyer = 3;
        int submarine = 4;

        for (int x = 0; x < field.length; x++) {
            for (int y = 0; y < field[x].length; y++) {
                if (field[x][y] == 1) {
                    int count = 0;
                    if (y + 1 <= 9 && field[x][y + 1] == 1) {
                        for (int y1 = y; y1 < field[x].length; y1++) {
                            if (field[x][y1] == 1) {
                                boolean con1 = x + 1 <= 9 && y1 + 1 <= 9 && field[x + 1][y1 + 1] == 1;
                                boolean con2 = x + 1 <= 9 && y1 - 1 >= 0 && field[x + 1][y1 - 1] == 1;
                                if (con1 || con2) return false;
                                
                                count++;
                                field[x][y1] = 2;
                                
                            } else break;
                        }

                    } else {
                        for (int x1 = x; x1 < field.length; x1++) {
                            if (field[x1][y] == 1) {
                                boolean con1 = x1 + 1 <= 9 && y + 1 <= 9 && field[x1 + 1][y + 1] == 1;
                                boolean con2 = x1 + 1 <= 9 && y - 1 >= 0 && field[x1 + 1][y - 1] == 1;
                                if (con1 || con2) return false;

                                count++;
                                field[x1][y] = 2;

                            } else break;
                        }
                    }

                    switch (count) {
                        case 1:
                            submarine = submarine - 1;
                            if (submarine < 0) return false;
                            break;
                        case 2:
                            destroyer = destroyer - 1;
                            if (destroyer < 0) return false;
                            break;
                        case 3:
                            cruiser = cruiser - 1;
                            if (cruiser < 0) return false;
                            break;
                        case 4:
                            battleShip = battleShip - 1;
                            if (battleShip < 0) return false;
                            break;
                        default:
                            return false;
                    }
                }
            }
        }

        return battleShip == 0 && cruiser == 0 && destroyer == 0 && submarine == 0;
    }
    
}
