using System;
using System.Collections.Generic;
using System.Linq;

public class StockList {

    public static string stockSummary(string[] lstOfArt, string[] lstOf1stLetter)
    {
        if (lstOfArt.Length == 0 || lstOf1stLetter.Length == 0)
            return string.Empty;
      
        Dictionary<string, int> Cat = new Dictionary<string, int>();
        foreach (string s in lstOf1stLetter)
        {
            Cat.Add(s, 0);
        }

        foreach(string s in lstOfArt)
        {
            string FirstChar = s.First().ToString();
            if (Cat.ContainsKey(FirstChar))
            {
                Cat[FirstChar] += int.Parse(s.Split(' ')[1]);
            }
        }

        List<string> output = new List<string>();

        foreach(KeyValuePair<string, int> kvp in Cat)
        {
            output.Add($"({kvp.Key} : {kvp.Value})");
        }

        return string.Join(" - ", output);
    }
}
________________________________________
public class StockList {

    public static string stockSummary(string[] lstOfArt, string[] lstOf1stLetter)
    {
      string result = "";
      
      if(lstOfArt.Length == 0 || lstOf1stLetter.Length == 0)
      {
        return result;
      }
      else
      {
        for(int i = 0; i < lstOf1stLetter.Length; i++)
        {
          int letcount = 0;
          for(int j = 0; j < lstOfArt.Length; j++)
          {
            if(lstOfArt[j][0].ToString() == lstOf1stLetter[i])
            {
              letcount += int.Parse(lstOfArt[j].Split(' ')[1]);
            }
          }
          result += @"(" +  lstOf1stLetter[i] + " : " + letcount.ToString() + @") - "; 

          letcount = 0;
        }
        result = result.Remove(result.Length - 3); 
        return result;
      }
    }
}
________________________________________
using System;
using System.Collections.Generic;
using System.Linq;    

  public class Artitcle
    {
        public string Category { get; set; }
        public string Code { get; set; }
        public int NrAvailable { get; set; }
    }
    public class Inventory
    {
        public string Key { get; set; }
        public string Category { get; set; }
        public int Total { get; set; }
    }

    public class StockList
    {
        public static string stockSummary(String[] articles, String[] letters)
        {
            if (letters == null || articles == null || !articles.Any() || !letters.Any())
            {
                return "";
            }

            var inventoryList = FormatArticles(articles);

            var artitclesGrouped = GroupArticles(inventoryList);

            var result = new List<string>();
            GetListOfInvetory(letters, artitclesGrouped).ForEach(q => result.Add($"({q.Key} : {q.Total})"));
            return string.Join(" - ", result);

        }

        private static List<Inventory> GetListOfInvetory(String[] letters, IEnumerable<Inventory> articlesGrouped)
        {
            var query = (from Initial in letters
                         join invetory in articlesGrouped on Initial equals invetory.Category
                         into Invetory
                         from categ in Invetory.DefaultIfEmpty()
                         select new Inventory { Key = Initial, Total = categ != null ? categ.Total : 0 }).ToList();
            return query;
        }

        private static IEnumerable<Inventory> GroupArticles(List<Artitcle> inventoryList)
        {
            var artitclesGrouped = inventoryList.GroupBy(x => x.Category).Select(
            g => new Inventory
            {
                Key = g.Key,
                Total = g.Sum(s => s.NrAvailable),
                Category = g.First().Category
            });
            return artitclesGrouped;
        }

        private static List<Artitcle> FormatArticles(string[] articles)
        {
            var invertory = new List<Artitcle>();
            articles.ToList().ForEach(a => invertory.Add(new Artitcle
            {
                Category = a.Substring(0, 1),
                Code = a.Substring(0, a.IndexOf(" ")),
                NrAvailable = Convert.ToInt32(a.Substring(a.IndexOf(" ") + 1))
            }));
            return invertory;
        }
    }
________________________________________
using System;
using System.Collections.Generic;
using System.Linq;

public class Inventory
{
        public string Category { get; set; }
        public string Code { get; set; }
        public int NrAvailable { get; set; }
}

public class StockList {

        public static string stockSummary(String[] articles, String[] letters)
        {
            if (letters == null || articles == null || !articles.Any() || !letters.Any())
            {
                return "";
            }

            var newInventory = new List<Inventory>();
            articles.ToList().ForEach(a => newInventory.Add(new Inventory
            {
                Category = a.Substring(0, 1),
                Code = a.Substring(0, a.IndexOf(" ")),
                NrAvailable = Convert.ToInt32(a.Substring(a.IndexOf(" ") + 1))
            }));

            var artitclesGrouped = newInventory.GroupBy(x => x.Category).Select(
                g => new
                {
                    Key = g.Key,
                    TotalAvailable = g.Sum(s => s.NrAvailable),
                    Category = g.First().Category
                });

            var query = (from Initial in letters
                        join invetory in artitclesGrouped on Initial equals invetory.Category
                        into Invetory
                        from categ in Invetory.DefaultIfEmpty()
                        select new { Initial, categ }).ToList();
            var result = new List<string>();

            query.ForEach(q=> result.Add($"({q.Initial} : {(q.categ != null ? q.categ?.TotalAvailable : 0)})"));
            return string.Join(" - ", result);

        }
}
________________________________________
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using NUnit.Framework;

    class Inventory
    {
        public string Category { get; set; }
        public string Code { get; set; }
        public int NrAvailable { get; set; }
    }
    public class StockList
    {
        public static string stockSummary(String[] lstOfArt, String[] lstOf1stLetter)
        {
          if (lstOf1stLetter == null || lstOfArt == null || lstOfArt.Length == 0 || lstOf1stLetter.Length == 0)
            {
                return "";
            }

            var newInventory = new List<Inventory>();
            foreach (var item in lstOfArt)
            {
                newInventory.Add(new Inventory
                {
                    Category = item.Substring(0, 1),
                    Code = item.Substring(0, item.IndexOf(" ")),
                    NrAvailable = Convert.ToInt32(item.Substring(item.IndexOf(" ") + 1))
                });
            }

            var grp = newInventory.GroupBy(x => x.Category).Select(
                g => new
                {
                    Key = g.Key,
                    TotalAvailable = g.Sum(s => s.NrAvailable),
                    //Code = g.First().Code,
                    Category = g.First().Category
                });

            var query = from Initial in lstOf1stLetter
                        join invetory in grp on Initial equals invetory.Category
                        into gj
                        from categ in gj.DefaultIfEmpty()
                        select new { Initial, categ };
            var result = new List<string>();
            foreach (var q in query)
            {
                result.Add($"({q.Initial} : {(q.categ != null ? q.categ?.TotalAvailable : 0)})");
            }
            return string.Join(" - ", result);
        }
    }
________________________________________
using System;

public class StockList 
{
  public static string stockSummary(String[] lstOfArt, String[] lstOf1stLetter)
  {
    if (lstOfArt.Length == 0 || lstOfArt == null)
      return "";
    if (lstOf1stLetter.Length == 0 || lstOf1stLetter == null)
      return "";
    
    var result = "";
    for (var j = 0; j < lstOf1stLetter.Length; j++)
    {
      var sum = 0;
      for (var i = 0; i < lstOfArt.Length; i++)
      {
        string[] str = lstOfArt[i].Split(' ');
        if (str[0].StartsWith(lstOf1stLetter[j]))
        {
          sum += Int32.Parse(str[1]);
        }
      }
      result += $"({lstOf1stLetter[j]} : {sum})";
      if (j != lstOf1stLetter.Length - 1)
      {
        result += " - ";
      }
      sum = 0;
    }
    return result;
  }
}
