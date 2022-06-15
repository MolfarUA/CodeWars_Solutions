using System.Linq;

public class Kata
{
  public static string FakeBin(string x)
  {
    return string.Concat(x.Select(a => a < '5' ? "0" : "1"));
  }
}
__________________________________
using System.Text;
public class Kata
{
  public static string FakeBin(string x)
  {
    StringBuilder builder = new StringBuilder();
    
    foreach (char t in x)
    {
      builder.Append( t >= '5' ? '1' : '0' );
    }
        
    return builder.ToString();
  }
}
__________________________________
using System.Text.RegularExpressions;
public class Kata
{
  public static string FakeBin(string x)
  {
    x = Regex.Replace(x, "[4321]", "0");
    x = Regex.Replace(x, "[56789]", "1");
    return x;
  }
}
__________________________________
using System.Linq;

public class Kata
{
  public static string FakeBin(string x)
  {
    return string.Concat(x.Select(c => c / '5'));
  }
}
__________________________________
using System.Text.RegularExpressions;
public class Kata
{
  public static string FakeBin(string x)
  {
    return Regex.Replace(Regex.Replace(x, "[1-4]", "0"), "[5-9]", "1");
  }
}
__________________________________
using System.Text;
public class Kata
{
  public static string FakeBin(string x)
  {
    var builder = new StringBuilder(x);
    for (int i = 0; i < builder.Length; ++i)
    {
      builder[i] = builder[i] < '5' ? '0' : '1';
    }
    return builder.ToString();
  }
}
