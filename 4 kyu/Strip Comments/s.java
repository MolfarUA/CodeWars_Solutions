51c8e37cee245da6b40000bd


import java.util.Arrays;
import java.util.stream.Collectors;

public class StripComments {

  public static String stripComments(String text, String[] commentSymbols) {
    String pattern = String.format(
        "[ ]*([%s].*)?$",
        Arrays.stream( commentSymbols ).collect( Collectors.joining() )
    );
    return Arrays.stream( text.split( "\n" ) )
        .map( x -> x.replaceAll( pattern, "" ) )
        .collect( Collectors.joining( "\n" ) );
  }

}
__________________________________
public class StripComments {

  //Strip Comments
  public static String stripComments(String text, String[] commentSymbols) {

    String[] textByLine = text.split("\n");

    for (int i = 0; i < textByLine.length; i++) {
      for (String symbol : commentSymbols) {
        int symbolIndex = textByLine[i].indexOf(symbol);
        if (symbolIndex != -1) 
          textByLine[i] = textByLine[i].substring(0, symbolIndex);
      }
    }

    return generateTextFromLines(textByLine);
  }

  private static String generateTextFromLines(String[] textByLine) {

    String result = "";
    for (String line : textByLine) 
      result += line.replaceAll("\\s+$","") + '\n';

    return result.substring(0,result.length() - 1);
  }
  
}
__________________________________
public class StripComments {

  public static String stripComments(String text, String[] commentSymbols) {
      String[] lines = text.split("\n");
        for(int i = 0; i < lines.length; i++) {
            for(String commentSymbol: commentSymbols) {
                int position = lines[i].indexOf(commentSymbol);
                if(position >= 0) {
                    lines[i] = lines[i].substring(0, position);
                }
                lines[i] = lines[i].stripTrailing();
            }
        }
        return String.join("\n", lines);
  }
}
__________________________________
import java.util.Arrays;
import java.util.stream.Collectors;

public class StripComments {
    public static String stripComments(String text, String[] symbols) {
        return Arrays.stream(text.split("\n")).map(s -> {
            for (String symbol : symbols) s = s.replaceAll("(\\s+$)|(\\s*[" + symbol + "].*)", "");
            return s;
        }).collect(Collectors.joining("\n"));
    }
}
