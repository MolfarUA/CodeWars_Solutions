5659c6d896bc135c4c00021e


using System;
public class Kata
{
  public static long NextSmaller(long n)
  {
    int[] a = new int[n.ToString().Length];
    int j = 0;
    // Loading digits into array so easier to work with
    while (n > 0)
    {
        a[j++] = (int)(n % 10);
        n /= 10;
    }
    
    // Strategy = go from right to left and find the first digit with a number greater to the left
    // eg 285123 - find the '1' because there's a greater number beside
    // Find the biggest number to the right, and switch the two
    // eg 285123 - switch the 5 and the 3 = 283125
    // Then, sort everything to the right of the index in descending order
    // eg 283125 -> 283521

    // find int to move
    int index = 0;
    int highest = 0;
    for(index = 1; index < a.Length; index++)
    {
        if (a[index] > a[index - 1]) break;
    }
    // find biggest digit to the right of it
    if (index >= a.Length) return -1;
    highest = index-1;
    for (int k = 0; k < index; k++)
    {
        if (a[k] > a[highest] && a[index] > a[k]) highest = k;
    }
    
    // switch index with highest
    int temp = a[index];
    a[index] = a[highest];
    a[highest] = temp;

    // take array of everything to the right of the index
    int[] b = new int[index];
    for (int i = 0; i < index; i++)
    {
        b[i] = a[i];
    }
    // sort it and copy back
    Array.Sort(b);
    for (int i = 0; i < index; i++)
    {
        a[i] = b[i];
    }

    long output = 0;
    long pos = 1;
    // convert array back into long
    for (int i = 0; i < a.Length; i++)
    {
        output += pos * a[i];
        pos *= 10;
    }
    // if we needed to move a zero to the very left, then the long will be shorter, return -1
    if (output.ToString().Length < a.Length) return -1;

    return output;
  
  }
}
_______________________________
using System;
using System.Linq;

public class Kata
{
  public static long NextSmaller(long n)
  {
    var chars = n.ToString();
    for (var i = chars.Length - 1; i > 0; i--)
    {
      if (chars[i] < chars[i - 1])
      {
        var right = chars.Skip(i).ToArray();
        var next = right.Where(a => a < chars[i - 1]).Max();
        right[Array.IndexOf(right, next)] = chars[i - 1];        
        var answer = chars.Substring(0, i - 1) + next + string.Concat(right.OrderByDescending(a => a));
        return answer[0] == '0' ? -1 : long.Parse(answer);
      }
    }    
    return -1;
  }
}
_______________________________
using System.Linq;
public class Kata
{
  public static long NextSmaller(long n)
  {
    if (n>0&(n+"").Length==1) return -1;
      string s=n+"";
      for (int i=s.Length-2;i>=0;i--){
        if (s.Substring(i)!=string.Concat(s.Substring(i).OrderBy(x=>x))){
          var t=string.Concat(s.Substring(i).OrderByDescending(x=>x));
          var c=t.First(x=>x<s[i]);
          return i==0&c=='0' ? -1 : long.Parse(s.Substring(0,i)+c+string.Concat(t.Where((x,y)=>y!=t.IndexOf(c))));
        }
      }
      return -1;
  }
}
_______________________________
using System;
using System.Collections.Generic;
using System.Linq;

public static class Kata
{
    static bool Prev(this int[] a)
    {
        int i = a.Length - 2;
        while (i >= 0 && a[i] <= a[i + 1]) i--;
        if (i < 0) return false;

        int j = a.Length - 1;
        while (a[j] >= a[i]) j--;
        a[i] ^= a[j]; a[j] ^= a[i]; a[i] ^= a[j];

        Array.Reverse(a, i + 1, a.Length - i - 1);
        return true;
    }

    public static long NextSmaller(long n)
    {
        Console.WriteLine(n);
        if (n < 10) return -1;
        var r = n.ToString().Select(c => c - '0').ToArray();
        if (!Prev(r) || r[0] == 0) return -1;
        return r.Aggregate(0L, (x, y) => 10 * x + y);
    }
}
