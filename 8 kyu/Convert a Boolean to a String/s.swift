func booleanToString(_ b: Bool) -> String {
  return String(b)
}
_________________________________
func booleanToString(_ b: Bool) -> String {
  return "\(b)"
}
_________________________________
func booleanToString(_ b: Bool) -> String {
  return b.description
}
_________________________________
func booleanToString(_ b: Bool) -> String {
  return "\(String(b))"
}
_________________________________
func booleanToString(_ b: Bool) -> String {

    var string = ""
    
  if b == true {
    string = "true"
  } else if b == false {
    string = "false"
  }
  return string
}
_________________________________
func booleanToString(_ b: Bool) -> String {
  String(describing: b)
}
_________________________________
func booleanToString(_ b: Bool) -> String {
  let bool: String = ""
  if b == true {
    return "true"
  } else if b == false {
    return "false"
  }
  return "error"
}
_________________________________
func booleanToString(_ b: Bool) -> String {"\(String(b))"}
