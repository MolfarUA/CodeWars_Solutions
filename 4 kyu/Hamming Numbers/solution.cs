using System;
using System.Linq;
using System.Collections.Generic;

public class Hamming
{
  public static long hamming(int n)
  {
    var next = new SortedSet<long>();
    next.Add(1);
    
    for(int i = 1; i < n; i++) 
    {
      var hamming = next.First();
      next.Remove(hamming);
      next.Add(hamming * 2);
      next.Add(hamming * 3);
      next.Add(hamming * 5);
    }
    
    return next.First();
  }
}

___________________________________________________
using System;
using System.Collections.Generic;
using System.Linq;

public class Hamming
{
  public static long hamming(int n)
  {
    var values = new SortedSet<long>();
    values.Add(1);
    
    for(int i = 1; i < n; i++) 
    {
      var firstHamming = values.First();
      values.Remove(firstHamming);
      values.Add(firstHamming * 2);
      values.Add(firstHamming * 3);
      values.Add(firstHamming * 5);
    }
    
    return values.First();
  }
    
}

___________________________________________________
using System;

public class Hamming
{
        public static long hamming(int n)
        {
            long[] hamming = new long[n];
            hamming[0] = 1;

            long time2 = 0, time3 = 0, time5 = 0;
            long multiple2 = 2, multiple3 = 3, multiple5 = 5;


            for (int i = 1; i < n; i++)
            {
                hamming[i] = Math.Min(multiple2, Math.Min(multiple3, multiple5));

                if (hamming[i] == multiple2)
                {
                    time2++;
                    multiple2 = hamming[time2] * 2;
                }
                if (hamming[i] == multiple3)
                {
                    time3++;
                    multiple3 = hamming[time3] * 3;
                }

                if (hamming[i] == multiple5)
                {
                    time5++;
                    multiple5 = hamming[time5] * 5;
                }
            }

            return hamming[n - 1];
        }
}

___________________________________________________
using System.Collections.Generic;
using System.Linq;

public class Hamming
{
        private static List<ulong> _cashed;

        public static long hamming(int n)
        {
            List<ulong> resultList;
            if (_cashed == null || n > 5000)
            {
                resultList = HammingInternal(5000).OrderBy(x => x).ToList();
                _cashed = resultList;
            }
            else
            {
                resultList = _cashed;
            }
            return (long)resultList[n - 1];
        }

        public static HashSet<ulong> HammingInternal(int n)
        {
            var counter = 0;
            var allNumbers = new HashSet<ulong>() { 1 };
            while (allNumbers.Count <= 5 * n)
            {
                var currentNumber = allNumbers.ToList()[counter];
                allNumbers.Add(currentNumber * 2);
                allNumbers.Add(currentNumber * 3);
                allNumbers.Add(currentNumber * 5);
                counter += 1;
            }
            return allNumbers;
        }
}

___________________________________________________
using System;
using System.Collections.Generic;
using System.Linq;

public class Hamming
{
  public static long hamming(
    int n)
  {
    var bases = new[] { 2, 3, 5 };
    var expos = new[] { 0, 0, 0 };
    var hamms = new List<long> { 1 };

    for (var i = 1; i < n; ++i)
    {
      var nextHamms = new long[3];

      for (var j = 0; j < 3; ++j)
      {
        nextHamms[j] = bases[j] * hamms[expos[j]];
      }

      var nextHamm = nextHamms
        .Min();

      hamms.Add(
        nextHamm);

      for (var j = 0; j < 3; ++j)
      {
        expos[j] += Convert.ToInt32(
          nextHamms[j] == nextHamm);
      }
    }
    
    return hamms[^1];
  }
}

___________________________________________________
using System;

public class Hamming
{
  public static long hamming(int n)
  {
    long[] Hamming = new long[n];
    Hamming[0] = 1;
       
    long x2 = 2, x3 = 3, x5 = 5;
    int i = 0, j = 0, k = 0;
    
    for (int index = 1; index < n; index++)
    {
      Hamming[index] = Math.Min(x2, Math.Min(x3, x5));
      
      if (Hamming[index] == x2) x2 = 2 * Hamming[++i];
      if (Hamming[index] == x3) x3 = 3 * Hamming[++j];
      if (Hamming[index] == x5) x5 = 5 * Hamming[++k];
    }    
    return Hamming[--n];
  }
}
