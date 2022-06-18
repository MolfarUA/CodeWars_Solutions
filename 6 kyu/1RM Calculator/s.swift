595bbea8a930ac0b91000130

import Foundation

func calculate1RM(_ weight: Int,_ reps: Int) -> Int? {
  if reps == 0 {
    return nil
  }
  
  let w: Double = Double(weight)
  let r: Double = Double(reps)
  
  let a = w * (1 + (r / 30))
  let b = (100 * w) / (101.3 - 2.67123 * r)
  let c = w * pow(r, 0.1)
  
  return Int(round([a,b,c].sorted().last ?? 0))
}
_______________________________
import Foundation
func calculate1RM(_ weight: Int, _ reps: Int) -> Int? {
  guard reps > 0 else { return nil }
  guard reps > 1 else { return weight }
  return Int([
    Double(weight) * (1.0 + Double(reps) / 30.0),
    Double(100*weight) / (101.3 - 2.67123 * Double(reps)),
    Double(weight) * pow(Double(reps), 0.10)
  ].max()!.rounded())
}
_______________________________
func calculate1RM(_ weight: Int, _ reps: Int) -> Int? {
  if reps==0 { return nil }
  if reps==1 { return weight }
  let w = Double(weight)
  let r = Double(reps)
  let e = w*(1+r/30.0)
  let m = 100*w/(101.3-2.67123*r)
  let l = w*pow(r, 0.10)
  return Int(round(max(max(e, m), l)))
}
_______________________________
func calculate1RM(_ weight: Int, _ reps: Int) -> Int? {
  guard reps > 0 else {
    return nil
  }
  
  if reps == 1 {
    return weight
  }
  
  let epley = Double(Double(weight) * (1 + (Double(Double(reps) / 30))))
  
  let mcGlothin = (100 * Double(weight)) / abs((101.3 - (2.67123 * Double(reps))))
  
  let lombardi = Double(weight) * pow(Double(reps), 0.1)
  
 let roudedEpley = epley.rounded()
  let roundedMcGlothin = mcGlothin.rounded()
  let roundedLombardi = lombardi.rounded()
  
  return [Int(roudedEpley), Int(roundedMcGlothin), Int(roundedLombardi)].max()
}
_______________________________
func calculate1RM(_ wi: Int, _ ri: Int) -> Int? {
  guard ri > 0 else { return nil }
  guard ri > 1 else { return wi }
  
  let w = Double(wi)
  let r = Double(ri)
  
  let e = w * (1 + r / 30)
  let m = 100 * w / (101.3 - 2.673123 * r)
  let l = w * pow(r, 0.1)
  
  return Int(max(e, max(m, l)).rounded())
}
_______________________________
func calculate1RM(_ weight: Int, _ reps: Int) -> Int? {
  guard reps > 0 else {
    return nil
  }
  
  if reps == 1 {
    return weight
  }
  
  let epley = Double(Double(weight) * (1 + (Double(Double(reps) / 30))))
  
  let mcGlothin = (100 * Double(weight)) / abs((101.3 - (2.67123 * Double(reps))))
  
  let lombardi = Double(weight) * pow(Double(reps), 0.1)
  
 let roudedEpley = epley.rounded()
  let roundedMcGlothin = mcGlothin.rounded()
  let roundedLombardi = lombardi.rounded()
  
  return [Int(roudedEpley), Int(roundedMcGlothin), Int(roundedLombardi)].max()
}
