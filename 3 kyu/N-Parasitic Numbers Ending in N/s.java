55df87b23ed27f40b90001e5


import java.math.BigInteger;

public class Kata
{
    public static String calculateSpecial(int lastDigit, int radix) {
        StringBuilder result = new StringBuilder(Integer.toString(lastDigit, radix));
        int nextDigit = lastDigit;
        int carry = 0;
        while ((nextDigit + carry) != 1) {
            int prod = (nextDigit * lastDigit) + carry;
            nextDigit = prod % radix;
            carry = prod / radix;
            result.append(Integer.toString(nextDigit, radix));
        }
        result.append(Integer.toString(nextDigit + carry, radix));
        return result.reverse().toString();
    }
}
____________________________
import java.math.BigInteger;

public class Kata {
    public static String calculateSpecial(int lastDigit, int radix) {
        int mod = lastDigit * radix - 1;
        int numDigits = 0;
        int pow = 1;
        do {
            numDigits++;
            pow = (pow * radix) % mod;
        } while (pow != 1);
        return BigInteger.valueOf(radix).pow(numDigits).subtract(BigInteger.ONE)
                .divide(BigInteger.valueOf(mod)).multiply(BigInteger.valueOf(lastDigit))
                .toString(radix).toUpperCase();
    }
}
____________________________
public class Kata
{
    public static String calculateSpecial(int lastDigit, int radix) {
        String rez = "";
        int divider = lastDigit*radix-1;
        int rest = lastDigit;
        do {
            rest *= radix;
            rez += Integer.toString(rest/divider, radix);
            rest %= divider;
        }
        while (rest!=lastDigit);
        return rez;
    }
}
