public static class Kata
{
  public static char TrilingualDemocracy(string speakers) =>
    (char)(speakers[0] ^ speakers[1] ^ speakers[2]);
}
____________
public static class Kata
{
  public static char TrilingualDemocracy(string speakers)
  {
    return (char)(speakers[0] ^ speakers[1] ^ speakers[2]);
  }
}
_____________
using System.Collections.Generic;
using System.Linq;
public static class Kata
{
  public static char TrilingualDemocracy(string speakers)
  {
    char[] lang = new char[4]{'D','F','I','K'} ;
Dictionary<char,int> keyValuePairs = new Dictionary<char,int>();
foreach(char speaker in speakers)
{
    if(keyValuePairs.ContainsKey(speaker))
    {
        keyValuePairs[speaker] += 1;
    }
    else keyValuePairs.Add(speaker, 1);
}
if (keyValuePairs.Count == 1) return keyValuePairs.Keys.First(); 
if (keyValuePairs.Count == 2) return keyValuePairs.OrderBy(x =>x.Value).First().Key;
return lang.First(x => !keyValuePairs.ContainsKey(x));
  }
}
