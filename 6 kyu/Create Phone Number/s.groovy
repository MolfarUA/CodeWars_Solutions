class Kata {
  static String createPhoneNumber(digits) {
    String.format("(%d%d%d) %d%d%d-%d%d%d%d", *digits)
  }
}
_______________________________
class Kata {
  static String createPhoneNumber(numbers){
    "(${numbers[0..2].join()}) ${numbers[3..5].join()}-${numbers[6..9].join()}"
  }
}
_______________________________
class Kata {
  static String createPhoneNumber(n) {
    return String.format("(%d%d%d) %d%d%d-%d%d%d%d", n[0], n[1], n[2], n[3], n[4], n[5], n[6], n[7], n[8], n[9])
  }
}
_______________________________
class Kata {
  static String createPhoneNumber(numbers){
    return "(${numbers[0..2].join()}) ${numbers[3..5].join()}-${numbers[6..-1].join()}"
  }
}
