public class BinaryRegexp {
  public static string MultipleOf7() {
    // Write a *string* which represents a regular expression to detect whether a binary number is divisible by 7
    return "^(0|(10((0|11)(1|00))*(10|(0|11)01)|11)(01*0(0|101|1(1|00)((0|11)(1|00))*(10|(0|11)01)))*1)+$";
  }
}

______________________________
public class BinaryRegexp {
  public static string MultipleOf7() 
  {
    string A = @"(0(01)*00)";
    string B = @"(101*0|0(01)*1)";
    string C = @"(11(01)*00|10)";
    return $"^(0|1{A}*11|(1{A}*{B}(001*0|11(01)*1|{C}{A}*(101*0|0(01)*1))*(01|{C}{A}*11)))+$";
  }
}

_________________________________
public class BinaryRegexp
    {
        public static string MultipleOf7()
        {
            var ss = "^("
                     + "0+|"  //state 0 -> state 0 
                     + "1"    //state 0 -> state 1
                     + "("
                       + "0((01)*|(111)*)*(00|11(10)*0)" 
                     + ")*"   //state 1 -> state 1
                     + "("
                       + "1|"
                       + "0((01)*|(111)*)*10"
                     + ")"    //state 1 -> state 3 
                     + "("  
                     + "01*0"  //state 3 -> state 5
                       + "("
                         + "("
                           + "1((10)*|(000)*)*(001|11)"
                         + ")*" //state 5 -> state 5
                         + "0|" //state 5 -> state 3
                         + "("
                           + "1((10)*|(111)*)*0"
                         + ")"  //state 5 -> state 1
                         + "("
                           + "0((01)*|(111)*)*(00|11(10)*0)"
                         + ")*" //state 1 -> state 1
                         + "1"  //state 1 -> state 3
                       + ")"
                     + ")*" //state 3 -> state 3
                     + "1"  //state 3 -> state 0
                   + ")+$";

            return ss;
        }
    }
    
___________________________________________________
public class BinaryRegexp {
  public static string MultipleOf7() {
    string q1q4 = "1(01*00)*01*01|0((0|11)|10(01*00)*01*01)";
    string q4q4 = "1((0|11)|10(01*00)*01*01)";
    string q4q0 = "110(01*00)*1";
    string q1q1 = $"({q1q4})({q4q4})*0";
    string q1q0a = "1(01*00)*1|010(01*00)*1";
    string q1q0b = $"({q1q4})({q4q4})*({q4q0})";
    string q1q0 = $"({q1q1})*(({q1q0a})|({q1q0b}))";
    string q0q0 = $"0|1({q1q0})";
    return $"^(0|1({q1q0}))({q0q0})*$";
  }
}

_____________________________________________
public class BinaryRegexp
{
  public static string MultipleOf7()
  {
    return "^0*(?=0$|1)((0|111|100((1|00)0)*011|(101|100((1|00)0)*(1|00)1)(1((1|00)0)*(1|00)1)*(01|1((1|00)0)*011)|(110|100((1|00)0)*010|(101|100((1|00)0)*(1|00)1)(1((1|00)0)*(1|00)1)*(00|1((1|00)0)*010))(1|0(1((1|00)0)*(1|00)1)*(00|1((1|00)0)*010))*0(1((1|00)0)*(1|00)1)*(01|1((1|00)0)*011))*)$";
  }
}

____________________________
using System.Text.RegularExpressions;
public class BinaryRegexp {
  public static string MultipleOf7() 
  {
    return "^(0|111|100((1|00)0)*011|(101|100((1|00)0)*(1|00)1)(1((1|00)0)*(1|00)1)*(01|1((1|00)0)*011)|(110|100((1|00)0)*010|(101|100((1|00)0)*(1|00)1)(1((1|00)0)*(1|00)1)*(00|1((1|00)0)*010))(1|0(1((1|00)0)*(1|00)1)*(00|1((1|00)0)*010))*0(1((1|00)0)*(1|00)1)*(01|1((1|00)0)*011))+$";
  }
}

_______________________________
public class BinaryRegexp {
  public static string MultipleOf7() {
    // Write a *string* which represents a regular expression to detect whether a binary number is divisible by 7
    return "(^0+$)|(^0*(0*1(0(01)*(11(10)*1)*((0(10)*0)|(11(10)*0)))*((1)|(0(01)*(11(10)*1)*10))(01*0(((1(10)*((1)|(00))(01)*1)*0)|(((1(10)*11)|(1(10)*(00(01)*0)*00(01)*1))*1(10)*(00(01)*0)*01)))*1)+0*$)";
  }
}

____________________________________
public class BinaryRegexp {
  public static string MultipleOf7() {
    // Write a *string* which represents a regular expression to detect whether a binary number is divisible by 7
    return "^(0|(1((0(01)*1|101*0)(001*0|11(01)*1)*(10|11(01)*00)|0(01)*00)*((0(01)*1|101*0)(001*0|11(01)*1)*01|11)0*)+)$";
  }
}

____________________________
using System.Text.RegularExpressions;
public class BinaryRegexp {
  
  public static string MultipleOf7() {
    return "^((0)|(1((1(01*00)*01*010)|(((0)|(1(01*00)*01*011))((01)|(111)|(10(01*00)*01*011))*((00)|(110)|(10(01*00)*01*010))))*((1(01*00)*1)|(((0)|(1(01*00)*01*011))((01)|(111)|(10(01*00)*01*011))*10(01*00)*1))))+$";
  }
}
