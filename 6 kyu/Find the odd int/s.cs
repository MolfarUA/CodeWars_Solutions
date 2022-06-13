using System.Linq;

namespace Solution
{
  class Kata
    {
      public static int find_it(int[] seq) 
      {
        return seq.GroupBy(x => x).Single(g => g.Count() % 2 == 1).Key;
      }
    }
}
_______________________________
namespace Solution
{
  class Kata
  {
        public static int find_it(int[] seq)
        {
            int found = 0;

            foreach (var num in seq)
            {
                found ^= num;
            }

            return found;
        }
  }
}
_______________________________
using System.Linq;


namespace Solution
{
  class Kata
    {
    public static int find_it(int[] seq) 
      {
        return  seq.First(x => seq.Count(s => s == x) % 2 == 1);
      }
       
    }
}
_______________________________
using System.Linq;

namespace Solution
{
    class Kata
    {
        public static int find_it(int[] seq) 
        {
            return seq.Aggregate(0, (a, b) => a ^ b);
        }
    }
}
_______________________________
namespace Solution
{
  class Kata
    {
    public static int find_it(int[] seq) 
      {
      int counter = 0;
      //iterate through the list
      foreach(int i in seq)
      {
      counter = 0;
        for(int r = 0; r < seq.Length; r++)
        {
          //count the number of times it occurs
          if(i == seq[r]){ counter++; }
        }
        if(!(counter % 2 == 0)){ return i; }
      }
      
      return -1;
      }
       
    }
}
_______________________________
using System.Collections.Generic;

namespace Solution
{
  class Kata
    {
    public static int find_it(int[] seq) 
      {
        Dictionary<int, int> numbersWithTimes = new Dictionary<int, int>();
        
        foreach(var number in seq)
        {
          if(!numbersWithTimes.ContainsKey(number))
          {
            numbersWithTimes.Add(number, 1);
          }
          else
          {
            numbersWithTimes[number]++;
          }
        }
        
        foreach(KeyValuePair<int, int> item in numbersWithTimes)
        {
          if(item.Value % 2 == 1)
            return item.Key;
        }
        
        return -1;
      }      
    }
}
