54b72c16cd7f5154e9000457


import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class MorseCodeDecoder {
    public static String decodeBits(String bits) {
        String trimmedBits = bits.replaceAll("^0+|0+$", "");
        int rate = getRate(trimmedBits);

        String morseCode = "";
        for (String word : trimmedBits.split("0{"+ (7 * rate) +"}")) {
            for (String letter : word.split("0{"+ (3 * rate) +"}")) {
                for (String dot : letter.split("0{" + rate + "}")) {
                    morseCode += dot.length() > rate ? '-' : '.';
                }
                morseCode += ' ';
            }
            morseCode += "  ";
        }
        return morseCode;
    }

    private static int getRate(String bits) {
        int rate = Integer.MAX_VALUE;
        Matcher matcher = Pattern.compile("1+|0+").matcher(bits);
        while (matcher.find()) {
            rate = Math.min(rate, matcher.group().length());
        }
        return rate;
    }

    public static String decodeMorse(String morseCode) {
        String decoded = "";
        for (String word : morseCode.trim().split("   ")) {
            for (String letter : word.split(" ")) {
                decoded += MorseCode.get(letter);
            }
            decoded += ' ';
        }
        return decoded.trim();
    }
}
_____________________________
import java.util.regex.Pattern;
import java.util.regex.MatchResult;

public class MorseCodeDecoder {
    public static String decodeBits(String bits) {
        bits = bits.replaceAll("^0*|0*$", "");
        int timeUnit = Pattern.compile("0+|1+")
                              .matcher(bits)
                              .results()
                              .map(MatchResult::group)
                              .mapToInt(String::length)
                              .min()
                              .orElseGet(bits::length);
        return bits.replace("111".repeat(timeUnit), "-")
                   .replace("000".repeat(timeUnit), " ")
                   .replace("1".repeat(timeUnit), ".")
                   .replace("0".repeat(timeUnit), "");
    }
    
    public static String decodeMorse(String morseCode) {
        String decoded = "";
        for (String word : morseCode.split(" "))
            if (word.equals("")) decoded += " ";
            else decoded += MorseCode.get(word);
        return decoded;
    }
}
_____________________________
import java.util.stream.Stream;

import static java.util.stream.Collectors.joining;

public class MorseCodeDecoder {
  
  public static String decodeBits(String bits) {
    bits = bits.replaceAll("^0*|0*$", "");
    String min0 = Stream.of(bits.replaceAll("^1*|1$", "").replaceAll("1+", " ").split(" ")).min( (s1,s2) -> Integer.compare(s1.length(), s2.length())).get();
    String min1 = Stream.of(bits.replaceAll("0+", " ").split(" ")).min( (s1,s2) -> Integer.compare(s1.length(), s2.length())).get();
    
    int rate = min0.length() < min1.length() && !min0.isEmpty() ? min0.length(): min1.length();
    return Stream.of(bits.split("0{" + rate * 7 + "}"))
          .map(s -> Stream.of(s.split("0{" + rate * 3 + "}"))
                            .map(s1 -> Stream.of(s1.split("0{" + rate + "}"))
                                            .map(s2 -> s2.length() >= rate * 3 ? "-" : ".")
                                            .collect(joining()))
                            .collect(joining(" ")))
          .collect(joining("   "));
  }

  public static String decodeMorse(String morseCode) {
    return Stream.of(morseCode.replace("   ", " _ ").split(" ")).map(s -> "_".equals(s) ? " " : MorseCode.get(s)).collect(joining());
  }
}
