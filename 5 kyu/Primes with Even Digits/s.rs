// use itertools::Itertools;

fn sieve(in_n: u32) -> Vec<u32> {
    let n = in_n as usize;
    let mut a = Vec::new();
    a.resize(n, true);
    for i in 2..(f64::sqrt(n as f64) as usize + 1) {
        if a[i] {
            for j in (i*i..n).step_by(i) {
                a[j] = false;
            }
        }
    }
    return a.iter().enumerate().filter_map(|(i, &t)| {
      if t {Some(i as u32)} else {None}   
    }).collect();
}

fn num_even_digits(n: u32) -> u32 {
    format!("{}", n).chars().filter_map(|c| c.to_digit(10)).filter(|d| d%2==0).count() as u32
}

fn f(n: u32) -> u32 {
    let primes = sieve(n);
    let ned_ps = primes.iter().map(|&p| (num_even_digits(p), p));
    let max = ned_ps.fold(None::<(u32, u32)>, |res, item| { match res {
        Some(acc) => if item.0 >= acc.0 { Some(item) } else { Some(acc) },  // Take last of equivalent.
        None => Some(item)
    }});
    max.unwrap().1
}
____________________________________________
fn f(n: u32) -> u32 {
    (0..n).rev().find(|x| check(*x) && is_prime(*x)).unwrap()
}

fn check(k: u32) -> bool {
    let mut s: Vec<char> = k.to_string().chars().collect();
    s.pop();
    if s[0] == '1' {
        s.remove(0);
    }
    s.iter().all(|x| x.to_digit(10).unwrap() & 1 == 0)
}

fn is_prime(x: u32) -> bool {
    if x%2==0 || x%3==0 || x%5==0 {return false;}
    let c = [4, 2, 4, 2, 4, 6, 2, 6];
    let mut p = 7;
    let mut i=0;
    let s=(x as f64).sqrt() as u32;
    while p <= s {
        if x%p == 0 {return false;}
        else {p += c[i];}
        i = (i+1)%8;
    }
    true
}
