fn is_prime(x: i64) -> bool {
    let last = (x as f64).sqrt() as i64 + 1;
    x > 1 && (2..last).all(|d| x % d != 0)
}
_______________
// 6k+-1 optimization
fn is_prime(n: i64) -> bool {
    if n <= 3 {
        return n > 1;
    }
    if n % 2 == 0 || n % 3 == 0 {
        return false;
    }
    let mut i: i64 = 5;
    while i.pow(2) <= n {
        if n % i == 0 || n % (i + 2) == 0 {
            return false;
        }
        i += 6;
    }
    return true;
}
_____________________
fn is_prime(x: i64) -> bool {
    x > 1 && !(2..=(x as f32).sqrt() as i64).any(|i| x%i==0)
}
