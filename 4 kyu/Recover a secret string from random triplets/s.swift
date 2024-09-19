53f40dff5f9d31b813000774


func recoverSecret(from triplets: [[String]]) -> String {
    var prev = [String]()
    var secret = Array(Set(triplets.flatMap{ $0 }))
    
    while !prev.elementsEqual(secret) {
        let duplicateSecret = secret
        prev = duplicateSecret
        
        for triplet in triplets {
            let charTuples = [
                ( triplet[0], triplet[1] ),
                ( triplet[1], triplet[2] )
            ]
            
            for tuple in charTuples {
                let aIndex = secret.firstIndex(of: tuple.0)!
                let bIndex = secret.firstIndex(of: tuple.1)!
                
                if (aIndex > bIndex) {
                    secret.insert(tuple.0, at: bIndex)
                    secret.remove(at: aIndex + 1)
                }
            }
        }
    }
    
    return secret.joined()
}

##############################
func recoverSecret(from triplets: [[String]]) -> String {
    var secret = Array(Set(triplets.joined()))
    (triplets + triplets).forEach {
        zip($0.dropLast(), $0.dropFirst()).forEach {
            if let firstIndex = secret.firstIndex(of: $0.0), let secondIndex = secret.firstIndex(of: $0.1),
               firstIndex > secondIndex {
                    let element = secret.remove(at: firstIndex)
                    secret.insert(element, at: secondIndex)
            }
        }
    }
    return secret.joined()
}

#############################
func recoverSecret(from triplets: [[String]]) -> String {
  
  // get the set of all characters to get an anagram of the secret
  var set = Set(triplets.joined())
  
  var triplets: [[String]] = triplets
  var r = ""
  
  // search for the only character that only appears in the first position in any triplet, then remove it from the set... repeat
  for _ in 0..<set.count {
    let n = set.first{ c -> Bool in
      let firstOrNotFound: [Bool] = triplets.flatMap{ ($0.firstIndex(of: c) ?? 0) == 0 }
      return firstOrNotFound.reduce(true, {$0 && $1})
    } ?? ""
    r += n
    triplets = triplets.map { $0.filter{$0 != n} }
    set.remove(n)
  }
  
  return r
}
