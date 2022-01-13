import java.util.Arrays;
import java.util.IntSummaryStatistics;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class StockList {

    private static class Book {
        public final String category;
        public final String code;
        public final int quantity;

        public Book(String label) {
            category = label.substring(0,1);
            code = label.split(" ")[0].substring(1);
            quantity = Integer.parseInt(label.split(" ")[1]);
        }
    }

    public static String stockSummary(String[] lstOfArt, String[] lstOf1stLetter) {
        if (lstOfArt.length == 0 || lstOf1stLetter.length == 0)
          return "";
        Map<String, Integer> categoryCounts = Arrays.stream(lstOfArt)
                .map(Book::new)
                .collect(Collectors.groupingBy(book -> book.category,
                         Collectors.summingInt(book -> book.quantity)));
        return Arrays.stream(lstOf1stLetter)
                .map(initial -> String.format("(%s : %d)", 
                                              initial, categoryCounts.getOrDefault(initial, 0)))
                .collect(Collectors.joining(" - "));
    }
}
________________________________________
import java.util.Map;
import static java.util.Arrays.stream;
import static java.util.stream.Collectors.groupingBy;
import static java.util.stream.Collectors.summingInt;
import static java.util.stream.Collectors.joining;

public class StockList {
  private static int stockCount(final String s) {
    return Integer.valueOf(s.split(" ")[1]);
  }
  
  public static String stockSummary(final String[] stock, final String[] categories) {
    if (stock.length == 0 || categories.length ==  0)
      return "";
    final Map<String, Integer> counts = stream(stock)
        .collect(groupingBy(s -> s.substring(0, 1), summingInt(StockList::stockCount)));
    return stream(categories)
        .map(s -> "(" + s + " : " + counts.getOrDefault(s, 0) + ")")
        .collect(joining(" - "));
  }
}
________________________________________
import java.util.stream.Stream;
import java.util.stream.Collectors;
public class StockList { 
  public static String stockSummary(String[] arts, String[] cats) {
    if (arts.length == 0) return "";
    final int space = arts[0].indexOf(" ");
    return Stream.of(cats)
      .map(c -> c + " : " + Stream.of(arts)
        .filter(a -> c.contentEquals(a.subSequence(0, 1)))
        .map(a -> a.substring(space + 1))
        .mapToInt(Integer::parseInt)
        .sum())
      .map(s -> "(" + s + ")")
      .collect(Collectors.joining(" - "));
  }
}
________________________________________
public class StockList { 
  public static String stockSummary(String[] lstOfArt, String[] lstOf1stLetter) {
    if (lstOfArt.length == 0 || lstOf1stLetter.length == 0) return "";
    
    int sum = 0;
    String res = "";
    
    for (String i : lstOf1stLetter) {
        sum = 0;
        for (String j : lstOfArt) {
            sum += j.substring(0,1).equals(i) ? Integer.parseInt(j.replaceAll("[^0-9]","")) : 0;
        }
        res += " - (" + i + " : " + sum + ")";
    }
    
    return res.substring(3);
  }
}
________________________________________
import static java.util.Arrays.stream;
import static java.util.stream.Collectors.groupingBy;
import static java.util.stream.Collectors.joining;
import static java.util.stream.Collectors.summingInt;

class StockList {
  static String stockSummary(String[] lstOfArt, String[] lstOf1stLetter) {
    if (lstOfArt.length > 0 && lstOf1stLetter.length > 0) {
      var counts = stream(lstOfArt).collect(groupingBy(s -> s.substring(0, 1), summingInt(s -> Integer.parseInt(s.split(" ")[1]))));
      return stream(lstOf1stLetter).map(s -> "(" + s + " : " + counts.getOrDefault(s, 0) + ")").collect(joining(" - "));
    }
    return "";
  }
}
