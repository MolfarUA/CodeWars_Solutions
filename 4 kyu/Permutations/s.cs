5254ca2719453dcc0b00027d


using System.Collections.Generic;
using System.Linq;

public class Permutations {
    public static List<string> SinglePermutations( string s ) {
        if ( s.Length < 2 ) {
            return new List<string> {s};
        }
        var result = new HashSet<string>( );
        foreach ( var sub in SinglePermutations( s.Substring( 1 ) ) ) {
            for ( int i = 0; i <= sub.Length; i++ ) {
                result.Add( sub.Substring( 0, i ) + s [ 0 ] + sub.Substring( i ) );
            }
        }
        return result.ToList( );
    }
}
______________________________
using System.Linq;
using System.Collections.Generic;

class Permutations
{
  public static List<string> SinglePermutations(string s) => $"{s}".Length < 2 ?
    new List<string> { s } :
    SinglePermutations(s.Substring(1))
      .SelectMany(x => Enumerable.Range(0, x.Length + 1)
        .Select((_, i) => x.Substring(0, i) + s[0] + x.Substring(i)))
      .Distinct()
      .ToList();
}
______________________________
using System;
using System.Collections.Generic;
using System.Linq;
class Permutations
{
   public static List<string> SinglePermutations(string s)
   {
       // Your code here!
       List<string> returnstrings = new List<string>();
       if (s.Length == 1)
       {
         returnstrings.Add(s);
       }
       else
       {
         for (int x = 0; x < s.Length; x++)
         {
           returnstrings.AddRange(SinglePermutations(s.Remove(x,1)).Select(z => s[x] +z));
         }
       }       
       
       return returnstrings.Distinct().ToList();
   }
}
