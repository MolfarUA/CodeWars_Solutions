5470c635304c127cad000f0d


import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.stream.Collectors;



public class RegExpParser {
    
    static class InvalidRegex extends RuntimeException {}
    
    private LinkedList<Character> tokens;
    
    public RegExpParser(final String input) {
        tokens = new LinkedList<Character>(input.chars()
                                                .mapToObj( i -> new Character((char) i))
                                                .collect(Collectors.toList()));
    }
    
    public RegExp parse() {
        RegExp ans;
        try {                    ans = parse_Or(); }
        catch (InvalidRegex e) { ans = new Void(); }
        
        return hasChar() ? new Void(): ans;
    }
    
    private char    popChar()  { return tokens.remove(); }
    private char    peekChar() { return tokens.peek(); }
    private boolean hasChar()  { return !tokens.isEmpty(); }

    private RegExp parse_Or() {
        RegExp or_ = parse_Str();
        if (hasChar() && peekChar() == '|') {
            popChar();
            or_ = new Or(or_, parse_Str()); 
        }
        return or_;
    }

    private RegExp parse_Str() {
        List<RegExp> str_ = new ArrayList<RegExp>();
        while (hasChar() && !"*)|".contains(Character.toString(peekChar())))
            str_.add(parse_ZeroMul());
        
        return str_.isEmpty()  ? new Void() :
               str_.size() > 1 ? new Str(str_)
                               : str_.get(0);
    }

    private RegExp parse_ZeroMul() {
        RegExp zm = parse_Term();
        if (!(zm instanceof Void) && hasChar() && peekChar() == '*') {
            popChar();
            zm = new ZeroOrMore(zm);
        }
        return zm;
    }

    private RegExp parse_Term() {
        if (!hasChar()) throw new InvalidRegex();
        char was =  popChar();
        
        RegExp expr;
        if (was == '(') {
            if (!hasChar() || peekChar() == ')') throw new InvalidRegex();
            expr = parse_Or();
            if (!hasChar() || peekChar() != ')') throw new InvalidRegex();
            popChar();
        
        } else if (was == '.') 
            expr = new Any();
        
          else if (!"()*|".contains(Character.toString(was)))  
              expr = new Normal(was);
          
          else
              throw new RuntimeException("Wrong code: You should never get there...");
        
        return expr;
    }
}
____________________________________________________________
import java.util.ArrayList;
import java.util.Deque;
import java.util.LinkedList;
import java.util.List;

public class RegExpParser {

  private final String pattern;

  public RegExpParser(final String input) {
    this.pattern = input;
  }

  public RegExp parse() {
    try {
      return parse(pattern);
    } catch (IllegalArgumentException e) {
      return new Void();
    }
  }

  private static RegExp parse(String pattern) {
    pattern = '(' + pattern + ')';

    LinkedList<RegExp> stack = new LinkedList<>();

    Deque<Integer> openParenthesesStack = new LinkedList<>();

    Deque<int[]> ORStack = new LinkedList<>();

    for (int i = 0; i < pattern.length(); i++) {
      char c = pattern.charAt(i);

      switch (c) {
        case '(':
          openParenthesesStack.add(stack.size());
          break;
        case ')':
          Integer index = openParenthesesStack.pollLast();
          if (index == null) {
            throw new IllegalArgumentException(pattern);
          }

          int[] ORIndex = ORStack.peekLast();
          if (ORIndex != null && ORIndex[0] == index) {
            ORStack.pollLast();
            List<RegExp> chunk = stack.subList(ORIndex[1], stack.size());

            if (chunk.size() >= 2) {
              RegExp seq = chunkToSeq(chunk);
              chunk.clear();
              stack.add(seq);
            }

            RegExp second = stack.pollLast();
            RegExp first = stack.pollLast();
            Or or = new Or(first, second);

            stack.add(or);

            System.out.println();

          } else {
            List<RegExp> chunk = stack.subList(index, stack.size());

            if (chunk.size() >= 2) {
              RegExp seq = chunkToSeq(chunk);
              chunk.clear();
              stack.add(seq);
            }
          }


          break;
        case '*':
          RegExp regExp = stack.pollLast();
          if (regExp == null) {
            throw new IllegalArgumentException(pattern);
          }

          if (regExp instanceof ZeroOrMore) {
            throw new IllegalArgumentException(pattern);
          }

          ZeroOrMore zeroOrMore = new ZeroOrMore(regExp);
          stack.add(zeroOrMore);
          break;
        case '|':
          Integer parentheseIndex = openParenthesesStack.peekLast();
          if (parentheseIndex == null) {
            throw new IllegalArgumentException(pattern);
          }

          int[] lastOR = ORStack.peekLast();
          if (lastOR != null) {
            if (lastOR[0] == parentheseIndex) {
              throw new IllegalArgumentException(pattern);
            }
          }

          List<RegExp> chunkToEvaluate = stack.subList(parentheseIndex, stack.size());

          if (chunkToEvaluate.size() >= 2) {
            RegExp seq = chunkToSeq(chunkToEvaluate);
            chunkToEvaluate.clear();
            stack.add(seq);
          }

          ORStack.addLast(new int[]{parentheseIndex, stack.size()});
          break;
        case '.':
          stack.add(new Any());
          break;
        default:
          stack.add(new Normal(c));
          break;
      }
    }

    if (!openParenthesesStack.isEmpty() || stack.size() != 1) {
      throw new IllegalArgumentException(pattern);
    }

    return stack.poll();
  }

  private static RegExp chunkToSeq(List<RegExp> chunk) {
    assert chunk.size() > 2;

    return new Str(new ArrayList<>(chunk));
  }
}
____________________________________________________________
import java.util.*;

public class RegExpParser {
    private final String s;
    private final int end;
    private int i;

    public RegExpParser(String input) {
        s = input;
        end = s.length();
    }

    private RegExp fromList(List<RegExp> list) {
        switch (list.size()) {
            case 0:
                return null;
            case 1:
                return list.get(0);
            default:
                return new Str(list);
        }
    }

    private RegExp parse(boolean rprEnd) {
        List<RegExp> reList = new ArrayList<>();
        loop:
        for (; i < end; i++) {
            char c = s.charAt(i);
            switch (c) {
                case '(':
                    i++;
                    RegExp inner = parse(true);
                    if (inner == null)
                        return null;
                    reList.add(inner);
                    break;
                case ')':
                    if (rprEnd)
                        break loop;
                    else
                        return null;
                case '*':
                    int k = reList.size() - 1;
                    if (k < 0)
                        return null;
                    RegExp last = reList.get(k);
                    if (last instanceof ZeroOrMore)
                        return null;
                    reList.set(k, new ZeroOrMore(last));
                    break;
                case '|':
                    RegExp first = fromList(reList);
                    i++;
                    RegExp second = parse(rprEnd);
                    if (first == null || second == null || second instanceof Or)
                        return null;
                    else
                        return new Or(first, second);
                case '.':
                    reList.add(new Any());
                    break;
                default:
                    reList.add(new Normal(c));
                    break;
            }
        }
        if (rprEnd && i == end)
            return null;
        return fromList(reList);
    }

    public RegExp parse() {
        i = 0;
        RegExp result = parse(false);
        return result == null ? new Void() : result;
    }
}
____________________________________________________________
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Objects;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class RegExpParser {
    private static final Pattern PATTERN_WORD = Pattern.compile("(\\w|\\,|\\^|\\s|\\&|\\}|\\]|\\{|\\#|\\@|<|\\>|\\[|\\?|\\`|\\!|\\+|\\/|\\\\|\\:|\\%|\\,\\/|\\=|\\-|\\;|\\'|\\$|\\\")");
    private static final Set<String> SET_SPECIAL_CHARS = new HashSet<>(Arrays.asList("*", "|", "."));

    final String input;
    public RegExpParser(final String input) {
        this.input = input;
    }

    private RegExp parse(final String subinput) {
        if (".".equals(subinput)) {
            return new Any();
        }

        final List<RegExp> wordlist = new ArrayList<>();
        RegExp result = null;
        RegExp lastRegExp = null;
        for (int i = 0; i < subinput.length(); i++) {
            final char c = subinput.charAt(i);
            final String stringChar = String.valueOf(c);
            final Matcher matcher = PATTERN_WORD.matcher(stringChar);
            if (matcher.find()) {
                lastRegExp = new Normal(c);
                wordlist.add(lastRegExp);
                continue;
            }
            if (".".equals(stringChar)) {
                lastRegExp = new Any();
                wordlist.add(lastRegExp);
                continue;
            }

            if ("|".equals(stringChar)) {
                final RegExp subres = ((i + 1) == subinput.length()) ? null : parse(subinput.substring(i + 1));
                if (subres instanceof Void || subres instanceof Or) {
                    return new Void();
                }

                return new Or(
                        wordlist.isEmpty() ? new Void() : (wordlist.size() > 1 ? new Str(new ArrayList<>(wordlist)) : wordlist.get(0)),
                        Objects.isNull(subres) ? new Void() : subres);
            }
            if ("*".equals(stringChar)) {
                if (lastRegExp instanceof ZeroOrMore || Objects.isNull(lastRegExp)) {
                    return new Void();
                }           
                wordlist.remove(wordlist.size() - 1);
                lastRegExp = new ZeroOrMore(lastRegExp);
                wordlist.add(lastRegExp);
                continue;
            }
            if ("(".equals(stringChar)) {
                final int indexOfClosingBrace = indexOfClosingBrace(subinput.substring(i));
                final RegExp reg = parse(subinput.substring(i + 1, i + indexOfClosingBrace));
                if (reg instanceof Void) {
                    return new Void();
                }
                lastRegExp = reg;
                wordlist.add(reg);
                i = i + indexOfClosingBrace;
            }
        }

        if (wordlist.size() == 1) {
            result = wordlist.get(0);
        } else if (wordlist.size() > 1) {
            result = new Str(new ArrayList<>(wordlist));
        }

        return Objects.isNull(result) ? new Void() : result;
    }

    public RegExp parse() {        
        if (SET_SPECIAL_CHARS.contains(input) && !".".equals(input)) {
            return new Void();
        }
        //Check braces
        int braceCounter = 0;
        for (int i = 0; i < input.length(); i++) {
            final char c = input.charAt(i);
            braceCounter = braceCounter + ('(' == c ? 1 : (')' == c ? -1 : 0));
            if (braceCounter < 0) {
                return new Void();
            }
        }
        if (braceCounter > 0) {
            return new Void();
        }
        return parse(input);
    }

    private int indexOfClosingBrace(final String inputstring) {
        int count = 1;
        for (int i = 1; i < inputstring.length(); i++) {
            final char c = inputstring.charAt(i);
            switch(c) {
                case ')': count--; break;
                case '(': count++; break;
                default: continue;

            }
            if (count == 0) {
                return i;
            }
        }
        return -1;
    }
}
