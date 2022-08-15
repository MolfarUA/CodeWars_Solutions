52f677797c461daaf7000740


use num::integer::gcd;

fn solution(xs: &[u64]) -> u128 {
    xs.len() as u128 * xs.iter().copied().fold(0, gcd) as u128
}
_______________________________
fn gcd(a: u64, b: u64) -> u64 {
    if a == 0 {
        b
    } else {
        gcd(b % a, a)
    }
}

fn solution(arr: &[u64]) -> u128 {
    let mut nums = arr.to_vec();
    let count = nums.len();
    
    let mut divider = nums[0];
    for i in 1..count {
        divider = gcd(divider, nums[i]);
    }
    
    (count as u128) * (divider as u128)
}
_______________________________
use num::Integer;

fn solution(arr: &[u64]) -> u128 {
    let mut r = 0u64;
    for n in arr.iter() {
        r = r.gcd(n);
    }
    r as u128 * arr.len() as u128
}
