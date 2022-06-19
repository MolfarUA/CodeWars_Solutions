515de9ae9dcfc28eb6000001


class Kata {
    static List<String> solution(String str) {
        (str + '_').findAll(/../)
    }
}
________________________________
class Kata {
    static List<String> solution(String str) {
      if (str.isEmpty()) {return []}
      List<String> pairs = str.split("(?<=\\G.{2})")
      if (pairs.last().size() == 1) {
        pairs[pairs.size()-1] = pairs.last() + "_"
      }
      return pairs
    }
}
________________________________
class Kata {
    static List<String> solution(String randomstring) {
    def list = []
    def i=0
    randomstring = (randomstring.length() % 2 ) == 0 ? randomstring : randomstring + "_"
    while (i<randomstring.length()){
        list.add(randomstring[i] + randomstring[i+1])
        i += 2
    }
    return list
    }
}
________________________________
class Kata {
    static List<String> solution(String str) {
      List<String> arr = new ArrayList<>();
      for(int i = 0; i < str.length(); i += 2){
        if(i + 1 >= str.length()){
          arr.add(str[i] +'_');
          break;
        }
        arr.add(str[i..i+1]);
      }
      arr;
    }
}
________________________________
class Kata {
    static List<String> solution(String str) {
      def size = str.size()
      def res = []
      for (def i = 0; i < size - 1; i += 2){
        res << str.substring(i,i+2)
      }
      if(size % 2 != 0){
        res << "${str[size-1]}_"
      }
      res
    }
}
