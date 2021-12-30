public class Number
{
  public int DigitalRoot(long n)
  {
     return (int)(1 + (n - 1) % 9);
  }
}

________________________________
public class Number
{
    public int DigitalRoot(long n)
    {
        if (n < 10) return (int)n;
        long r = 0;
        while (n > 0)
        {
            r += n % 10;
            n /= 10;
        }
        return DigitalRoot(r);
    }
}

________________________________
using System;
using System.Linq;

public class Number
{
  public int DigitalRoot(long n)
  {
    if(n.ToString().Length >1)
      return DigitalRoot(n.ToString().Select(digit=> int.Parse(digit.ToString())).Sum());
    
    return (int)n;
  }
}

________________________________
using System;
using System.Linq;

public class Number
{
  public int DigitalRoot(long n) 
  {
    long count = n.ToString().ToCharArray().Select(x => int.Parse(x.ToString())).Sum();
    
    return count > 9 ? DigitalRoot(count) : Convert.ToInt32(count);
  }
}

________________________________
using System;

public class Number
{
  public int DigitalRoot(long n)
  {
    string num = n.ToString();
    while (num.Length > 1)
    {
      
      int total = 0;
      
      foreach(var c in num)
      {
        total += c - '0';
      }
      
      num = total.ToString();
      
    }
    return Convert.ToInt32(num);
  }
}

________________________________
public class Number
{
  public int DigitalRoot(long n)
        {
            string input = n.ToString();
            var nums = input.ToCharArray();
            int sum = 10;
            while (sum > 9)
            {
                nums = GetSumOfNums(nums, out sum);
            }
            return sum; 
        }
        private char[] GetSumOfNums(char[] nums, out int sum)
        {
            sum = 0;
            foreach (char num in nums)
            {
                sum += int.Parse(num.ToString());
            }
            return sum.ToString().ToCharArray();
        }
}
