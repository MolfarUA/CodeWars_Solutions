fn xo(string: &'static str) -> bool {
  string.chars().fold(0, |a, c|{
    match c {
      'x' | 'X' => a + 1,
      'o' | 'O' => a - 1,
      _ => a
    }
  }) == 0
}
__________________________________
fn xo(s: &str) -> bool {
    let s2 = s.to_lowercase();
    s2.matches("x").count() == s2.matches("o").count()
}
__________________________________
fn xo(string: &str) -> bool {
    string.chars().filter(|&c| c == 'X' || c == 'x').count() == string.chars().filter(|&c| c == 'O' || c == 'o').count()
}
__________________________________
fn xo(string: &'static str) -> bool {
  string.chars().fold(0, |acc, ch| match ch {
    'x' | 'X' => acc + 1,
    'o' | 'O' => acc - 1,
    _ => acc
  }) == 0
}
__________________________________
fn xo(string: &'static str) -> bool {
  string.to_lowercase().matches("x").count() == string.to_lowercase().matches("o").count()
}
__________________________________
fn xo(string: &'static str) -> bool {
    let mut xs:u32 = 0;
    let mut os:u32 = 0;
    for c in string.chars() {
        match c {
            'x' | 'X' => xs += 1,
            'o' | 'O' => os += 1,
            _ => ()
        }
    }
    xs == os
}
__________________________________
fn xo(string: &'static str) -> bool {
  let difference: i32 = string.chars()
    .map(|c| match c {
      'X' | 'x' => 1,
      'O' | 'o' => -1,
      _ => 0
    }).sum();
  
  difference == 0
}
