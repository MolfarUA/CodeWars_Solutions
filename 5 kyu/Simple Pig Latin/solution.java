public class PigLatin {
    public static String pigIt(String str) {
        return str.replaceAll("(\\w)(\\w*)", "$2$1ay");
    }
}

################
import java.util.Arrays;
import java.util.stream.Collectors;
import java.util.regex.Pattern;

public class PigLatin {
    public static String pigIt(String str) {
        return Arrays.stream(str.trim().split(" "))
                .map(v -> v.matches("[a-zA-Z]+") ? v.substring(1).concat(v.substring(0, 1)).concat("ay") : v)
                .collect(Collectors.joining(" "));
    }
}

#######################
import java.util.Arrays;
import java.util.stream.Collectors;
import java.util.regex.Pattern;

public class PigLatin {
    public static String pigIt(String str) {
         return Arrays.stream(str.split(" "))
                .map(PigLatin::convertString)
                .collect(Collectors.joining(" "));

    }

    private static String convertString(String s) {
        if (!Pattern.matches("\\p{Punct}", s)){
            char firstLetter = s.charAt(0);
            return new StringBuilder(s).deleteCharAt(0).append(firstLetter).append("ay").toString();
        }
        return s;
    }
}

##################
import java.util.Arrays;
public class PigLatin {
    public static String pigIt(String str) {
        StringBuilder sb = new StringBuilder();
        Arrays.stream(str.split(" ")).forEachOrdered(s -> {
            char c = s.charAt(0);
            if (c >= 'a' && c <= 'z' || c >= 'A' && c <= 'Z')
              sb.append(s.substring(1)).append(s.charAt(0)).append("ay ");
            else
              sb.append(c);
        });
        return sb.toString().stripTrailing();
    }
}

################
import java.util.regex.Pattern;

public class PigLatin {
    public static String pigIt(String str) {
        // Write code here
        String latinised = "";

        String[] splits = str.split(" ");

        //test with
        for(String s : splits) {
            System.out.println(s);
            if (!Pattern.matches("\\p{Punct}", s)) {
                s = s.replace(" ", "");
                s = s.substring(1) + s.charAt(0) + "ay ";
                latinised += s;  
            }else{
              latinised += s;
            }
        }
        System.out.println(latinised.trim());
        return latinised.trim();

    }
}
