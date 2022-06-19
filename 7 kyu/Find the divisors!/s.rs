544aed4c4a30184e960010f4


fn divisors(integer: u32) -> Result<Vec<u32>, String> {
    let divs = (2..integer)
        .filter(|k| integer % k == 0)
      .collect::<Vec<u32>>();
      
  if divs.len() > 0 {
    Ok(divs)
  } else {
    Err(format!("{} is prime", integer))
  }
}
__________________________________
fn divisors(integer: u32) -> Result<Vec<u32>, String> {
  let divisors: Vec<u32> = (2..integer / 2 + 1).filter(|x| integer % x == 0).collect();
  match !divisors.is_empty() {
    true => Ok(divisors),
    _ => Err(format!("{} is prime", integer))
  }
}
__________________________________
fn divisors(integer: u32) -> Result<Vec<u32>, String> {
    let divs: Vec<u32> = (2..integer)
        .filter(|k| integer % k == 0)
        .collect();
      
    if divs.is_empty() { return Err(format!("{} is prime", integer)); }
    
    Ok(divs)
}
__________________________________
fn divisors(integer: u32) -> Result<Vec<u32>, String> {
    let arr: Vec<u32> = (2..=integer/2).filter(|x| integer % x == 0).collect();
    match arr.is_empty() {
        true => Err(format!("{} is prime", integer)),
        false => Ok(arr)}
}
__________________________________
fn divisors(integer: u32) -> Result<Vec<u32>, String> {
      let result: Vec<u32> = (2..integer).filter(|x| integer % x == 0).collect();
    if result.len() > 0 { Ok(result) } else { Err(format!("{} is prime", integer)) }
}
