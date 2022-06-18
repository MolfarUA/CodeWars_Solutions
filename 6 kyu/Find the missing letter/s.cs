public class Kata
{
    public static char FindMissingLetter(char[] array)
    {
        for(int i = 0; i < array.Length - 1; i++)
        {
            if(array[i + 1] - array[i] > 1)
            {
                return (char)(array[i] + 1);
            }
        }
    
        return ' ';
    }
}
________________________
using System.Linq;

public class Kata
{
  public static char FindMissingLetter(char[] array) => (char)Enumerable.Range(array[0], 25).First(x => !array.Contains((char)x));
}
________________________
using System.Linq;

public class Kata
{
  public static char FindMissingLetter(char[] array) => (char) (array.Where((c, i) => array[i + 1] - c != 1).First() + 1);
}
________________________
using System.Linq;

public class Kata
{
  public static char FindMissingLetter(char[] array)
  {
    return Enumerable.Range(array[0], array.Length + 1).Select(a => (char)a).Except(array).Single();
  }
}
________________________
using System.Linq;

public class Kata
{
  public static char FindMissingLetter(char[] arr)
  {
    char m = arr.First(), n = arr.Last();
    return (char)(n*(n+1)/2 - (m-1)*m/2 - arr.Sum(c => c));
  }
}
