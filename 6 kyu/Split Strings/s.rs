515de9ae9dcfc28eb6000001


use itertools::Itertools;

fn solution(s: &str) -> Vec<String> {
    s.chars().chunks(2).into_iter().map(|c| c.pad_using(2, |_| '_').collect()).collect()
}
________________________________
fn solution(s: &str) -> Vec<String> {
    s.chars()
        .collect::<Vec<_>>()
        .chunks(2)
        .map(|v| {
            if v.len() == 1 {
                format!("{}_", v[0])
            } else {
                v.into_iter().collect()
            }
        })
        .collect()
}
________________________________
fn solution(s: &str) -> Vec<String> {
    s.chars()
        .chain(std::iter::once('_'))
        .collect::<Vec<_>>()
        .chunks_exact(2)
        .map(|chunk| chunk.iter().collect())
        .collect()    
}
________________________________
fn solution(s: &str) -> Vec<String> {
    let odds: Vec<char> = s.chars().step_by(2).collect();
    let mut evens: Vec<char> = s.chars().skip(1).step_by(2).collect();
    if odds.len() != evens.len() {
        evens.push('_');
    }
    odds.iter().zip(evens.iter()).map(|(c1, c2)| format!("{}{}", c1, c2)).collect()
}
________________________________
fn solution(s: &str) -> Vec<String> {
    let first = s.chars().step_by(2);
    let second = s.chars().skip(1).step_by(2).chain(std::iter::once('_'));
    first
        .zip(second)
        .map(|(a, b)| format!("{}{}", a, b))
        .collect()
}
