func persistence(for num: Int) -> Int {
  let digits: [Int] = String(num).characters.flatMap { Int(String($0)) }
  
  return digits.count == 1 ? 0 : 1 + persistence(for: digits.reduce(1, *))
}
________________________________________
func persistence(for num: Int) -> Int {
    var numbers = num.digitArray
    var count = 0
    while numbers.count > 1 {
        count += 1
        numbers = numbers.reduce(1, *).digitArray
    }

    return count
}

extension Int {
    var digitArray: [Int] {
        return description.characters.map{Int(String($0)) ?? 0}
    }
}
________________________________________
func persistence(for num: Int) -> Int {
   guard num >= 10 else { return 0 }
   
   let digits = String(num).characters.map { Int(String($0))! }
   let product = digits.reduce(1, *)
   
   return persistence(for: product) + 1
}
________________________________________
func persistence(for num: Int) -> Int {
    return num < 10 ? 0 : 1 + persistence( for: String(num).characters.reduce( 1, {$0 * Int(String($1))!} ) )
}
________________________________________
func persistence(for num: Int) -> Int {
  guard num > 9 else {return 0}
  return 1 + persistence(for: String(num).compactMap{$0.wholeNumberValue}.reduce(1, *))
}
________________________________________
func persistence(for num: Int) -> Int {
    return persistence(for: num, count: 0)
}

func persistence(for num: Int, count: Int) -> Int {
    let digits = String(num).characters
    if digits.count == 1 {
        return count
    }
    return persistence(for: multiplied(digits), count: count + 1)
    
}

func multiplied(_ characters: String.CharacterView) -> Int {
    return characters.reduce(1, { (result, nextCharacter) in
        let nextNumber = Int(String(nextCharacter))!
        return result * nextNumber })
}
