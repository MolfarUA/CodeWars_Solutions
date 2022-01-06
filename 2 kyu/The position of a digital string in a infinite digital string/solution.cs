using System;

public class InfiniteDigitalString
{
    public static string BuildString(string numberString, int length)
    {
        string buffer = String.Empty;
        long n = Math.Max(long.Parse(numberString) - 1, 1);

        while (buffer.Length <= length + numberString.Length)
        {
            buffer += n.ToString();
            n++;
        }

        return buffer;
    }

    public static long FindNumberPosition(long n)
    {
        long location = 0;
        long log10 = (long)Math.Log10(n);

        for (long i = 0; i < log10; i++)
        {
            // Number of numbers in this range * number of digits in each number
            location += (long)(Math.Pow(10, i + 1) - Math.Pow(10, i)) * (i + 1);
        }

        location += (log10 + 1) * (n - (long)Math.Pow(10, log10));

        return location;
    }

    public static long CheckString(string startNumberString, string target)
    {
        long minLocation = long.MaxValue;

        var testString = BuildString(startNumberString, target.Length);
        var targetIndex = testString.IndexOf(target);

        if (-1 != targetIndex)
        {
            var startNumber = long.Parse(startNumberString) - 1;
            var location = FindNumberPosition(startNumber);
            location += targetIndex;

            minLocation = Math.Min(minLocation, location);
        }

        return minLocation;
    }

    public static long findPosition(string str)
    {
        if (long.Parse(str) == 0)
        {
            return FindNumberPosition((long)Math.Pow(10, str.Length)) + 1;
        }

        long minLocation = long.MaxValue;

        // Look for cases where the target number is fully expressed in the target string.
        // That is, the target string doesn't truncate the numbers.
        for (int spacing = 1; spacing <= str.Length; spacing++)
        {
            for (int offset = 0; offset < spacing; offset++)
            {
                if (offset + spacing > str.Length || str[offset] == '0')
                {
                    continue;
                }

                // Build and check a potential string based on the input fragment
                minLocation = Math.Min(minLocation, CheckString(str.Substring(offset, spacing), str));
            }
        }

        // Split the input string into 2 pieces at all possible points to see if it spans 2 numbers
        for (int splitIndex = 1; splitIndex < str.Length; splitIndex++)
        {
            var splitLow = str.Substring(0, splitIndex);
            var splitHigh = str.Substring(splitIndex);

            var low = (long.Parse(splitLow) + 1).ToString(new string('0', splitLow.Length));

            if (low.Length > splitLow.Length)
            {
                low = low.Substring(low.Length - splitLow.Length);
            }

            minLocation = Math.Min(minLocation, CheckString(splitHigh + low, str));

            // Look for digits that may be repeated and merge them together to check these shorter strings.
            // For example, "91 and 100" might be "91100" or "9100" (with the 1 repeated).
            for (int n = 1; n < low.Length; n++)
            {
                string sub = low.Substring(0, n);

                if (splitHigh.EndsWith(sub))
                {
                    minLocation = Math.Min(minLocation, CheckString(splitHigh + low.Substring(n), str));
                }
            }
        }

        return minLocation;
    }
}
___________________________________________________
using System;
using System.Collections.Generic;
using System.Linq;

 public class InfiniteDigitalString
    {
        public struct NumAndAddition
        {
            public long number;
            public int addition;
        }
        public static long findPosition(string str)
        {
            int strLen = str.Length;
            List<NumAndAddition> candidateList = new List<NumAndAddition>();
            
            for (int i = 1; i <= strLen; i++)
            {
                int Addition = 0;
                string padding = new string(' ', i - 1);
                string strX = padding + str + padding;
                
                for (int k = 1; k <= i; k++)
                {
                    List<long> numsList = new List<long>();
                    List<int> additionList = new List<int>();
                    bool status = true;
                    
                    for (int j = 0; j <= strX.Length - 2 * i; j += i)
                    {
                        string subStr1 = strX.Substring(j, i).Trim();
                        string subStr2 = strX.Substring(j + i, i).Trim();
                        long num = IsPotentialSequentialNumbers(subStr1, subStr2, i, out Addition);
                        
                        if (num == Convert.ToInt64(str))
                            return CalculateNumOfDigitBefore(num);
                            
                        numsList.Add(num);
                        additionList.Add(Addition);
                        
                        if (num == -1)
                        {
                            status = false;
                            break;
                        }
                    }
                    if (status == true && numsList.Count > 0)
                        candidateList.Add(new NumAndAddition() { number = numsList[0], addition = additionList[0] });

                    strX = strX.Substring(1);
                }
            }

            if (candidateList.Count > 0)
            {
                var min = candidateList.OrderBy(item => item.number).First();
                long strNum = Convert.ToInt64(str);
                if (min.number > strNum && strNum.ToString().Length == strLen)
                    return CalculateNumOfDigitBefore(strNum);
                else
                    return CalculateNumOfDigitBefore(min.number) + min.addition;
            }
            else
            {
                long num = Convert.ToInt64(str);
                if (num != 0)
                    return CalculateNumOfDigitBefore(num);
                else
                    return CalculateNumOfDigitBefore((long)Math.Pow(10, str.Length)) + 1;
            }

        }

        public static long IsPotentialSequentialNumbers(string str1, string str2, int numOfDigits, out int Addition)
        {
            int first = (int)Math.Pow(10, numOfDigits - 1);
            int str1Len = str1.Length;
            int str2Len = str2.Length;
            Addition = 0;
            string num1
                , num2;

            if (str2.Length == numOfDigits && str1.Last() == str2.Last())
                return -1;

            if (str1Len == numOfDigits)
            {
                if (Convert.ToInt64(str1) < Math.Pow(10, numOfDigits - 1))
                    return -1;
                num2 = (Convert.ToInt64(str1) + 1).ToString();
                if (num2.Substring(0, str2Len) == str2)
                {
                    return Convert.ToInt64(str1);
                }
            }
            else if (str2Len == numOfDigits)
            {
                if (Convert.ToInt64(str2) < Math.Pow(10, numOfDigits - 1))
                    return -1;

                num1 = (Convert.ToInt64(str2) - 1).ToString();
                if (num1.Substring(num1.Length - str1Len) == str1)
                {
                    Addition = num1.Length - str1Len;
                    return Convert.ToInt64(str2) - 1;
                }
            }

            else
            {
                int dif = numOfDigits - str1Len;
                string str1Completed;
                string str2Completed;

                if (Math.Floor(Math.Log10(Convert.ToInt64(str1) + 1)) + 1 > str1.Length)
                {
                    str1Completed = (Convert.ToInt64(str2.Substring(0, dif)) - 1).ToString() + str1;
                    str2Completed = str2.PadRight(numOfDigits, '0');
                }
                else
                {
                    str1Completed = str2.Substring(0, dif) + str1;
                    str2Completed = (Convert.ToInt64(str1Completed) + 1).ToString();
                }

                if (Convert.ToInt64(str1Completed) < Math.Pow(10, numOfDigits - 1)
                 ||
                    Convert.ToInt64(str1Completed) + 1 != Convert.ToInt64(str2Completed))
                    return -1;

                if (str2Completed.Substring(0, str2.Length) == str2)
                {

                    Addition = (str1Completed + str2Completed).IndexOf(str1 + str2); //dif;
                    return Convert.ToInt64(str1Completed);
                }
            }          
            return -1;
        }

        public static long CalculateNumOfDigitBefore(long number)
        {
            int numOfDigits = (int)Math.Floor(Math.Log10(number)) + 1;

            long sum = (number - (long)Math.Pow(10, numOfDigits - 1)) * numOfDigits;
            for (int i = 1; i <= numOfDigits - 1; i++)            
                sum += i * (9 * (long)Math.Pow(10, i - 1));           

            return sum;
        }
    }
___________________________________________________
using System; 
using System.Collections.Generic;
using System.IO;
using System.Linq;

public class InfiniteDigitalString
{
  private static long __numIndex(long n)
  {
    if(n<10) return n-1;
    long c = 0, p = 10;
    for(int i=1;;i++, p*=10) {
      c += i*9*(p/10);
      if(n<p*10) return c+(i+1)*(n-p);
    }
  }
  public static long findPosition(string str)
  {
      if(Convert.ToInt64(str) == 0) return __numIndex(Convert.ToInt64("1"+str))+1;
      for(int l=0; l<=str.Length; l++) {
        List<long> poss = new List<long>();
        for(int i=0; i<l; i++) {
          string sdt = str.Substring(0,l-i), end = str.Substring(l-i,i);
          List<string> cands = end == "" || end == "0" ? new List<string>{end+sdt}:new List<string>{end+sdt,(Convert.ToInt64(end)-1).ToString()+sdt};
          foreach(string c in cands) {
            if(c[0] == '0') continue;
            string ds = c;
            long n = Convert.ToInt64(c);
            while(ds.Length<str.Length+l) ds += (++n).ToString();
            int idx = ds.IndexOf(str);
            if(idx != -1) poss.Add(__numIndex(Convert.ToInt64(c))+idx); 
          }
        }
        if(poss.Count > 0) return poss.Min();
      }
      return -1;
  }
}
___________________________________________________
using System;
using System.Text;

public class InfiniteDigitalString
{
    // for given str find its position
    public static long findPositionForNumber(string str)
    {
        long searchForRecursively = 0;
        long searchedNumber = long.Parse(str);
        long powerOfTen = (long)Math.Pow(10, str.Length - 1);
        long subpowerOfTen = (long)Math.Pow(10, str.Length - 2);
        if (str.Length > 2)
            searchForRecursively = findPositionForNumber(subpowerOfTen.ToString());
        return (searchedNumber - powerOfTen) * (str.Length) + (powerOfTen - subpowerOfTen) * (str.Length - 1) + searchForRecursively;
    }
    // check if given two strings with missing digits are consecutive
    public static (bool, string, string) areMatching(StringBuilder prev, StringBuilder next)
    {
        if (prev.Equals("0")) return (false, "", "");
        int carry = 1; // because prev + 1 should equal to next so we start with 1
        bool isMatching = true;
        for (int i = next.Length - 1; i >= 0 && isMatching; i--)
        {
            if (next[i] == ' ')
            {
                next[i] = (prev[i] == '9' && carry == 1) ? '0' : (char)(prev[i] + carry);
                carry = (prev[i] == '9' && carry == 1) ? 1 : 0;
            }
            else if (prev[i] == ' ')
            {
                prev[i] = (next[i] == '0' && carry == 1) ? '9' : (char)(next[i] - carry);
                carry = (prev[i] == '9' && next[i] == '0') ? 1 : 0;
            }
            else if ((prev[i] - '0' + carry) % 10 == next[i] - '0' && (i != 0 || prev[i] != '0'))
            {
                carry = prev[i] - '0' + carry == 10 ? 1 : 0;
            }
            else
                isMatching = false;
        }
        return (isMatching, prev.ToString(), next.ToString());
    }
    // check if given two strings with missing digits are consecutive assuming more digits can be added up to expandCounter
    public static (bool, long, long) checkIfSequence(string predecessor, string successor, int expandCounter)
    {
        if (successor[0] == '0') return (false, 0, 0);
        if (predecessor == "9" && successor == "1") return (true, 10, -1);
        StringBuilder testNext = new StringBuilder(successor.PadRight(predecessor.Length));
        StringBuilder testPrev = new StringBuilder(predecessor.PadLeft(successor.Length));
        bool isMatched = true;
        string matchedPrev, matchedNext;
        do {
            (isMatched, matchedPrev, matchedNext) = areMatching(new StringBuilder(testPrev.ToString()), new StringBuilder(testNext.ToString()));
            testPrev.Insert(0, " ");
            testNext.Append(" ");
        } while (expandCounter-- > 0 && !isMatched);
        if (isMatched)
            return (isMatched, long.Parse(matchedNext), -predecessor.Length);
        else
            return (false, 0, 0);
    }
    public static long findPosition(string str)
    {
        if (long.Parse(str) == 0) // if only 0s then it's 10^n without "1"
            return findPositionForNumber(Math.Pow(10, str.Length).ToString()) + 1;
        (long num, long offset) matched = (0, 0);
        for (int range = 1; range <= str.Length; range++) // possible length of number (window used for checking parts of str)
        {
            (long num, long offset) candidate = (0, 0);
            for (int shift = 0; shift < range; shift++) // shift of window
            {
                StringBuilder strCut = new StringBuilder(str);
                string prevPart = "";
                bool isMatching = true;
                int i = 0;
                while (strCut.Length > 0 && isMatching)
                {
                    if (prevPart == "")
                    {
                        prevPart = strCut.ToString(0, shift + 1);
                        strCut.Remove(0, shift + 1);
                    }
                    if (strCut.Length == 0)
                        break;
                    string nextPart = strCut.ToString(0, Math.Min(range, strCut.Length));
                    strCut.Remove(0, Math.Min(range, strCut.Length));
                    long foundNumber, foundOffset;
                    (isMatching, foundNumber, foundOffset) = checkIfSequence(prevPart, nextPart, range);
                    //Console.WriteLine($"R={range} S={shift} prev={prevPart} next={nextPart} -> isMatching={isMatching} num={foundNumber} off={foundOffset}");
                    if (isMatching)
                    {
                        if (candidate.num == 0 || foundNumber < candidate.num)
                            candidate = (foundNumber, foundOffset);
                        if (candidate.num + i != foundNumber) // pairs must be in sequence, increasing by one
                            isMatching = false;
                        if (prevPart + nextPart == str)
                        {
                            if (matched.num == 0 || foundNumber < matched.num || (foundNumber == matched.num && foundOffset < matched.offset))
                                matched = (foundNumber, foundOffset);
                            break;
                        }
                    }
                    prevPart = nextPart;
                    i++;
                }
                if (isMatching && (matched.num == 0 || candidate.num < matched.num))
                    matched = (candidate.num, candidate.offset);
                //Console.WriteLine($"- FOR GIVEN RANGE / SHIFT num={matched.num} (candidate={candidate.num})");
            }
        }
        //Console.WriteLine($"FOUND num={matched.num} offset={matched.offset}");
        if (matched.num == 0 || (str[0] != '0' && matched.num > long.Parse(str)))
            return findPositionForNumber(str);
        else
            return findPositionForNumber(matched.num.ToString()) + matched.offset;
    }
}
