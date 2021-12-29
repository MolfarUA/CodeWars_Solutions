public class Bio{
    public String dnaToRna(String dna){
        return dna.replace("T", "U");
    } 
}

_____________________________
import java.io.*;

public class Bio {
    public String dnaToRna(String dna){
        return dna.replaceAll("T", "U");
    } 
}

_____________________________
public class Bio {
    public String dnaToRna(String dna) {

    String rna = "";
       
     // For every letter in String called DNA
     for(int i = 0; i < dna.length(); i++) {
     
     // get the letter at index i
      char letter = dna.charAt(i);
     
      // if letter != T,
      //    add letter to rna
      // else 
       //   add U 
       if(letter != 'T') {
         rna += letter;
       } else {
         rna += 'U';     
     }
     
     }
     

       return rna;  // Do your magic!
    }
}

_____________________________
class Bio {
  static String dnaToRna(String dna) {
    return dna.replace("T", "U");
  }
}

_____________________________
public class Bio {
    public String dnaToRna(String dna) {
        String result = dna;
        return result.replace('T','U');
    } 
}
