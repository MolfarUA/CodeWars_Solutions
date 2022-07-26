536a155256eb459b8700077e


using System;
public class TheClockwiseSpiral
{
    public static int[,] CreateSpiral(int N)
    {
        int[,] matrix = new int[N,N];
        int numValue = 1;
        int c1 = 0, c2 = N - 1;
            while (numValue <= N * N)
            {
                //Right Direction Move  
                for (int i = c1; i <= c2; i++)
                    matrix[c1, i] = numValue++;
                //Down Direction Move  
                for (int j = c1 + 1; j <= c2; j++)
                    matrix[j, c2] = numValue++;
                //Left Direction Move  
                for (int i = c2 - 1; i >= c1; i--)
                    matrix[c2, i] = numValue++;
                //Up Direction Move  
                for (int j = c2 - 1; j >= c1 + 1; j--)
                    matrix[j, c1] = numValue++;
                c1++;
                c2--;
            }
        return matrix;
    }
}
_________________________
using System;
public class TheClockwiseSpiral
{
    public static int[,] CreateSpiral(int N)
    {
        int[,] result = new int[N, N];
        if ((N & 1) == 1)
            result[N / 2, N / 2] = N * N;
        int count = 0;
        for (int l = 0; l < N / 2; l++)
        {
            for (int a = l; a < N - 1 - l; a++)
            {
                count++;
                result[l, a] = count;
            }
            for (int b = l; b < N - 1 - l; b++)
            {
                count++;
                result[b, N - 1 - l] = count;
            }
            for (int c = N - 1 - l; c > l; c--)
            {
                count++;
                result[N - l - 1, c] = count;
            }
            for (int d = N - 1 - l; d > l; d--)
            {
                count++;
                result[d, l] = count;
            }
        }
        return result;
    }
}
_________________________
using System;
using System.Collections.Generic;
using System.Linq;

public class TheClockwiseSpiral
{
    public static int[,] CreateSpiral(int size)
    {
        var spiral = new int[size, size];
        var j = 0;
        foreach (var p in Walk(-1, 0, 1, 0, size))
        {
            spiral[p.y, p.x] = ++j;
        }
        return spiral;   
        IEnumerable<(int x, int y)> Walk(int x, int y, int dx, int dy, int l)
        {
            if (l <= 0) yield break;
            for (var i = 0; i < l; i++) 
            {
                x += dx;
                y += dy;
                if (x >= 0) yield return (x, y);
                if (l == 0) yield break;
            }
            foreach (var next in Walk(x, y, -dy, dx, dy == 0 ? l - 1 : l)) 
            {
                yield return next;
            }
        }
    }
}
