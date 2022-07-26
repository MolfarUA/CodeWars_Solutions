587f0abdd8730aafd4000035


import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.nio.charset.StandardCharsets;

public class Cracker {
  
  private static String[] permutations(final String s) {
    // Finds all permutations of the provided string with potential duplicates
    if (s.isEmpty())
      return new String[] {""};
    String[]
      a = permutations(s.substring(1, s.length())),
      result = new String[s.length() * a.length];
    for (int i = 0; i < s.length(); i++)
      for (int j = 0; j < a.length; j++)
        result[i * a.length + j] = new StringBuilder(a[j]).insert(i, s.charAt(0)).toString();
    return result;
  }
  
  // Helper function to convert bytes returned by MessageDigest::digest
  // into a hex string
  // Source: http://www.baeldung.com/sha-256-hashing-java
  private static String bytesToHex(byte[] hash) {
    StringBuffer hexString = new StringBuffer();
    for (int i = 0; i < hash.length; i++) {
      String hex = Integer.toHexString(0xff & hash[i]);
      if (hex.length() == 1)
        hexString.append('0');
      hexString.append(hex);
    }
    return hexString.toString();
  }
  
  public static String crackSha256(String h, String s) {
    MessageDigest sha256 = null;
    try {
      sha256 = MessageDigest.getInstance("SHA-256");
    } catch (NoSuchAlgorithmException e) {
      /* uhhh ... I'm not sure how to handle this exception if it occurs :p */
    }
    for (String msg : permutations(s))
      if (bytesToHex(sha256.digest(msg.getBytes(StandardCharsets.UTF_8))).equals(h))
        return msg;
    return null;
  }
}
_________________________
import static java.security.MessageDigest.getInstance;
import static java.util.stream.IntStream.range;

import java.math.BigInteger;
import java.util.stream.Stream;

interface Cracker {
  static String crackSha256(String hash, String chars) {
    return permutations(chars).filter(opt -> {
          try {
            return String.format("%064x", new BigInteger(1, getInstance("SHA-256").digest(opt.getBytes()))).equals(hash);
          } catch (Exception e) {
            return false;
          }
        }).findFirst().orElse(null);
  }

  private static Stream<String> permutations(String s) {
    return s.isEmpty() ? Stream.of(s) : range(0, s.length()).boxed().flatMap(i -> permutations(s.substring(0, i) + s.substring(i + 1)).map(x -> s.charAt(i) + x));
  }
}
_________________________
import static java.util.function.Function.identity;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.stream.IntStream;
import java.util.stream.Stream;
import javax.xml.bind.DatatypeConverter;

public class Cracker {

  private final MessageDigest digester;

  static String crackSha256(final String hash, final String chars) {
    return new Cracker().crack(hash, chars);
  }

  Cracker() {
    try {
      digester = MessageDigest.getInstance("SHA-256");
    } catch (final NoSuchAlgorithmException e) {
      throw new RuntimeException(e);
    }
  }

  String crack(final String hash, final String chars) {
    return permute("", chars)
        .filter(charPermutation -> hash.equals(encoded(charPermutation)))
        .findAny().orElse(null);
  }

  static Stream<String> permute(final String prefix, final String tail) {
    return tail.isEmpty() ? Stream.of(prefix) : IntStream.range(0, tail.length())
        .mapToObj(i -> permute(prefix + tail.charAt(i), removeChar(tail, i)))
        .flatMap(identity());
  }

  private static String removeChar(final String string, final int index) {
    return string.substring(0, index) + string.substring(index + 1);
  }

  private String encoded(final String permutation) {
    return DatatypeConverter.printHexBinary(digester.digest(permutation.getBytes())).toLowerCase();
  }
}
