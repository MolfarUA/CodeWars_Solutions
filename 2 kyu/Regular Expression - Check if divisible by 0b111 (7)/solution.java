public class BinaryRegexp {
  public static String multipleOf7() {
    return "^(0|(10((0|11)(1|00))*(10|(0|11)01)|11)(01*0(0|101|1(1|00)((0|11)(1|00))*(10|(0|11)01)))*1)+$";
  }
}

_______________________
public class BinaryRegexp {
    public static String multipleOf7() {
        return "^(0|1(00(10|11(001*0)*1)*0|01(001*0)*1(10|11(001*0)*1)*0|101*0(001*0)*1(10|11(001*0)*1)*0)*(11|01(001*0)*01|101*0(001*0)*01|00(10|11(001*0)*1)*11(001*0)*01|01(001*0)*1(10|11(001*0)*1)*11(001*0)*01|101*0(001*0)*1(10|11(001*0)*1)*11(001*0)*01))+$";
        /*
        R(0) = (0|1R(1))*
        R(1) = 0R(2)|1R(3)
        R(2) = 0R(4)|1R(5)
        R(3) = 1|0R(6)
        R(4) = 0R(1)|1R(2)
        R(5) = 0R(3)|1R(4)
        R(6) = 1*0R(5)

        Eliminate R(6) term
        R(0) = (0|1R(1))*
        R(1) = 0R(2)|1R(3)
        R(2) = 0R(4)|1R(5)
        R(3) = 1 | 01*0R(5)
        R(4) = 0R(1)|1R(2)
        R(5) = 0R(3)|1R(4)

        Eliminate R(3) term
        R(0) = (0|1R(1))*
        R(1) = 0R(2) | 101*0R(5) | 11
        R(2) = 0R(4) | 1R(5)
        R(4) = 0R(1) | 1R(2)
        R(5) = 1R(4) | 001*0R(5) | 01

        Solve R(5)'s recursion
        R(5) = 1R(4) | 001*0R(5) | 01
        R(5) = (001*0)*1R(4) | (001*0)*01

        Eliminate R(5) term
        R(0) = (0|1R(1))*
        R(1) = 0R(2) | 11 | 101*0(001*0)*01 | 101*0(001*0)*1R(4)
        R(2) = 0R(4) | 1(001*0)*01 | 1(001*0)*1R(4)
        R(4) = 0R(1) | 1R(2)

        Eliminate R(2) term
        R(0) = (0|1R(1))*
        R(1) = 11 | 01(001*0)*01 | 101*0(001*0)*01 | 00R(4) | 01(001*0)*1R(4) | 101*0(001*0)*1R(4)
        R(4) = 11(001*0)*01 | 0R(1) | 10R(4) | 11(001*0)*1R(4)

        Solve R(4)'s recursion
        R(4) = 11(001*0)*01 | 0R(1) | 10R(4) | 11(001*0)*1R(4)
        R(4) = (10|11(001*0)*1)*11(001*0)*01 | (10|11(001*0)*1)*0R(1)

        Eliminate R(4) term
        R(0) = (0|1R(1))*
        R(1) = 11 | 01(001*0)*01 | 101*0(001*0)*01 |
              00(10|11(001*0)*1)*11(001*0)*01 | 00(10|11(001*0)*1)*0R(1) |
              01(001*0)*1(10|11(001*0)*1)*11(001*0)*01 | 01(001*0)*1(10|11(001*0)*1)*0R(1) |
              101*0(001*0)*1(10|11(001*0)*1)*11(001*0)*01 | 101*0(001*0)*1(10|11(001*0)*1)*0R(1)

        Rearrange R(1)
        R(1) = 11 |
              01(001*0)*01 |
              101*0(001*0)*01 |
              00(10|11(001*0)*1)*11(001*0)*01 |
              01(001*0)*1(10|11(001*0)*1)*11(001*0)*01 |
              101*0(001*0)*1(10|11(001*0)*1)*11(001*0)*01 |
              00(10|11(001*0)*1)*0R(1) |
              01(001*0)*1(10|11(001*0)*1)*0R(1) |
              101*0(001*0)*1(10|11(001*0)*1)*0R(1)

        Solve R(1)'s recursion
        R(1) = (00(10|11(001*0)*1)*0|
                01(001*0)*1(10|11(001*0)*1)*0|
                101*0(001*0)*1(10|11(001*0)*1)*0)*
                  (11 |
                  01(001*0)*01 |
                  101*0(001*0)*01 |
                  00(10|11(001*0)*1)*11(001*0)*01 |
                  01(001*0)*1(10|11(001*0)*1)*11(001*0)*01 |
                  101*0(001*0)*1(10|11(001*0)*1)*11(001*0)*01)

        Eliminate R(1)
        R(0) = (0|
                1(00(10|11(001*0)*1)*0|
                        01(001*0)*1(10|11(001*0)*1)*0|
                        101*0(001*0)*1(10|11(001*0)*1)*0)*
                          (11 |
                          01(001*0)*01 |
                          101*0(001*0)*01 |
                          00(10|11(001*0)*1)*11(001*0)*01 |
                          01(001*0)*1(10|11(001*0)*1)*11(001*0)*01 |
                          101*0(001*0)*1(10|11(001*0)*1)*11(001*0)*01))*

        R(0) = (0|1(00(10|11(001*0)*1)*0|01(001*0)*1(10|11(001*0)*1)*0|101*0(001*0)*1(10|11(001*0)*1)*0)*(11|01(001*0)*01|101*0(001*0)*01|00(10|11(001*0)*1)*11(001*0)*01|01(001*0)*1(10|11(001*0)*1)*11(001*0)*01|101*0(001*0)*1(10|11(001*0)*1)*11(001*0)*01))*
         */
    }
}

___________________________
public class BinaryRegexp {
  public static String multipleOf7() {
    String P_3_6_5 = "01*0";
    String P_5_3_6_5 = "(0" + P_3_6_5 + ")*";
    String P_3_6_5_3_6_5 = P_3_6_5 + P_5_3_6_5;
    String P_5_1 = "1(1(01)*1" + P_5_3_6_5 + "1|10)*0";
    
    String P_2_5_4 = "(000|01)*(11|0)(10)*";
    String P_2_5_4_2 = "(" + P_2_5_4 + "(1|00))*";
    String P_1_2_5_4_1 = "(0" + P_2_5_4_2 + P_2_5_4 + "0)*";
    String P_1_3 = P_1_2_5_4_1 + "(0" + P_2_5_4_2 + "10|1)";


    return "^(1" + P_1_3 + "(" + P_3_6_5_3_6_5 + "(0|(11(01)*1)*0|" + P_5_1 + P_1_3 + "))*1|0)+$";
  }
}

_____________________________________
public class BinaryRegexp {
  public static String multipleOf7() {
    return "^((0|111|1((101*0|01|0011)(001*0|111)*01))|((1000)(00(10)*0|(101*0|01|00(10)*11)(001*0|1(10)*11)*1(10)*0)*(11|((101*0|01|00(10)*11)(001*0|1(10)*11)*01)))|((1001)((0|11)(1|00)|(10|(0|11)01)(01*00|01*0101)*01*01(1|00))*((10|(0|11)01)(01*00|01*0101)*1))|((1010)(01*00|01*0101|01*01(1|00)((0|11)(1|00))*(10|(0|11)01))*1)|((1011)((1|00)(0|11)|((1|00)10|01)(01*00)*01*01)*(((1|00)10|01)(01*00)*1))|((1100)(001*0|1(10)*11|1(10)*0(00(10)*0)*(101*0|01|00(10)*11))*(01|(1(10)*0)(00(10)*0)*11))|((1101)((0(1(10)*11)*1(10)*0((01|0011)(1(10)*11)*1(10)*0|(00(10)*0))*(10|(01|0011)(1(10)*11)*00))|1|0(1(10)*11)*00)*(0(1(10)*11)*01|0(1(10)*11)*1(10)*0((01|0011)(1(10)*11)*1(10)*0|(00(10)*0))*(11|(01|0011)01))))+$";
  }
}

_________________________
public class BinaryRegexp {
  public static String multipleOf7() {
      StringBuilder result = new StringBuilder();
      //S0-S6 is finite-states of DFA
      String fromS0toS4 = "100(10|000)*";
      String fromS0toS5 = "101";
      String fromS0toS6 = "110";
      String fromS4ToS5 = "(11|001)";
      String fromS4ToS6 = "010";
      String fromS4ToEnd = "011";
      String fromS0ToS5ThroughS4 = fromS0toS4 + fromS4ToS5;
      String loopS5ThroughS4 = "(1(10|000)*(11|001))*";
      String fromS5ToS6 ="00";
      String fromS5ToEnd = "(01|1(10|000)*011)";
      String fromS5ToEndThroughS4 = "1(10|000)*010";
      result.append("^(?!$|0.)");
      result.append("(");
      result.append("0");
      result.append("|111");
      result.append("|(" + fromS0toS5 + "|" + fromS0ToS5ThroughS4 +")");
      result.append(loopS5ThroughS4 + fromS5ToEnd);
      result.append("|" + fromS0toS4 + fromS4ToEnd);
      result.append("|(" + fromS0toS6);
      result.append("|" + fromS0toS4 + fromS4ToS6);
      result.append("|(" + fromS0toS5 + "|" + fromS0ToS5ThroughS4 +")" + loopS5ThroughS4);
      result.append("(" + fromS5ToEndThroughS4 + "|" + fromS5ToS6 + "))");
      result.append("(1|0" + loopS5ThroughS4);
      result.append("(" + fromS5ToS6 + "|" + fromS5ToEndThroughS4 + "))*");
      result.append("0" + loopS5ThroughS4);
      result.append(fromS5ToEnd);
      result.append(")*");
      return result.toString();
  }
}

_________________________________
public class BinaryRegexp {
  public static String multipleOf7() {
    return "^(0|1(1(01*00)*01*010|(0|1(01*00)*01*011)(01|111|10(01*00)*01*011)*00|(0|1(01*00)*01*011)(01|111|10(01*00)*01*011)*110|(0|1(01*00)*01*011)(01|111|10(01*00)*01*011)*10(01*00)*01*010)*1(01*00)*1|1(1(01*00)*01*010|(0|1(01*00)*01*011)(01|111|10(01*00)*01*011)*00|(0|1(01*00)*01*011)(01|111|10(01*00)*01*011)*110|(0|1(01*00)*01*011)(01|111|10(01*00)*01*011)*10(01*00)*01*010)*(0|1(01*00)*01*011)(01|111|10(01*00)*01*011)*10(01*00)*1)+$";
  }
}

_____________________________
import java.util.stream.IntStream;
public class BinaryRegexp {
  public static String multipleOf7() {
    //Method:

    //Create a finite state machine for the problem
    //  Seven nodes, each representing n%7, with each node pointing to two other nodes (or itself) for
    //  if a 0 or a 1 is added to the end of the binary string
    
    //From that state machine, generate a tree
    //  Starting at node 0, write out possible paths with left being a 0 and right being a 1
    //  If a remainder is a ancestor of itself, leave it as a leaf
    //  This left me with 27 nodes and 14 leaves.
      
    //For each node in the binary tree, if a node has an ancestor with the same remainder, label it
    
    //Assign a variable for each, where that variable defines all of the ways to the ancestors with
    //the same remainder. If another labelled node is in the path, include it, as seen below.

    String i = String.format("(1)*");
    String h = String.format("(10)*");
    String g = String.format("(1%s11)*", h);
    String f = String.format("(00%s0)*", i);
    String e = String.format("(1)*");
    String d = String.format("((01)|(1%s11))*", f);
    String c = String.format("(0%s0%s0)*", e, g);
    String b = String.format("((1%s0%s0%s1%s0)|(0%s((1%s10)|(00))))*", c, e, g, h, d, f);
    String a = String.format("^(0|(1%s((1%s1)|(0%s1%s01))))+$", b, c, d, f);
    
    //Once done, the 0 node, labelled a here, will build to the entire regex.
    //^(0|(1((1(0(1)*0(1(10)*11)*0)*0(1)*0(1(10)*11)*1(10)*0)|(0((01)|(1(00(1)*0)*11))*((1(00(1)*0)*10)|(00))))*((1(0(1)*0(1(10)*11)*0)*1)|(0((01)|(1(00(1)*0)*11))*1(00(1)*0)*01))))+$
    
    return a;
  }
}
