use std::collections::HashSet;

fn doubleton(num: u32) -> u32 {
    let mut n=num+1;
    loop {
        if n.to_string().chars().collect::<HashSet<char>>().len() == 2 {
            break;
        }
        n+=1;
    }
    n
}

#############
fn doubleton(num: u32) -> u32 {
    ((num + 1)..)
        .find(|&i| digits(i).fold(0u32, |m, x| m | 1 << x % 10).count_ones() == 2)
        .unwrap()
}

fn digits(x: u32) -> impl Iterator<Item = u32> {
    std::iter::successors(Some(x), |&x| if x >= 10 { Some(x / 10) } else { None })
}
  
###########
use std::collections::HashSet;

fn doubleton(num: u32) -> u32 {
    let mut result = num + 1;
    while !is_doubleton(result) {
        result += 1;
    }
    result
}

fn is_doubleton(num: u32) -> bool {
    num.to_string().chars().collect::<HashSet<_>>().len() == 2
}
  
#################
fn doubleton(num: u32) -> u32 {
    let mut n = num;
    if is_doubleton(n) {n += 1;}
    while !is_doubleton(n) {n += 1;}
    n
}

fn is_doubleton(num: u32) -> bool {
    let mut s = num.to_string().into_bytes();
    s.sort();
    s.dedup();
    s.len() == 2
}
  
############
fn doubleton(mut n: u32) -> u32 {
    n += 1;
    let mut a = n; let mut b = None; let mut c = None;
    while a != 0 {
        let d = a % 10;
        if b.is_none() { b = Some(d); } else if c.is_none() {
            if b != Some(d) {c = Some(d); }
        } else if b != Some(d) && c != Some(d) {
            n += 1;a = n;b = None;c = None;continue;
        }
        a /= 10;
        if a==0 && c.is_none(){n += 1;a = n;b = None;}
    }
    n
}
