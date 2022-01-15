class CodeDecode {
    public static String code(String str) {
        StringBuilder out=new StringBuilder();
        
        for(char c:str.toCharArray()) {
            String b=Integer.toBinaryString(Character.getNumericValue(c));
            out.append("0".repeat(b.length()-1)+"1"+b);
        }
        return out.toString();
    }
    
    public static String decode(String str) {
        StringBuilder out=new StringBuilder();
        
        for(int i=0,k=1;i<str.length();i++,k++)
            if(str.charAt(i)=='1') {
                out.append(Integer.parseInt(str.substring(i+1,i+1+k),2));
                i+=k; k=0;
            }
        return out.toString();
    }
}
__________________________
class CodeDecode {
    
    private static String dec2Bin(String s) {
        String[] dict = {"10", "11", "0110", "0111", "001100", "001101", "001110", "001111", "00011000", "00011001"};
        return dict[Integer.parseInt(s)];
    }
    public static String code(String strng) {
        int lg = strng.length();  
        String[] ret = new String[lg];
        for (int start = 0; start < lg; start += 1) { 
            String d = Character.toString(strng.charAt(start));
            ret[start] = dec2Bin(d);
        }
        return String.join("", ret);
    }
    public static String decode(String str) {
        String ret = "";
        int i = 0;
        int lg = str.length();
        while (i < lg) {
            int zero_i = i;
            while ((zero_i < lg) && (str.charAt(zero_i) != '1'))
                zero_i++;
            int l = zero_i - i + 2;
            String ss = str.substring(zero_i + 1, zero_i + l);
            ret += Integer.toString(Integer.parseInt(ss, 2), 10);
            i = zero_i + l;
        }
        return ret;
    }
}
__________________________
class CodeDecode {
  public static String code(String str) {
    return str.chars().boxed()
      .map(charCode -> Integer.toBinaryString(charCode - '0'))
      .map(binaryStr -> "0".repeat(binaryStr.length() - 1).concat("1").concat(binaryStr))
      .reduce("", String::concat);
  }

  public static String decode(String str) {
    if (str.length() == 0) return "";
    int i = str.indexOf("1");
    return String.valueOf(Integer.parseInt(str.substring(i + 1, 2 * i + 2), 2))
      .concat(decode(str.substring(2 * i + 2)));
  }
}
__________________________
import static java.util.stream.Collectors.joining;

import java.util.List;

class CodeDecode {
  static final List<String> CODES = List.of("10", "11", "0110", "0111", "001100", "001101", "001110", "001111", "00011000", "00011001");

  static String code(String strng) {
    return strng.chars().map(c -> c - 48).mapToObj(CODES::get).collect(joining());
  }

  static String decode(String str) {
    var decoded = new StringBuilder();
    for (int i = 0, l = 1; i < str.length(); i++, l++)
      if (str.charAt(i) == '1') {
        decoded.append(Integer.parseInt(str.substring(i + 1, (i += l) + 1), 2));
        l = 0;
      }
    return decoded.toString();
  }
}
__________________________
import java.util.regex.Matcher;
import java.util.regex.Pattern;

class CodeDecode {
    
    static String[] binaries = new String[] {"10", "11", "0110", "0111", "001100", "001101", "001110", "001111", "00011000", "00011001"};
    
    public static String code(String str) {
        String result = "";
        for (int i = 0; i < str.length(); i++) {
            for (int j = 0; j < binaries.length; j++) {
                if ((str.charAt(i) + "").equals(j +"")) {
                    result += binaries[j];
                    break;
                }
            }
        }
        return result;
    }
    
    public static String decode(String str) {
       String result = "";
        while (str.length() > 0) {
            for (int i = 0; i < binaries.length; i++) {
                Pattern p = Pattern.compile("^" + binaries[i] + "");
                Matcher m = p.matcher(str);
                if (m.find()) {
                    str = str.replaceFirst("^" + binaries[i] + "", "");
                    result += i;
                    break;
                }
            }
        }
        return result;
    }
}
