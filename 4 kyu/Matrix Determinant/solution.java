public class Matrix {
    
    public static int determinant(int[][] m) {
        int d = 0, size = m.length;
        if (size == 1) return m[0][0];
        
        for (int n = 0 ; n < size ; n++) {
            int[][] newM = new int[size-1][size-1];
            for (int x = 1 ; x < size ; x++) for (int y = 0 ; y < size ; y++) {
                if (y == n) continue;
                newM[x-1][y + (y>n ? -1 : 0)] = m[x][y];
            }
            d += (n%2!=0 ? -1 : 1) * m[0][n] * determinant(newM);
        }
        return d;
    }
}
_____________________________________________
public class Matrix {

    public static int minor(int[][] m, int n, int[] excluded) {
        int size = m.length;
        if (n == size) return 1;
        int sum = 0;
        int sign = 1;
        for (int i = 0; i < size; i++)
            if (excluded[i] == 0) {
                excluded[i] = 1;
                sum += sign * m[n][i] * minor(m, n + 1, excluded);
                sign = - sign;
                excluded[i] = 0;
            }
        return sum;
    }
    
    public static int determinant(int[][] matrix) {
        return minor(matrix, 0, new int[matrix.length]);
    }
}
_____________________________________________
import java.util.Arrays;

public class Matrix {
    
    public static int determinant(int[][] matrix) {
        if (matrix.length == 1) return matrix[0][0];
        
        boolean[] activeCols = new boolean[matrix.length];
        Arrays.fill(activeCols, true);
        return determinant(matrix, 0, activeCols);
    }
    
    private static int determinant(int[][] matrix, int depth,  boolean[] activeCols) {
        if (depth == matrix.length - 1) {
            for (int col = 0; col < matrix.length; col++) {
                if (activeCols[col]) {
                    return matrix[depth][col];
                }
            }
        }
        
        int sign = 1;
        int det = 0;
        for (int col = 0; col < activeCols.length; col++) {
            if (activeCols[col]) {
                activeCols[col] = false;
                det += sign * matrix[depth][col] * determinant(matrix, depth + 1, activeCols);
                activeCols[col] = true;
                
                sign = -sign;
            }
        }
        
        return det;
    }
}
_____________________________________________
public class Matrix{
  public static int determinant(int[][] m){
    if(m.length == 1) return m[0][0];
    int d = 0, k, l;
    for(int j = 0; j < m.length; j++){
      int[][] n = new int[m.length-1][m.length-1];
      for(k = 0; k < m.length; k++) for(l = 0; l < m.length; l++)
        if(k != 0 && l != j) n[k-((k>0)?1:0)][l-((l>j)?1:0)] = m[k][l];
      d += ((j % 2 == 0)?1:-1) * m[0][j] * determinant(n);
    }
    return d;
  }
}
