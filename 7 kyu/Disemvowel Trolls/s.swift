func disemvowel(_ s: String) -> String {
  return s.replacingOccurrences(of: "[aeiou]", with: "", options: [.regularExpression, .caseInsensitive])
}
______________________________
func disemvowel(_ s: String) -> String {
  let vowels: [Character] = ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]
  
  return String(s.characters.filter { !vowels.contains($0) })
}
______________________________
func disemvowel(_ s: String) -> String {
   return s.replacingOccurrences(of: "[AEIOUaeiou]", with: "", options: .regularExpression)
}
______________________________
func disemvowel(_ s: String) -> String {
  var str = ""
  let vowels = ["a", "e", "i", "o", "u"]
  for i in s.characters {
    if !vowels.contains(String(i).lowercased()) {
      str += String(i)
     }
  }
  return str
}
______________________________
let vowels = Set("aeiouAEIOU")

func disemvowel(_ s: String) -> String {
    return s.filter { !vowels.contains($0) }
}
______________________________
func disemvowel(_ s: String) -> String {
    s.filter { !["a", "e", "i", "o", "u"].contains($0.lowercased())}
}
