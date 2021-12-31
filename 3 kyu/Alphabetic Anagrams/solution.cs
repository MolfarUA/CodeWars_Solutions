using System;
using System.Linq;
using System.Collections.Generic;

public class Kata
{
    public static long ListPosition(string value)
    {
        var chars = new List<char>(value.OrderBy(c => c));
        
        return value.Aggregate(1L, (pos,cur) =>
        {
            var before = chars.TakeWhile(c => c != cur).Count();
            var adjust = chars.GroupBy(c => c).Aggregate(1L, (p,g) => p * Fac(g.Count()));
            chars.Remove(cur);
            return pos + before * Math.Max(1L, Fac(chars.Count)) / adjust;
        });
    }

    private static long Fac(long i) => i < 2 ? i : i * Fac(i - 1);
}

___________________________________________________
using System.Collections.Generic;
using System.Linq;

struct Range
{
    public long LowBound;
    public long HighBound;
}

public static class Kata
{
    static long GetNumberOfPermutationsWithRepetition(this string value, SortedDictionary<char, int> countByLetter)
    {
        long result = Factorial(value.Length);
        foreach (int Ni in countByLetter.Values)
            result /= Factorial(Ni);
        return result;
    }
    static long Factorial(int x)
    {
        long factorial = 1;
        for (int i = 1; i <= x; i++)
            factorial *= i;
        return factorial;
    }
    static long GetListPosition(this string value, Range range, SortedDictionary<char, int> countByLetter)
    {
        if (range.LowBound == range.HighBound)
            return range.LowBound;
        long numberOfPermutationsWithRepetition = value.GetNumberOfPermutationsWithRepetition(countByLetter);
        long step = numberOfPermutationsWithRepetition / value.Length;
        long lowBoundIncrement = 0;
        foreach (char letter in countByLetter.Keys)
        {
            if (letter == value[0])
                break;
            lowBoundIncrement += step * countByLetter[letter];
        }
        long highBoundDecrement = numberOfPermutationsWithRepetition - (lowBoundIncrement + step * countByLetter[value[0]]);
        Range newRange;
        newRange.LowBound = range.LowBound + lowBoundIncrement;
        newRange.HighBound = range.HighBound - highBoundDecrement;
        countByLetter[value[0]]--;
        return value.Substring(1).GetListPosition(newRange, countByLetter);
    }
    public static long ListPosition(string value)
    {
        SortedDictionary<char, int> countByLetter = new SortedDictionary<char, int>();
        foreach (char letter in value.Distinct())
            countByLetter.Add(letter, value.Count(c => c == letter));
        Range range;
        range.LowBound = 1;
        range.HighBound = value.GetNumberOfPermutationsWithRepetition(countByLetter);
        return value.GetListPosition(range, countByLetter);
    }
}

___________________________________________________
using System;
using System.Linq;
using System.Collections.Generic;

public class Kata
{
    public static long ListPosition(string value)
    {
        var orderedLetters = value
            .OrderBy(c => c)
            .GroupBy(
                    c => c,
                    c => c,
                    (c, letters) =>
                        new Letter
                        {
                            Key = c,
                            Count = letters.Count()
                        }
                )
            .ToList();

        long result = 0;

        for (int i = 0; i < value.Length; i++)
        {
            var currentLetterOrderIndex = orderedLetters.FindIndex(letter => letter.Key == value[i]);

            // check if the first letter in the word is not the first one in alphabetical order
            if (currentLetterOrderIndex > 0)
            {
                // iterate through ordered letters until the current word letter is reached
                for (int j = 0; j < currentLetterOrderIndex; j++)
                {
                    // deep copy a list of ordered letters
                    var tempLetters = new List<Letter>();
                    orderedLetters.ForEach(l =>
                        tempLetters.Add(new Letter { Key = l.Key, Count = l.Count })
                    );

                    // for the current letter, remove it or decrease the count
                    if (tempLetters[j].Count > 1)
                        tempLetters[j].Count -= 1;
                    else
                        tempLetters.RemoveAt(j);

                    // get repeated occurences in word letters to calculate number of permutations
                    var elementsRepetitions = tempLetters
                        .Select(letter => letter.Count)
                        .ToArray();

                    // get number of elements to calculate number of permutations
                    var elementsCount = tempLetters
                        .Select(letter => letter.Count)
                        .Sum();

                    result += GetPermutationsNumber(elementsCount, elementsRepetitions);
                }

            }

            // for the current letter, remove it or decrease the count
            if (orderedLetters[currentLetterOrderIndex].Count > 1)
                orderedLetters[currentLetterOrderIndex].Count -= 1;
            else
                orderedLetters.RemoveAt(currentLetterOrderIndex);

        }
        result += 1;
        return result;
    }

    private static long GetPermutationsNumber(int elementsCount, params int[] elementsRepetitions)
    {
        long dividend = Factorial(elementsCount);
        long divisor = 1;
        foreach (var repetitionNb in elementsRepetitions)
        {
            if (repetitionNb > 0)
                divisor *= Factorial(repetitionNb);
        }
        return dividend / divisor;
    }

    private static long Factorial(int inputValue)
    {
        long result = 1;
        for (int i = 0; i < inputValue; i++)
        {
            result *= (i + 1);
        }
        return result;
    }

    class Letter
    {
        internal char Key { get; set; }
        internal int Count { get; set; }
    }
}

___________________________________________________
using System;
using System.Collections.Generic;
using System.Linq;

public class Kata
{
    public static long ListPosition(string value)
    {
      char[] letters = value.ToCharArray();
      char[] sorted = (char[])letters.Clone(); Array.Sort(sorted);
      List<char> unused = sorted.ToList();
      
      decimal totalcombos = 1; 
      for(int i = 2;i<=value.Length;i++)              {totalcombos *= i;}         //// The number of combinations is n! (n factorial) 
      decimal estimate = 1;                                                       //// Our estimate iterates upwards from the first possibility.            
        
      var freq = letters.GroupBy(c=>c);
      foreach (var g in freq.Where(g=>g.Count() > 1)){
        for(int i = 2;i<=g.Count();i++){               totalcombos /= i;          //// For repeated letters, possibilities are divided 
        }                                                                         //// by (# of repeats for that letter)!
      }     
    
      foreach(char l in letters)
      {                                                                             ///////////// ALGORITHM 
        decimal binwidth = totalcombos / unused.Count();                           //// split the number of possibilities into 'bins', based on the available letters.            
        int bin          = unused.FindIndex(x=> x==l);                             //// e.g. for ABC, if the first letter is A, it will be in the first third of the possibilities                                                      
        totalcombos      = binwidth * unused.Where(x => x==l).Count();             //// find the new number of combinations possible for the following letter - bin width * frequency of that letter. 
        
        estimate         += bin * binwidth;                                        //// update the estimate accordingly, it iterates upward to the correct possibility. 
        unused.Remove(l);                                                          //// and remove that letter from our list of 'available' letters. 
      }
      
      
      return (long)estimate;
    }
}

___________________________________________________
using System;
using System.Linq;

public class Kata
{
    public static long ListPosition(string value)
    {
        long amount = 0;
        while (!string.IsNullOrWhiteSpace(value))
        {
            long division = 1;
            foreach (char c in value.Distinct())
                division *= Factorial(value.Count(x => x == c));
          
            amount += (Factorial(value.Count() - 1) / (division)) * value.Count(x => x < value.First());
            value = value.Substring(1);
        }

        return amount + 1;
    }
  
    public static long Factorial(int n)
    {
        long total = 1;
        for (int i = 1; i <= n; i++)
            total *= i;

        return total;
    }
}

___________________________________________________
using System;
using System.Linq;

public class Kata
{
  static long[] fact;
  
  static long NumberOfPermutationsWithRepetitions(int[] a)
  {
    long fact_sum = fact[a.Sum()];
    long fact_mult = 1;
    for (int i = 0; i < a.Length; i++)
      fact_mult *= fact[a[i]];
    return fact_sum / fact_mult;
  }
  
  static void GenFact(int size)
  {
    fact = new long[size + 1];
    fact[0] = 1;
    for (int i = 1; i <= size; i++) fact[i] = i * fact[i - 1];
  }
  
  public static long ListPosition(string str)
  {
    int[] nums_str = new int[26];
    for (int i = 0; i < str.Length; i++) nums_str[str[i] - 'A']++;

    GenFact(nums_str.Sum());
    
    long ans = 0;
    for (int i = 0; i < str.Length; i++)
    {
      for (int j = 0; j < str[i] - 'A'; j++)
      {
        if (nums_str[j] != 0)
        {
          nums_str[j]--;
          ans += NumberOfPermutationsWithRepetitions(nums_str);
          nums_str[j]++;
        }
      }
      nums_str[str[i] - 'A']--;
    }
    return ans + 1;
  }
}

___________________________________________________
using System;
using System.Collections.Generic;
using System.Text;
public class Kata
{
    public static long ListPosition(string value)
    {
        //Our algorithm:
        /*
          For each letter, find how many letters could be placed before it. Call this N
          We then have N * (unique combinations of remaining letters) permutations that would be before it.
          We then add all these together
        
        */
      
        return 1+Calculate(value,0);
    }
    public static long Calculate(string s, int p)
    {
      if( p >= s.Length)
      {
        return 0;
      }
      string curString = s.Substring(p);
      List<char> usedLetters = new List<char>();
      long permutations = 0;
      for(int i = 1; i < curString.Length;i++)
      {
        char cLetter = curString[i];
        //If the letter is less than whwat were at rn, swap em and calculate unique permutations
        if(cLetter < curString[0] && !usedLetters.Contains(cLetter))
        {
          //Swap the letters, count the number of unique permutations
          StringBuilder sb = new StringBuilder(curString);
          
          sb[i] = curString[0];
          sb.Remove(0,1);
          permutations += uniquePermutations(sb.ToString());
          usedLetters.Add(cLetter);
        }
      }
      return permutations+Calculate(s,p+1);
    }
    public static long uniquePermutations(string s)
    {
       Dictionary<char,int> dict = new Dictionary<char,int>();
      for(int i = 0; i < s.Length;i++)
      {
        if(!dict.ContainsKey(s[i]))
        {
          dict[s[i]] = 1;
        }
        else
        {
          dict[s[i]]+=1;
        }
      }
      List<int> repeats = new List<int>();
      foreach(var kvp in dict)
      {
        if(kvp.Value != 1)
        {
          repeats.Add(kvp.Value);
        }
      }
      long permutations = 1;
      if(repeats.Count == 0)
      {
        for(int i = s.Length; i>=2;i--)
        {
          permutations *= (long)i;
        }
        return permutations;
      }
      
      
      //So we work when we dont have repeats....
      
      repeats.Sort();
      for(int i = s.Length; i>repeats[repeats.Count-1];i--)
      {
        permutations *= (long)i;
      }
      repeats.RemoveAt(repeats.Count-1);
      foreach(int l in repeats)
      {
        int lp = 1;
        for(int i = 2; i <=l;i++)
        {
          lp*=i;
        }
        permutations/=lp;
      }
      return permutations;
    }
}
