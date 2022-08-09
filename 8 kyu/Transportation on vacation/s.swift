568d0dd208ee69389d000016


func RentalCarCost(_ days: Int) -> Int {
  let cost = days * 40
  var discount = days >= 7 ? 50 : 20
  return days >= 3 ? cost - discount : cost
}
__________________________
func RentalCarCost(_ days: Int) -> Int {

        let rentCostPerDay = 40
        var total = days * rentCostPerDay
        
        if days >= 7 {
            total -= 50
        } else if days >= 3 {
            total -= 20
        }
        
        return total
}
__________________________
func RentalCarCost(_ days: Int) -> Int {
  return days * 40 - (days >= 3 ? ( days >= 7 ? 50 : 20 ) : 0)
}
