using System;
using System.Collections.Generic;

public static class Kata
{
  public static string AddBinary(int a, int b)
  {
    List<int> sumBin = new List<int>();
    int sumDec = a + b;
    int quotient = sumDec;
    int binUnit;
    string result = "";
    
    while (quotient > 0){
      binUnit = quotient % 2;
      sumBin.Add(binUnit);
      quotient /= 2;
    }
    
    sumBin.Reverse();
    
    result = string.Join("", sumBin.ToArray());
    return result;
  }
}
__________________________________
using System;

public static class Kata
{
  public static string AddBinary(int a, int b)
  {
    int sum = a + b;
    string res = Convert.ToString(sum, 2);
    return res;
  }
}
__________________________________
using System;

public static class Kata
{
  public static string AddBinary(int a, int b)
  {
    string result="";
    int sum = a+b;
    while(sum>0)
      {
        if(sum%2==0)
          {
            result=result.Insert(0,"0");
          }
        else 
          {
             result=result.Insert(0,"1");
          }
      sum=sum/2;
      }
    return result;
  }
}
__________________________________
using System;

public static class Kata
{
  public static string AddBinary(int a, int b)
        {
            int summ = a + b;
            int result = 0;
            string answer = "";
            while (summ != 0)
            {
                result = summ % 2;
                answer += result;
                summ /= 2;
            }
            char[] arr = answer.ToCharArray();
            Array.Reverse(arr);
            return new string(arr);           
        }
}
__________________________________
using System;
using System.Linq;

public static class Kata
{
  public static string AddBinary(int a, int b)
  {
   // your code ...
    int sum = a + b;
    string binary = "";
    while (sum != 0)
    {
      binary += sum % 2;
      sum = sum / 2;
    }
    return (new string(binary.ToCharArray().Reverse().ToArray()));
  }
}
