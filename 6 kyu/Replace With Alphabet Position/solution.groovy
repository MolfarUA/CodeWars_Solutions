class Kata {
    static def alphabetPosition(text) {
        text.findAll(/(?i)[a-z]/){ (int)it.toLowerCase() - (int)'a' + 1 }.join(" ")
    }
}

_______________________________________________
class Kata {
    static def alphabetPosition(text) {
        text.toLowerCase()
            .findAll { c -> c >= 'a' && c <= 'z' }
            .collect { c -> ((int) c - 96).toString() }
            .join(" ")
    }
}

_______________________________________________
class Kata {
    static def alphabetPosition(text) {
        text.toLowerCase().collect{ (int)it - 96 }.findAll { it > 0 && it < 27 }.join(" ")
    }
}

_______________________________________________
class Kata {
    static def alphabetPosition(text) {
      List result = []
      String a = "abcdefghijklmnopqrstuvwxyz"
      
      text.replaceAll("[^a-zA-Z ]+|\\s","").each{ c -> 
        println(c.toLowerCase())
        result.add(a.indexOf(c.toLowerCase()) + 1)
    }
      return result.join(" ")
    }
}

// 10 10 15 22 11 7 17 3 10 11 15 17 21 5 7 13 23 17 26 3 2 15 8 8 17 10 26 1 19 17 7 15 13 11 7 15 18 25 10
// 10 0 10 0 15 22 11 7 17 3 10 11 15 17 21 5 7 13 23 17 26 3 2 15 8 8 17 10 26 1 19 0 17 7 15 13 11 7 15 0 18 0 25 10

_______________________________________________
class Kata {
    static def alphabetPosition(text) {
      def alphabet = "abcdefghijklmnopqrstuvwxyz"
      def output = ""
        for (int i = 0; i < text.length(); i++)
        {
           if(alphabet.contains(text[i].toString().toLowerCase()))
           {
              def alphabetPos = alphabet.indexOf(text[i].toString().toLowerCase()) + 1
              output += alphabetPos + " "
           }
        }
      output = output.trim()
      return output
    }
}

_______________________________________________
class Kata {

    static def alphabetPosition(text) {

        def characterNumberMap = [:]
        int x = 0

        for (i in 'a'..'z') {
            characterNumberMap.put(i,++x)
        }

        text = text.toLowerCase()
        String numberString = ""

        for (i in text) {
            if (characterNumberMap[i]) {
                numberString += characterNumberMap[i] + " "
            }
        }
        numberString = numberString.trim()

        return numberString
    }
}
