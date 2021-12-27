using System.Linq;

public static class Kata
{
  public static int Doubleton(int num)
  {
    while ((++num).ToString().Distinct().Count() != 2);
    return num;
  }
}

###################
using System;
using System.Linq;

public static class Kata
{
    public static int Doubleton(int num)
    {
            num += 1;
            char[] numToArray = num.ToString().Distinct().ToArray();

            while (numToArray.Length != 2)
            {
                num += 1;
                numToArray = num.ToString().Distinct().ToArray();
            }

            return num;
    }
}

##################
using System.Linq;

public static class Kata
{
    public static int Doubleton(int num)
    {
        while ($"{++num}".Distinct().Count() != 2); return num;
    }
}

###################
using System;
public static class Kata
{
    public static int Doubleton(int num)
    {
      if (num < 10) return 10;
     for (int i = num + 1;;i++) 
     {
      if (IsDoubleton(i))
      {
        return i;
      }
     }
    }
    public static bool IsDoubleton(int num)
    {
        string diżit = Convert.ToString(num);
        char dubA = diżit[0], dubB = '\0';
        for (int i = 1; i < diżit.Length; i++)
        {
          char ch = diżit[i];
          if (ch != dubA)
          {
            dubB = ch;
            break;
          }
          
        }
      if (dubB == '\0')
      {
        return false;
      }
        foreach (char ch in diżit)
        {
         if (ch != dubA && ch != dubB) 
           return false;
        }
      return true;
    }
}

#########################
using System.Linq;
public static class Kata
{
    public static int Doubleton(int n) 
    {
      while ((++n).ToString().Distinct().Count() != 2);
      return n;
    } 
}

###################
using System.Linq;
public static class Kata
{
    public static int Doubleton(int num)
    {
      int nextNum = num+1;
        while(!isDoubleton(nextNum)){
          ++nextNum;
        }
      return nextNum;
    }
  private static bool isDoubleton(int num){
    return num.ToString().Distinct().Count()==2;
  }
}

##################
using System;
using System.Linq;

public static class Kata
{
    public static int Doubleton(int num)
    {
        for(int i =num+1; i< 5000000; i++){
          int check =i.ToString().Distinct().ToArray().Length;
          if(check ==2){return i;}
        }
      return -1;
    }
}

###################
using System.Linq;

public static class Kata
{
    public static int Doubleton(int num)
    {
        for (int i = num + 1; i < 1000000; i++)
            {
                if ((i.ToString().GroupBy(c => c).Count()) == 2)
                    return i;
            }
            return 10000000;
    }
}

######################
using System.Linq;

public static class Kata
{
    public static int Doubleton(int num)
    {
        int current = num+1;

        while(IsDoubleton(current) == false)            
            current++;            

        return current;
    }


    public static bool IsDoubleton(int num) =>        
        $"{num}"
            .Distinct()
            .Count() == 2;
}
##########################
using System.Linq;
class Kata
{
  public static int Doubleton(int n)
  {
      while ((++n + "").Distinct().Count() != 2){ }
      return n;
  }
}

####################
using System.Linq;

public static class Kata {
    public static int Doubleton(int num) {
      int nextInt = num + 1;
      while (!IsDoubleton(nextInt))
        nextInt += 1;
      return nextInt;
    }
    
    private static bool IsDoubleton(int num) {
      return num.ToString().Distinct().Count() == 2;
    }
}
