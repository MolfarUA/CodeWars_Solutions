class Solution {
  static func twosum(numbers: [Double], target: Double) -> [Int] {
    for i in 0..<(numbers.count-1) {
      for j in (i+1)..<numbers.count {
        if numbers[i] + numbers[j] == target {
          return [i,j]
        }
      }
    }
    return [];
  }
}
________________________________
class Solution {
  static func twosum(numbers: [Double], target: Double) -> [Int] {
    var numberPairs = [Double: Double]()
    for (index,number) in numbers.enumerated() {
        if let pairIndex = numberPairs[target - number] {
            return[Int(pairIndex),index]
        } else {
            numberPairs[Double(number)] = Double(index)
        }
    }
    return []
  }
}
________________________________

class Solution {
  static func twosum(numbers: [Double], target: Double) -> [Int] {
   guard numbers.count != 0 else { return [] }
   
    for i in 0..<numbers.count {
        for j in 0..<numbers.count - 1 {
            if numbers[i] + numbers[j + 1] == target{
                return [i, j + 1]
            }
        }
    }
    return []
    }
}
________________________________
class Solution {
  static func twosum(numbers: [Double], target: Double) -> [Int] {

      for index in 0..<numbers.count{
          for jindex in 0..<numbers.count{
              if numbers[index]+numbers[jindex] == target && index != jindex{
                  return [index,jindex]
              }
          }
      }
      return [Int]()
  }
}
________________________________
class Solution {
  static func twosum(numbers: [Int], target: Int) -> [Int] {
    var dict = [Int: Int]()
    for i in 0..<numbers.count {
      let value = numbers[i]
      let remainder = target - value
      if let j = dict[remainder] {
        return [j, i]
      }
      dict[value] = i
    }
    return []
  }
}
