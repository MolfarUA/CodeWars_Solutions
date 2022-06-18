544675c6f971f7399a000e79


class Kata {
    static int stringToNumber(String s) {
        return s as Integer
    }
}
_______________________
class Kata {
    static int stringToNumber(String s) {
        return s.toInteger()
    }
}
_______________________
class Kata {
    static int stringToNumber(String s) {
      s as int
    }
}
_______________________
class Kata {
    static stringToNumber = Integer.&parseInt
}
_______________________
class Kata {
    static int stringToNumber(String s) {
        s.isInteger() ? s.toInteger() : null
    }
}
