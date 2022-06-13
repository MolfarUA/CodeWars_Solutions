func potatoes (_ p0: Int, _ w0: Int, _ p1: Int) -> Int {
    return w0 * (100 - p0) / (100 - p1)
}
_______________________________________________
func potatoes (_ p0: Int, _ w0: Int, _ p1: Int) -> Int {
  w0 * (100 - p0) / (100 - p1) 
}
_______________________________________________
func potatoes (_ p0: Int, _ w0: Int, _ p1: Int) -> Int {
   let dryMatter = w0 * (100 - p0)
    
    return dryMatter / (100 - p1)
}
_______________________________________________
func potatoes (_ p0: Int, _ w0: Int, _ p1: Int) -> Int {
  let dryPersent = Double(100 - p0)
  print("dryPersent: ", dryPersent)
  let dryWeight: Double = Double(w0) / 100 * dryPersent
  let newDryPersent = 100 - p1
  let newWeight: Double = Double(100 / Double(newDryPersent) * dryWeight)
  return Int(newWeight)
}
