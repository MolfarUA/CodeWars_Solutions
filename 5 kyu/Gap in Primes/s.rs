561e9c843a2ef5a40c0000a4


fn gap(g: i32, m: u64, n: u64) -> Option<(u64, u64)> {
    let mut primes = (m..n + 1).filter(|&x| is_prime(x));
    primes.next().and_then(|mut prev| {
        primes.find(|&prim|
            if prim - prev == g as u64 {
                true
            } else {
                prev = prim;
                false
            }
        ).and_then(|second| Some((prev, second)))
    })
}

// assumption x > 2
fn is_prime(x: u64) -> bool {
    let sqrt_x = (x as f64).sqrt() as u64;
    (2..sqrt_x + 1).all(|t| x % t != 0)
}
__________________________________
fn gap(g: i32, m: u64, n: u64) -> Option<(u64, u64)> {
    let is_prime = |x: &u64| (2..=(*x as f64).sqrt() as u64).all(|n| x % n != 0);
    
    (m..=n).filter(is_prime)
        .zip((m..=n).filter(is_prime).skip(1))
        .find(|&(a, b)| b - a == g as u64)
}
__________________________________
fn gap(g: i32, m: u64, n: u64) -> Option<(u64, u64)> {
    (m..=n).filter(prime)
        .zip((m..=n).filter(prime).skip(1))
        .skip_while(|(a, b)| b - a != g as u64)
        .next()
}

fn prime(n: &u64) -> bool {
    (2..=(f64::from(*n as u32).sqrt().ceil() as u64))
        .all(|d| n % d != 0)
}
