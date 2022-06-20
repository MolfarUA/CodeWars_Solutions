566fc12495810954b1000030


fn nb_dig(n: i32, d: i32) -> i32 {
    let ex = d.to_string();
    (0..=n).map(|v| (v*v).to_string()).fold(0, |acc, v| acc + v.matches(&ex).count() as i32)
}
____________________________
use std::str::FromStr;
fn nb_dig(n: i32, d: i32) -> i32 {
    let d_char = char::from_str(&d.to_string()).unwrap();
    (0..n + 1).map(|x| {
        x.pow(2)
            .to_string()
            .chars()
            .filter(|s| s.eq(&d_char))
            .count()
    }).sum::<usize>() as i32
}
____________________________
fn nb_dig(n: i32, d: i32) -> i32 {
    let d = d.to_string();
    (0..=n).map(|x| (x * x).to_string().match_indices(&d).count() as i32).sum()
}
