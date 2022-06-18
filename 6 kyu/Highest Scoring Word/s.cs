57eb8fcdf670e99d9b000272


using System.Linq;
using System;

public class Kata
{
  public static string High(string s)
  {
    return s.Split(' ').OrderBy(a => a.Select(b => b - 96).Sum()).Last();
  }
}
_____________________________________________
public class Kata
{
  public static string High(string s)
  {
      string[] words = s.Split(' ');
      string highestWord = "";
      int highestNumber = 0;
      
      foreach (string word in words)
      {
           int number = WordsToMarks(word);
           if (highestNumber < number)
           {
               highestWord = word;
               highestNumber = number;
           }
      }
      return highestWord;
  }
  
  public static int WordsToMarks(string str)
  {
      int n = 0;
      string abc = "abcdefghijklmnopqrstuvwxyz";
      foreach (char x in str)
      {
          n += abc.IndexOf(x) + 1;
      }
      return n;
  }
  
}
_____________________________________________
using System.Linq;
using System.Collections.Generic;

public class Kata
{
  const int ALPHABET_COUNT = 26;
  const int LETTER_A = 97;
  
  private static readonly IDictionary<char, int> LetterScores =
    Enumerable
      .Range(0, ALPHABET_COUNT)
      .ToDictionary(x => (char)(LETTER_A+x), x => x + 1);
  
  public static string High(string s)
  {   
    var words = s.Split(" ");
    return words
            .Select(w => (w, score: Score(w)))
            .GroupBy(x => x.score)
            .OrderBy(x => x.Key)
            .Last()
            .First().w;
  }
  
  public static int Score(string word){
    return word.Select(c => LetterScores[c]).Sum();
  }
}
_____________________________________________
using System.Linq;

public class Kata
{
  public static string High(string s)
  {
      var abc = "abcdefghijklmnopqrstuvwxyz";
      var highest = "";
      foreach(var word in s.Split(" ")) {
          if (word.ToCharArray().Select(c => abc.IndexOf(c)+1).Sum() 
              > highest.ToCharArray().Select(c => abc.IndexOf(c)+1).Sum()) {
              highest = word;
          }
      }
      return highest;
  }
}
_____________________________________________
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

public class Kata
{
  public static string High(string s)
        {
            List<string> listOfStrings = s.Split(" ").ToList();
            List<int> listOfScores = new();
            for (int i = 0; i < listOfStrings.Count; i++)
            {
                int sum = 0;
                string str = listOfStrings[i];
                for (int j = 0; j < str.Length; j++)
                {
                    {
                        sum += Convert.ToInt32(str[j])-96;
                    }
                }
                listOfScores.Add(sum);
            }
            return listOfStrings[listOfScores.IndexOf(listOfScores.Max())];
        }
}
