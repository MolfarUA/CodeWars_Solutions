import java.util.Arrays;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

public class KataSolution {

  public static int nOverK(int n, int k) {
    if (n < k)
      return 0;
    if (k == 0 || k == n)
      return 1;
    return nOverK(n - 1, k - 1) + nOverK(n - 1, k);
  }

  public static String expand(String expr) {

    Matcher m = Pattern.compile("(\\-?\\d*)([a-z])([+-])(\\-?\\d+)\\D+(\\d+)").matcher(expr);
    m.find();
    int p = Integer.parseInt(m.group(5));
    String[] str = new String[p + 1];
    int a = m.group(1).length() == 0 ? 1 : m.group(1).equals("-") ? -1 : Integer.parseInt(m.group(1));
    int b = (m.group(3).equals("-") ? -1 : 1) * Integer.parseInt(m.group(4));
    for (int i = 0; i <= p; i++) {
      long f = (long) (nOverK(p, i) * Math.pow(a, p - i) * (i == 0 ? 1 : Math.pow(b, i)));
      if (f != 0) {
        str[i] = p - i == 0 ? f + ""
            : (f == 1 ? "" : f == -1 ? "-" : f) + m.group(2) + (p - i != 1 ? "^" + (p - i) : "");
      }
    }
    return Arrays.stream(str).filter(s -> s != null).collect(Collectors.joining("+")).replaceAll("\\+\\-", "\\-");
  }
}

___________________________________________________
import java.util.regex.*;
import java.util.*;
import java.lang.*;

public class KataSolution 
{
    public static String expand(String expr) 
    {
        Pattern pattern = Pattern.compile("\\((-?\\d*)(.)([-+]\\d+)\\)\\^(\\d+)");
        Matcher matcher = pattern.matcher(expr);
        matcher.find();
      
        final String _a = matcher.group(1);
        final int a = _a.isEmpty() ? 1 : _a.equals("-") ? -1 : Integer.parseInt(_a);
        final String x = matcher.group(2);
        final int b = Integer.parseInt(matcher.group(3).replace("+", ""));
        final int n = Integer.parseInt(matcher.group(4).replace("+", ""));
        double f = Math.pow((double)a, n);
      
        if (n == 0) return "1";
        if (a == 0) return String.format("%d", (int)Math.pow((double)b, n));
        if (b == 0) return String.format("%d%s%s", (int)f, x, (n > 1) ? String.format("^%d", n) : "");
      
        final StringBuilder result = new StringBuilder();
        for (int i = 0; i <= n; i++) 
        {
            if (f > 0 && i > 0) result.append("+");
            if (f < 0) result.append("-");
            if (i > 0 || f * f > 1) result.append((long)Math.abs(f));
            if (i < n) result.append(x);
            if (i < n - 1) result.append(String.format("^%d", n - i));
            f = f * (n - i) * b / (double)a / (double)(i + 1);
        }
      
        return result.toString();
    }
}

___________________________________________________
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class KataSolution {
  static Pattern pattern = Pattern.compile("\\(([\\+\\-]?)(\\d*)([a-z])(\\+|\\-)(\\d+)\\)\\^(\\d+)");
  
  public static long fact(int i) {
    if(i <= 1) return 1;
    return i * fact(i - 1);
  }
    
  public static long binomial(int n, int k) {
    return fact(n) / fact(k) / fact(n-k);
  }

  public static String expand(String expr) {
    Matcher matcher = pattern.matcher(expr);
    if (matcher.matches()) {
      String sgn1 = matcher.group(1);
      String str1 = matcher.group(2);
      int int1 = str1.equals("") ? 1 : Integer.parseInt(str1);
      if (sgn1.equals("-")) int1 *= -1;
      String var = matcher.group(3);
      String sgn2 = matcher.group(4);
      String str2 = matcher.group(5);
      int int2 = str2.equals("") ? 1 : Integer.parseInt(str2);
      if (sgn2.equals("-")) int2 *= -1;
      int exp = Integer.parseInt(matcher.group(6));
      
      if (exp == 0) return "1"; // special case
      
      StringBuilder strbuild = new StringBuilder();
      for (int i = exp; i >= 0; i--) { // for each order
        long num = (long) (binomial(exp, i) * Math.pow(int1,i) * Math.pow(int2, (exp-i))); // binomial expression
        String varstring = i==0 ? "" : i==1 ? var : (var+"^"+i);
        if (num == 0) continue;
        else if (i == 0) strbuild.append(num>=0 ? "+" + num : num);
        else if (num == 1) strbuild.append("+" + varstring);
        else if (num == -1) strbuild.append("-" + varstring);
        else if (num > 0) strbuild.append("+" + num + varstring);
        else if (num < 0) strbuild.append(num + varstring);
      }
      if (strbuild.charAt(0) == '+') strbuild.deleteCharAt(0); // ignore leading +
      return strbuild.toString();
    } else { // no match
      return "";
    }
  }
}

___________________________________________________
import java.util.*;

public class KataSolution {

    public static String expand(String expr) {
        int n = getN(expr);
        if (n == 0) {
            return "1";
        } else if (n == 1) {
            return expr
                    .replaceAll(".*(?=\\()", "")
                    .replaceAll("(?<=\\)).*", "")
                    .replaceAll("\\(", "")
                    .replaceAll("\\)", "")
                    .trim();
        }

        long a = getA(expr);
        long b = getB(expr);
        String x = getX(expr);

        Map<Integer, String> result = new HashMap<>();
        long firstA = ((Double)Math.pow(a, n)).longValue();
        if (firstA == 1) {
            result.put(0, String.format("%s^%d", x, n));
        } else if (firstA == -1) {
            result.put(0, String.format("-%s^%d", x, n));
        } else {
            result.put(0, String.format("%d%s^%d", firstA, x, n));
        }
        if (b == 0) {
            return formatResult(result);
        }
        for (int index = 1; index < n; index++) {
            result.put(index, String.format("%s%s", formatNumber(getC(n, index)
                            * ((Double)Math.pow(a, n - index)).longValue()
                            * ((Double)Math.pow(b, index)).longValue()),
                    formatVariable(x, n - index)));
        }
        result.put(n, formatNumber(((Double)Math.pow(b, n)).longValue()));
        return formatResult(result);
    }

    private static String formatVariable(String x, int n) {
        return n < 2 ? x : String.format("%s^%d", x, n);
    }

    private static String formatResult(Map<Integer, String> result) {
        return String.join("", result.values());
    }

    private static String formatNumber(long number) {
        String formattedC = String.valueOf(number);
        if (!formattedC.contains("-")) {
            formattedC = String.format("+%s", formattedC);
        }
        return formattedC;
    }

    private static long getC(int n, int k) {
        if (k == 0) {
            return 1;
        }
        long bottomFactorial = getFactorial(k == (n - k) ? k : Math.min(k, (n-k)));
        long upperFactor = 1;
        for (long i = Math.max(k, (n - k)) + 1; i <= n; i++) {
            upperFactor *= i;
        }
        return  upperFactor / bottomFactorial;
    }

    public static long getFactorial(long number) {
        long result = 1;
        for (long factor = 2; factor <= number; factor++) {
            result *= factor;
        }
        return result;
    }

    private static String getX(String expression) {
        return expression
                .replaceAll(".*(?=[a-zA-Z])", "")
                .replaceAll("(?<=[a-zA-Z]).*", "")
                .trim();
    }

    private static int getA(String expression) {
        String a = expression
                .replaceAll("(?<=[a-zA-Z]).*", "")
                .replaceAll("\\(", "")
                .trim();
        return getOptionalNegativeNumber(a);
    }

    private static int getB(String expression) {
        String b = expression
                .replaceAll(".*(?=[+-])", "")
                .replaceAll("(?<=\\)).*", "")
                .replaceAll("\\)", "")
                .trim();
        return getOptionalNegativeNumber(b);
    }

    private static int getOptionalNegativeNumber(String number) {
        int result = 1;
        if (number.matches("-.*")) {
            result = -1;
        }
        number = number.replaceAll("[^\\d]", "").trim();
        if (!"".equals(number)) {
            result = result * Integer.parseInt(number);
        }
        return result;
    }

    private static int getN(String expression) {
        return Integer.parseInt(expression
                .replaceAll(".*(?=\\^)", "")
                .replaceAll("\\^", "")
                .trim());
    }
}

___________________________________________________
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class KataSolution {

  private static final Map<Long, Long> factorialCache = new HashMap<>();

    public static String expand(final String expr) {
        final BinomialExpression expression = BinomialExpression.parseExpr(expr);

        if (expression == null) {
            return "Invalid Binomial Expression";
        }

        StringBuilder expandedExpr = new StringBuilder();
        for (long k = 0; k <= expression.exponent; k++) {
            generateTerm(expandedExpr, expression, k);
        }

        return expandedExpr.toString();
    }

    private static void generateTerm(final StringBuilder result, final BinomialExpression expression, final long k) {
        final long combinatoric = combinatoric(expression.exponent, k);
        long coefficient =  Math.round(Math.pow(expression.term, k)) * combinatoric;
        final long exponent = expression.exponent - k;
        if (exponent != 0) {
            coefficient *= Math.round(Math.pow(expression.coefficient, exponent));
        }

        if (coefficient == 0) {
            return;
        }

        if (k != 0 && coefficient >= 0 && (exponent != 0 || coefficient > 0)) {
            result.append('+');
        }

        if (coefficient == -1 && exponent != 0) {
            result.append('-');
        } else if (exponent == 0 || coefficient != 1) {
            result.append(coefficient);
        }

        if (exponent > 0) {
            result.append(expression.variableLetter);
        }

        if (exponent > 1) {
            result.append('^');
            result.append(exponent);
        }
    }

    private static long combinatoric(final long n, final long k) {
        return factorial(n) / (factorial(k) * factorial(n - k));
    }

    private static long factorial(long n) {
        Long cachedValue = factorialCache.get(n);
        if (cachedValue != null) {
            return cachedValue;
        }
        if (n == 1 || n == 0) {
            return 1;
        }
        final long result = n * factorial(n - 1);
        factorialCache.put(n, result);
        return result;
    }

    private static class BinomialExpression {

        private static final Pattern REGEX = Pattern.compile("\\((-?\\d*)([a-z])([+-]\\d+)\\)\\^(\\d+)");

        final long coefficient;
        final char variableLetter;
        final long term;
        final long exponent;

        private static BinomialExpression parseExpr(final String expr) {
            final Matcher matcher = REGEX.matcher(expr);

            if (!matcher.find()) {
                return null;
            }

            long coefficient = 1;
            if (!matcher.group(1).isEmpty()) {
                if (matcher.group(1).equals("-")) {
                    coefficient = -1;
                } else {
                    coefficient = Long.parseLong(matcher.group(1));
                }
            }
            final char variableLetter = matcher.group(2).charAt(0);
            final long term = Long.parseLong(matcher.group(3));
            final long exponent = Long.parseLong(matcher.group(4));

            return new BinomialExpression(coefficient, variableLetter, term, exponent);
        }

        private BinomialExpression(final long coefficient, final char variableLetter, final long term, final long exponent) {
            this.coefficient = coefficient;
            this.variableLetter = variableLetter;
            this.term = term;
            this.exponent = exponent;
        }
    }
}
