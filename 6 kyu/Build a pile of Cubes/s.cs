public class ASum {
  public static long findNb(long m) {
    long total = 1, i = 2;
    for(; total < m; i++) total += i * i * i;
    return total == m ? i - 1 : -1;
  }
}
_________________________________________
using System;

public class ASum {
  
  public static long findNb(long m) {
    long n = (long)Math.Floor(Math.Sqrt(2*Math.Sqrt(m)));
    return ((n * (n + 1)) / 2) * ((n * (n + 1)) / 2) == m ? n : -1;
  }
  
}
_________________________________________
using System;
public class ASum {
  
  public static long findNb(long m)
    {
      long result = -1;

      for (long i = 1; i <= long.MaxValue; i++)
      {
        var induction = Ind(i);
        if (induction == m) result = i;
        if (induction >= m) break;
      }

      return result;
    }

    private static long Ind(long val)
    {
      var r = (val * (val + 1)) / 2;
      return r * r;
    }
  
}
_________________________________________
using System;
public class ASum {
  
  public static long findNb(long m)
  {
    long result = 1;
    long sum = 0;

    while(m > sum)
    {
        sum += (long)Math.Pow(result, 3);
        result++;
    }

    return sum == m ? result - 1 : -1;
  } 
}
_________________________________________
using System;

public class ASum {
  
   public static long findNb(long m)
        {
            int count = 1;
            long sum = m;
            while (true)
            {
                long cubed =  (long)Math.Pow(count,3);
                sum -= cubed;

                if (sum == 0)
                    return count;

                if (sum < 0)
                    return -1;
                

                count++;
            }
        }
  
}
_________________________________________
using System;
public class ASum {
  
  public static long findNb(long m) {
    
    long n = 0;
            long total =0;
            for (long i = 0; i < m; i++)
            {
                total += Convert.ToInt64(Math.Pow(i, 3));
                if (total > m){return -1;}
                if (total == m) {return n; }
                n++;
            }

            
            return -1;      
  }
  
}
_________________________________________
using System;

public class ASum {
  
  public static long findNb(long m) {
    long ans = (long) Math.Sqrt(m);
    if(ans*ans != m)
      return -1;
    m = ans*2;
    ans = (long) Math.Sqrt(m);
    if(ans*ans+ans != m)
      return -1;
    return ans;
  }
}
_________________________________________
using System;

public class ASum {
  
  public static long findNb(long m) {
    
    var count = 0;
    long n = 0;
    
    for(var i = 0; i < Math.Sqrt(m); i++)
    {
      var x = (long)Math.Pow(i, 3);
      
      n += x;
      
      if(n > m)
        return -1;
      
      if(n==m)
        return count;     
      
       count++;
    }
    
    return -1;
  }
}
