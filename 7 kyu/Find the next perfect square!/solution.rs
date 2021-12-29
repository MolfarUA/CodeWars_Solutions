fn find_next_square(sq: u64) -> Option<u64> {
    let root = (sq as f64).sqrt();
    if root != root.floor() {
        return None
    }
    Some((root as u64 + 1).pow(2))
}
  
_____________________________________
fn find_next_square(sq: u64) -> Option<u64> {
    let num = (sq as f64).sqrt();
    if num.fract() > 0f64 {
        return Option::None
    }
    let ret = (num as u64) + 1;
    return Option::Some(ret.pow(2))
}
  
_____________________________________
fn find_next_square(sq: u64) -> Option<u64> {
    let dsquare = ((sq as f64).sqrt() + 1.0).powi(2);
    match dsquare.fract() {
        0.0 => Some(dsquare as u64),
        _ => None
    }
}
  
_____________________________________
fn find_next_square(sq: u64) -> Option<u64> {
    let n = (sq as f64).sqrt();
    
    (n.fract() == 0.0).then(|| (n as u64 + 1).pow(2))
}
  
_____________________________________
fn find_next_square(sq: u64) -> Option<u64> {
    if (sq as f64).sqrt() == (sq as f64).sqrt().round(){
        Some((((sq as f64).sqrt() + 1.) as u64).pow(2))
    }else{
        None
    }
}
  
_____________________________________
fn find_next_square(n: u64) -> Option<u64> {
    perfect_sqrt(n).map(|x| (x + 1) * (x + 1))
}

fn perfect_sqrt(n: u64) -> Option<u64> {
    match n & 0xf {
        0 | 1 | 4 | 9 => {
            let s = (n as f64).sqrt() as u64;
            if s * s == n {
                Some(s)
            } else {
                None
            }
        }
        _ => None,
    }
}
