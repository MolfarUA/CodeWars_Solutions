57eadb7ecd143f4c9c0000a3


using System;
using System.Linq;
public class Kata
{
       public static string AbbrevName(string name) => string.Join(".", name.Split(' ').Select(w => w[0])).ToUpper();
}
_________________________
public class Kata
{
  public static string AbbrevName(string name)
  {
   string[] words = name.Split(' ');

            return (words[0][0] + "." + words[1][0]).ToUpper();
  }
}
_________________________
class Kata
{
  public static string AbbrevName(string name)
  {
    return $"{name[0]}.{name[name.IndexOf(' ') + 1]}".ToUpper();
  }
}
_________________________
using System;
using System.Linq;

public class Kata
{
    public static string AbbrevName(string name)
    {
        string[] buf = name.Split(' ');

        var firstName = buf.First();
        var lastName = buf.Last();

        var oneUpper = Char.ToUpper(firstName.First());
        var twoUpper = Char.ToUpper(lastName.First());

        return $"{oneUpper}.{twoUpper}";
    }
}
