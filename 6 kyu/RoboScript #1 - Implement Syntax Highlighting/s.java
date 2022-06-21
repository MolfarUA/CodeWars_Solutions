58708934a44cfccca60000c4



import java.util.*;
import java.util.regex.*;

public class RoboScript {

    public static String highlight(String code) {
        return code
              .replaceAll("(F+)", "<span style=\"color: pink\">$1</span>")
              .replaceAll("(L+)", "<span style=\"color: red\">$1</span>")
              .replaceAll("(R+)", "<span style=\"color: green\">$1</span>")
              .replaceAll("(\\d+)", "<span style=\"color: orange\">$1</span>");
    }

}
__________________________
import java.util.regex.Matcher;
import java.util.regex.Pattern;
public class RoboScript {

    public static String highlight(String code) {
        Pattern p = Pattern.compile("(F+|L+|R+|\\d+)");
        Matcher m = p.matcher(code);
        return m.replaceAll(match->{
            String c = match.group(1);
            String color = null;
            switch(c.charAt(0)) {
            case 'F': color = "pink"; break;
            case 'L': color = "red"; break;
            case 'R': color = "green"; break;
            default: color = "orange";
            }
            return "<span style=\"color: "+color+"\">"+c+"</span>";
        });
    }

}
__________________________
import java.util.function.UnaryOperator;

class RoboScript {
  static String highlight(String code) {
    UnaryOperator<String> span = c -> String.format("<span style=\"color: %s\">$1</span>", c);
    return code.replaceAll("(F+)", span.apply("pink")).replaceAll("(L+)", span.apply("red")).replaceAll("(R+)", span.apply("green")).replaceAll("(\\d+)", span.apply("orange"));
  }
}
