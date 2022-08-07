58c5577d61aefcf3ff000081


using System;
using System.Linq;

public class RailFenceCipher
{
   public static string Encode(string s, int n)
   {
       var mod = (n - 1) * 2;
       return string.Concat(s.Select((c, i) => new { c, i }).OrderBy(a => Math.Min(a.i % mod, mod - a.i % mod)).Select(a => a.c));
   }

   public static string Decode(string s, int n)
   {
       var mod = (n - 1) * 2;
       var pattern = Enumerable.Range(0, s.Length).OrderBy(i => Math.Min(i % mod, mod - i % mod));
       return string.Concat(s.Zip(pattern, (c, i) => new { c, i }).OrderBy(a => a.i).Select(a => a.c));
   }
}
_____________________________
using System;
using System.Collections.Generic;
using System.Linq;
public class RailFenceCipher
{
    private static IEnumerable<T> Fencer<T>(int n, IEnumerable<T> str)
    {
        var rails = Enumerable.Range(0, n).Select(r => new List<T>()).ToList();
        int[] data = { 0, 1 };
        int x = 0, dx = 1;
        foreach (var t in str)
        {
            rails[data[x]].Add(t);
            if (data[x] == n - 1 && data[dx] > 0 || data[x] == 0 && data[dx] < 0)
                data[dx] *= -1;
            data[x] += data[dx];
        }
        return rails.SelectMany(lst => lst);
    }

    public static string Encode(string s, int n) => new string(Fencer(n, s).ToArray());

    public static string Decode(string s, int n)
    {
        char[] arr = new char[s.Length];
        int[] j = { 0 };
        Fencer(n, Enumerable.Range(0, s.Length)).ToList().ForEach(i => arr[i] = s[j[0]++]);
        return new string(arr);
    }
}
_____________________________
using System;
using System.Collections.Generic;
public class RailFenceCipher
{
   public static string Encode(string s, int n)
   {
     return Solve(s, n, true);
   }

   public static string Decode(string s, int n)
   {
     return Solve(s, n, false);
   }
  
   public static string Solve(string s, int n, bool isEncode){
     int position = 0;
     int pivot = 0;
     int steps = n * 2 - 2;
     int downSteps = steps;
     int upSteps = 0;
     bool goUpSteps = false;
     char[] word = new char[s.Length];
     
     for(int i = 0; i < s.Length; i++){
       if(isEncode)
         word[i] = s[position];
       else
         word[position] = s[i];
       
       if(position + downSteps < s.Length && (!goUpSteps || upSteps == 0)){
         position += downSteps;
         goUpSteps = true;
       }
       else if(position + upSteps < s.Length && goUpSteps && upSteps != 0){
         position += upSteps;
         goUpSteps = false;
       }
       else{
         pivot++;
         position = pivot;
         downSteps -= 2;
         upSteps += 2;
         goUpSteps = false;
         if(downSteps == 0) downSteps = steps;
       }
     }
     
     return String.Join("", word);
   }
}

