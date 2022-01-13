using System.Numerics;

public class Kata
{
    public static BigInteger[] GenerateDiagonal(int n, int l)
    {
      BigInteger[] diagonal = new BigInteger[l];
 
      BigInteger[,] arrPascal = new BigInteger[n+1, l+1];
      for (int i = 0; i <= n; i++)
          arrPascal[i,0] = 1;
      for (int i = 1; i <= l; i++)
          arrPascal[0, i] = 1;

      for (int i = 1; i <= n; i++)
          for (int j = 1; j <= l; j++)
              arrPascal[i, j] = arrPascal[i - 1, j] + arrPascal[i, j - 1];

      for (int i =  0; i < l; i++)
         diagonal[i] = arrPascal[n,i];
      
      return diagonal;
    }
}
_______________________________
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;

public class Kata
{
    public static BigInteger[] GenerateDiagonal(int n, int l)
    {
        if (l == 0)
        {
            return new BigInteger[] { };
        }
        var diagonalRow = n;

        BigInteger currNumb = new BigInteger(1);
        List<BigInteger> diagonal = new List<BigInteger> { currNumb };

        for (int i = 1; i < l; i++)
        {
            currNumb = currNumb * ++diagonalRow / i;
            diagonal.Add(currNumb);
        }


        return diagonal.ToArray();
    }
}
_______________________________
using System.Numerics;

public class Kata
{
    public static BigInteger[] GenerateDiagonal(int n, int l)
    {
      if (l==0) return new BigInteger[]{ };
      BigInteger[][] bi = new BigInteger[n+1][];
      for(int i = 0; i <= n; i++) {
        bi[i] = new BigInteger[n+l-i];
        bi[i][0] = 1;
        for(int b = 1; b < bi[i].Length; b++) {
          if (i == 0)
            bi[i][b] = 1;
          else
            bi[i][b] = bi[i-1][b] + bi[i][b-1];
        }
        
      }
      return bi[n] ;
    }
}
_______________________________
using System.Numerics;
public class Kata
{
    public static BigInteger[] GenerateDiagonal(int n, int l)
    {
       

    if (l == 0)
    {
        return new BigInteger[] { };
    }

        var gen = GenTriangle(n, l);

        var result = new BigInteger[l];
        int lay = n;
        for (int i = 0; i < l; i++)
        {
            result[i] = gen[lay, n];
            lay++;
        }
        
    return result;
    }
  
  static BigInteger [,] GenTriangle(int n, int l)
{
    int layers = n + l + 1;
    BigInteger[,] arr = new BigInteger [layers,layers];
    int count = 1; 
    for (int i = 0; i < layers; i++)
    {
        for (int j = 0; j < count; j++)
        {
            if (j == 0 )
            {
                arr[i,j] = 1;
            }else
            {
                arr[i,j] = arr[i - 1,j-1] + arr[i - 1,j];
            }
        }
        count++;
    }
    return arr;
}
}
_______________________________
using System.Numerics;
using System;

public class Kata
{
    public static BigInteger[] GenerateDiagonal(int n, int l)
    {
        if (l == 0) {
          return new BigInteger[] { };
        }
        if (n == 0) {
          BigInteger[] numbers = new BigInteger[l];
          for (long i = 0; i < numbers.Length; i++) {
            numbers[i] = 1;
          }
          return numbers; 
        } else {
          BigInteger[] prev_numbers = GenerateDiagonal(n - 1, l);
          BigInteger[] new_numbers = new BigInteger[l];
          new_numbers[0] = 1;
          for (long i = 1; i < prev_numbers.Length; i++) {
            new_numbers[i] = new_numbers[i - 1] + prev_numbers[i];
          }
          return new_numbers;
        }
    }
}
_______________________________
using System;
using System.Collections.Generic;
using System.Numerics;

public class Kata
{
        public static Dictionary<string, BigInteger> SavedValues = new Dictionary<string, BigInteger> { { "0|0", 1 } };

        public static BigInteger[] GenerateDiagonal(int n, int l)
        {
            if (l == 0)
                return new BigInteger[] { };

            var result = new BigInteger[l];

            for (int i = 0; i < l; i++)
            {
                result[i] = getDiagonalNumber(n, i);
            }

            return result;
        }

        // return ith number of the nth diagonal
        private static BigInteger getDiagonalNumber(int n, int i)
        {
            var key = n + "|" + i;            
            if (SavedValues.ContainsKey(key))
                return SavedValues[key];

            var alternateKey = i + "|" + n;
            if (SavedValues.ContainsKey(alternateKey))
            {
                SavedValues[key] = SavedValues[alternateKey];
                return SavedValues[key];
            }
                
            if (n == 0 || i == 0)
            {
                SavedValues[key] = 1;
                SavedValues[alternateKey] = 1;
                return 1; // first diagonal is all 1's
            }

            var num1 = getDiagonalNumber(n - 1, i);
            var num2 = getDiagonalNumber(n, i - 1);

            SavedValues[key] = num1 + num2;
            SavedValues[alternateKey] = num1 + num2;

            return SavedValues[key];
        }
}
_______________________________
using System.Numerics;

public class Kata
{
    public static BigInteger[] GenerateDiagonal(int n, int l)
    {
      if (l==0) return new BigInteger[] { };
      BigInteger[] ret = new BigInteger[l];
      ret[0]=1;
      for (int i=1;i<l;i++) {
        ret[i]=ret[i-1] * (n+i) / i;
      }
      return ret;
    }
}
