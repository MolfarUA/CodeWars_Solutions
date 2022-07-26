595970246c9b8fa0a8000086


using System;

public class Kata
{
  public static String CapitalizeWord(String word)
  {
    return char.ToUpper(word[0]) + word.Substring(1);
  }
}
______________________
public class Kata
{
  public static string CapitalizeWord(string word)
  {
    return char.ToUpper(word[0]) + word[1..];
  }
}
______________________
class Kata
{
  public static string CapitalizeWord(string s)
  {
    return char.ToUpper(s[0]) + s.Substring(1);
  }
}
______________________
public class Kata
{
  public static string CapitalizeWord(string word)
  {
    return char.ToUpper(word[0]) + word[1..].ToLower();
  }
}
