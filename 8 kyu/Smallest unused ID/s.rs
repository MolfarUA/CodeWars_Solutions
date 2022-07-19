55eea63119278d571d00006a


fn next_id(ids: &[usize]) -> usize {
    (0..).skip_while(|x| ids.contains(&x)).next().unwrap()
}
______________________
fn next_id(ids: &[usize]) -> usize {
    (0..).find(|n| !ids.contains(&n)).unwrap()
}
______________________
fn next_id(a: &[usize]) -> usize {
    let m: std::collections::HashSet<_> = a.iter().collect();
    let mut i = 0;
    while m.contains(&i) { i += 1; }
    i
}
