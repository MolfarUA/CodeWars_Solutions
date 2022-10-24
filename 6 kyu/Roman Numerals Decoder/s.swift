51b6249c4612257ac0000005

import Foundation

func value(of numeral: Character) -> Int? {
    switch numeral {
    case "I": return 1
    case "V": return 5
    case "X": return 10
    case "L": return 50
    case "C": return 100
    case "D": return 500
    case "M": return 1000
    default: return nil
    }
}

func solution(_ number: String) -> Int {

    let numbers = number.compactMap { value(of: $0) }
    let sum = numbers.reduce(0, +)

    let difference = zip(numbers, numbers.dropFirst())
        .filter { $0 < $1 }
        .map { $0.0 }
        .reduce(0, +)

    return sum - difference * 2
}
__________________________________
import Foundation

func solution(_ string:String) -> Int {
  let dict: [Character: Int] = [
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1_000
  ]
  
  var result = 0
  var lastReadValue = 0
  for letter in string.reversed() {
    guard let value = dict[letter] else { continue }
    if lastReadValue > value {
      result -= value
    } else {
      result += value
    }
    lastReadValue = value
  }
  return result
}
