using System;

public class Matrix
{

  public static int Determinant(int[][] matrix)
  {
    int det = 0;
    if (matrix.Length != matrix[0].Length)
      return -1;
    if (matrix.Length == 1)
      return matrix[0][0];

    for (int i = 0; i < matrix.Length; i++)
      det += (int)Math.Pow(-1, i) * matrix[0][i] * Determinant(Minor(matrix, i));

    return det;
  }

  public static int[][] Minor(int[][] matrix, int pos)
  {
    int[][] minor = new int[matrix.Length - 1][];
    for (int i = 0; i < minor.Length; i++)
      minor[i] = new int[minor.Length];

    for (int i = 1; i < matrix.Length; i++)
    {
      for (int j = 0; j < pos; j++)
        minor[i - 1][j] = matrix[i][j];
      for (int j = pos + 1; j < matrix.Length; j++)
        minor[i - 1][j - 1] = matrix[i][j];
    }
        return minor;
  }
}
_____________________________________________
using System;

public class Matrix
{
   public static int[][] Minor(int[][] matrix, int pos)
   {
      int[][] minor = new int[matrix.Length - 1][];
      for(int i = 0; i < minor.Length; i++)
      {
          minor[i] = new int[minor.Length];  
      }
       
      for(int i = 1; i < matrix.Length; i++)
      {
          for(int j = 0; j < pos; j++)
          {
              minor[i -1][j] = matrix[i][j];
          }
          for(int j = pos + 1; j < matrix.Length; j++)
          {
              minor[i - 1][j - 1] = matrix[i][j];
          }
      }
     
      return minor;
   }
  
   public static int Determinant(int[][] matrix)
   {
       int det = 0;
       if(matrix.Length != matrix[0].Length) return -1;
       if(matrix.Length == 1) return matrix[0][0];
     
       for(int i = 0; i < matrix.Length; i++)
       {
           det+= (int)Math.Pow(-1, i) * matrix[0][i] * Determinant(Minor(matrix, i));         
       }
     
       return det;
   }
}
_____________________________________________
using System;
using System.Collections.Generic;
using System.Linq;

public class Matrix
{
  public static int Determinant(int[][] matrix)
  {
    int sum = 0;
    
    if (matrix.Length == 1)
      return matrix[0][0];
    
    else
      for (int i = 0; i < matrix.Length; i++)
        sum += matrix[0][i] * (int)Math.Pow(-1, i) * Determinant(Minor(matrix, i));

    return sum;
  }
  
  private static int[][] Minor(int[][] matrix, int index)
  {
    int[][] minor = new int[matrix.Length - 1][];
    
    for (int i = 0; i < minor.Length; i++)
      minor[i] = new int[minor.Length];

    for (int i = 1; i < matrix.Length; i++)
    {
      for (int j = 0; j < index; j++)
        minor[i - 1][j] = matrix[i][j];
      for (int j = index + 1; j < matrix.Length; j++)
        minor[i - 1][j - 1] = matrix[i][j];
    }
    
    return minor;
  }
}
_____________________________________________
public class Matrix
{
    public static int Determinant(int[][] matrix)
    {
        if (matrix.Length == 1)
        {
            return matrix[0][0];
        }
        
        if (matrix.Length == 2)
        {
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0];
        }

        int res = 0;
        int sign = 1;
        for (int i = 0; i < matrix[0].Length; i++)
        {
            res += sign * matrix[0][i] * Determinant(Minor(matrix, i));
            sign *= -1;
        }

        return res;
    }

    public static int[][] Minor(int[][] matrix, int index)
    {
        var len = matrix.Length - 1;
        int[][] result = new int[len][];

        // Initialize
        for (int c = 0; c < len; c++)
        {
            result[c] = new int[len];
        }

        for (int i = 0; i < result.Length; i++)
        {
            int x = 0;
            for (int j = 0; j < result.Length; j++)
            {
                if (x == index)
                    x++;

                result[i][j] = matrix[i + 1][x];
                x++;
            }
        }
        return result;
    }
}
_____________________________________________
public class Matrix
{
   public static int Determinant(int[][] matrix)
   {
       if(matrix[0].Length == 1)
           return matrix[0][0];
       return DetHelper(matrix);
   }
   
   public static int DetHelper(int[][] matrix)
   {
       int l = matrix[0].Length;
       if(l == 2)
           return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0];
           
       int total = 0;
       for(int i = 0; i < l; i++)
       {
           if(i % 2 == 0)
               total += matrix[0][i] * DetHelper(RemoveColumn(matrix, i));
           else
               total -= matrix[0][i] * DetHelper(RemoveColumn(matrix, i));
       }
       return total;
   }
   
   public static int[][] RemoveColumn(int[][] matrix, int column)
   {
       int l = matrix[0].Length;
       int[][] newMatrix = new int[l - 1][];
       for(int i = 0; i < l - 1; i++)
           newMatrix[i] = new int[l - 1];
       
       for(int i = 1; i < l; i++)
       {
           int count = 0;
           for(int j = 0; j < l; j++)
           {
               if(j == column) continue;
               newMatrix[i - 1][count] = matrix[i][j];
               count++;
           }
       }
       return newMatrix;
   }
}
