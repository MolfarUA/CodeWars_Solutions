func countDuplicates(_ s:String) -> Int {
    var counts: [String: Int] = [:]
    for character in Array(s) {
        counts[character.lowercased(), default: 0] += 1
    }
    return counts.values.filter{ $0 > 1 }.count
}
____________________
func countDuplicates(_ s:String) -> Int {
  return s.lowercased().reduce(into: [:]) { $0[$1, default: 0] += 1 }.filter { $0.1 > 1 }.count
}
__________________
func countDuplicates(_ s:String) -> Int {
    // Make lowercased sorted string
    var duplicates = s.lowercased().sorted()
    
    // Value to hold char from last iteration
    var lastChar: Character?
    
    // Array of the repeated numbers of characters
    var repeatedChars = [Character]()
    
    // Parse through the string to find duplicates
    for character in duplicates {
        // Can't do this first time around
        if lastChar != nil {
            // Okay to use bang operator, tested for nil value
            if lastChar! == character && !repeatedChars.contains(character) {
                repeatedChars.append(character)
            }
        }

        lastChar = character
    }
    
    return repeatedChars.count
}
_________________________
func countDuplicates(_ s:String) -> Int {
  var counter = 0
    let chars = Array(s).map({ $0.lowercased() })
    Dictionary(grouping: chars, by: { $0 }).forEach({ if $0.value.count > 1 { counter += 1 } })
    return counter
}
