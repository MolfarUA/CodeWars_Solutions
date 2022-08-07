5861487fdb20cff3ab000030


import java.util.LinkedList;

public class Boolfuck {
  public static String interpret(String code, String iinput) {
    LinkedList<Boolean> mem = new LinkedList<>();
    mem.addLast(false);
    
    int codeptr = 0, memptr = 0, nesting = 0;
    
    String output = "";
    char ocurrent = 0;
    byte obits = 0;
    
    StringBuilder input = new StringBuilder(iinput);
    int iindex = 0;
    char ibits = 0;
    
    while(codeptr >= 0 && codeptr < code.length()) {
      switch(code.charAt(codeptr)) {
        case '+': 
          mem.set(memptr, !mem.get(memptr));
          break;
        case '<': 
          if(memptr == 0) {
            mem.addFirst(false);
          } else {
            memptr--;
          }
          break;
        case '>':
          memptr++;
          if(memptr == mem.size()) {
            mem.addLast(false);
          }
          break;
        case '[': 
          if(mem.get(memptr)) break;
          nesting = 1;
          while(nesting > 0) {
            codeptr++;
            if(code.charAt(codeptr) == '[') nesting++;
            if(code.charAt(codeptr) == ']') nesting--;
          }
          break;
        case ']':
          if(!mem.get(memptr)) break;
          nesting = 1;
          while(nesting > 0) {
            codeptr--;
            if(code.charAt(codeptr) == '[') nesting--;
            if(code.charAt(codeptr) == ']') nesting++;
          }
          break;
        case ',':
          if(iindex == input.length()) {  mem.set(memptr, false); break; }
          mem.set(memptr, (input.charAt(iindex) & 1) == 1);
          input.setCharAt(iindex, (char)(input.charAt(iindex) >> 1));
          if(++ibits == 8) {
            ibits = 0;
            iindex++;
          }
          break;
        case ';':
          ocurrent >>= 1;
          ocurrent |= (mem.get(memptr) ? 128 : 0);
          if(++obits == 8) {
            obits = 0;
            output += ocurrent;
            ocurrent = 0;
          }
          break;
      }
      codeptr++;
    }
    if(obits > 0) { while(obits++ < 8) ocurrent >>= 1; output += ocurrent; }
    return output;
  }
}
_____________________________
import java.util.ArrayList;

public class Boolfuck {

  public static final char[] bits = { 1, 2, 4, 8, 16, 32, 64, 128 };

  public static String interpret (String code, String input) {
    int oc = 0, ic = 0, ii = 0, in = input.length (), tp = 0; char i = 0, o = 0;
    ArrayList<Boolean> tape = new ArrayList<Boolean> (256); tape.add (false);
    StringBuilder output = new StringBuilder ();
    for (int c = 0, e = code.length (); c < e; ++c) {
      switch (code.charAt (c)) {
        case '<': if (--tp<0) { tape.add (0, false); tp=0; } break;
        case '>': tape.add (++tp<0); break;
        case '+': tape.set (tp, !(tape.get (tp))); break; 
        case '[': if (!tape.get (tp)) { int b= 1; while (b!=0 && ++c<e)  { if (code.charAt (c)=='[') ++b; else if (code.charAt (c)==']') --b; } } break; 
        case ']': if ( tape.get (tp)) { int b=-1; while (b!=0 && --c>=0) { if (code.charAt (c)=='[') ++b; else if (code.charAt (c)==']') --b; } } break; 
        case ',': if (--ic<0) { i=ii<in ? input.charAt (ii++) : 0; ic=7; } tape.set (tp, (i&1)>0); i=(char)(i>>1); break;
        case ';': if (tape.get (tp)) o |= bits[oc]; if (++oc>7) { output.append (o); o=0; oc=0; } break; 
      }
    }
    if (oc > 0) output.append (o);
    return output.toString ();
  }
}
_____________________________
import java.util.ArrayList;
import java.util.Arrays;
import java.util.BitSet;
import java.util.List;
import java.util.stream.Collectors;
import java.math.BigInteger;
import java.nio.charset.Charset;
public class Boolfuck {
 private static final char NEXT = '>';
  private static final char PREV = '<';
  private static final char FLIP = '+';
  private static final char READ = ',';
  private static final char WRITE = ';';
  private static final char LOOP_START = '[';
  private static final char LOOP_END = ']';
  private static final int FORWARD_SEARCH = 1;
  private static final int BACKWARD_SEARCH = -1;

  public static String interpret(String code, String input) {
    List<Integer> bits = new ArrayList<>(Arrays.asList(0));
    StringBuilder result = new StringBuilder();
    input = getBits(input);

    int pointer = 0;
    int bitIndex = 0;
    for (int i = 0; i < code.length(); i++) {
      char cmd = code.charAt(i);
      if (cmd == NEXT) {
        pointer++;
        if (pointer >= bits.size()) {
          bits.add(0);
        }
      } else if (cmd == PREV) {
        pointer--;
        if (pointer < 0) {
          bits.add(0, 0);
          pointer++;
        }
      } else if (cmd == FLIP) {
        bits.set(pointer, bits.get(pointer) ^ 1);
      } else if (cmd == READ) {
        int n = 0;
        if (bitIndex < input.length()) {
          n = Integer.valueOf("" + input.charAt(bitIndex++));
        }
        bits.set(pointer, n);
      } else if (cmd == WRITE) {
        result.append(bits.get(pointer));
      } else if (cmd == LOOP_START && bits.get(pointer) == 0) {
        i = getIndex(code, i, FORWARD_SEARCH);
      } else if (cmd == LOOP_END && bits.get(pointer) == 1) {
        i = getIndex(code, i, BACKWARD_SEARCH);
      }
    }
    if (result.length() > 0) {
      while (result.length() % 8 != 0) {
        result.append(0);
      }
      String res = Arrays.stream(result.reverse().toString().split("(?<=\\G.{8})"))
          .map(s -> new Character((char) Integer.parseInt(s, 2)).toString())
          .collect(Collectors.joining());
      return new StringBuilder(res).reverse().toString();
    }
    return "";

  }

  private static String getBits(String input) {
    if (input.length() > 0) {
      input = Arrays.stream(input.split(""))
          .map(str -> new StringBuilder(Integer.toBinaryString(str.charAt(0))))
          .map(str -> {
            int len = str.length();
            for (int i = 0; i < 8 - len; i++) {
              str.insert(0, "0");
            }
            return str.reverse().toString();
          })
          .collect(Collectors.joining());
    }
    return input;
  }


  public static Integer getIndex(String command, int point, int vector) {
    int i = point + vector;
    for (int counter = 1; counter != 0; i = i + vector) {
      if (command.charAt(i) == LOOP_START)
        counter = counter + vector;
      else if (command.charAt(i) == LOOP_END)
        counter = counter - vector;
    }
    return i - vector;
  }
}

