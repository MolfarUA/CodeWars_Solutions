public class StockList {

    public static String stockSummary(String[] lstOfArt, String[] lstOfCat) {
        if (lstOfArt == [] || lstOfCat == []) return ""
        lstOfCat.collect { cat -> 
          def count = lstOfArt.collect { it ->
            (it[0] == cat) ? it.split().last().toInteger() : 0
          }.sum()
          "($cat : $count)"
        }.join(' - ')
    }
}
________________________________________
public class StockList {

    public static String stockSummary(String[] listOfArticles, String[] listOfCategories) {

        List<String> allArticlesPerEveryCategory = []
        
        if (listOfArticles.size() == 0 || listOfCategories.size() == 0) {
            return ""
        }
        else {
            listOfCategories.collect {
                String category = it
                def articlesPerCategory = listOfArticles.findAll { it.charAt(0).toString() == category }
                int totalCountOfArticlesPerCategory = 0
                for (article in articlesPerCategory) {
                    totalCountOfArticlesPerCategory += article.substring(article.indexOf(" ")).toInteger()
                }
                allArticlesPerEveryCategory.add("(" + category + " : " + totalCountOfArticlesPerCategory + ")")
            }
            return allArticlesPerEveryCategory.join(" - ").toString()
        }
    }
}
________________________________________
public class StockList {

    public static String stockSummary(String[] lstOfArt, String[] lstOfCat) {
      if (lstOfArt.size()==0 || lstOfCat.size()==0) return ""
      def result = ""
      lstOfCat.each { category ->
          def accumulator = 0
          lstOfArt.findAll {(it[0] == category) }.each { element ->
              accumulator = accumulator + element.split(" ")[1].toInteger()
          }
          result = result + ((result.size()>0)?" - ":"") + "(${category} : ${accumulator})"
      }
      return result
    }
}
________________________________________
public class StockList {

    public static String stockSummary(String[] b, String[] c) {
      if(!b) 
        ""
      else
        (b.collect{[it.split(" ")[0][0],it.split(" ")[1]]}+c.collect{[it,0]})
                .groupBy { it[ 0 ] }
                .collectEntries { key, value ->
                    [key, value*.getAt(1)*.asType(Integer).sum()]
                }
                .subMap(c)
                .collect {"(${it.key} : ${it.value})"}
                .join(" - ")
    }
}
________________________________________
public class StockList {

    public static String stockSummary(String[] lstOfArt, String[] lstOfCat) {
      
     def counter = 0;
        def result = lstOfCat.collect { it2 ->
            def sum = lstOfArt.findAll({ it.startsWith(it2) })
                    .collect({ Long.parseLong(it.split(" ")[1]) })
                    .sum();
            if (sum == null) {
                counter++;
            }
            return "(${it2} : ${sum == null ? 0 : sum})"
        }.join(" - ");
        return counter == lstOfCat.size() ? "" : result;
    }
}
