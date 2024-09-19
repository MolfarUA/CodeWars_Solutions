fn last_digit(lst: &[u64]) -> u64 {
    let f = |x, y| std::cmp::min(x % y + y, x);
    lst.iter().rev().fold(1, |v, &n| f(n, 20).pow(f(v, 4) as u32)) % 10
}
_________
fn last_digit(lst: &[u64]) -> u64 {
    lst.into_iter()
       .rev()
       .fold(1u64, |p, &v| {
           let base = if v >= 20 { v % 20 + 20 } else { v };
           let exp = if p >= 4 { p % 4 + 4 } else { p };
           
           base.pow(exp as u32)
       }) % 10
}
____________
fn mod_off(num: i32, mod_num: i32) -> i32 {
    let tmp = (num - 2) % mod_num + 2;
    
    if num > tmp { return tmp; } else { return num; }
}

fn pow_mod(exp: i32, base: i32) -> i32 {
    (mod_off(base, 20) as f64).powi(mod_off(exp, 4)) as i32
}

fn last_digit(lst: &[u64]) -> u64 {
    lst.iter().map(|x| *x as i32).rev().fold(1, pow_mod) as u64 % 10
}
