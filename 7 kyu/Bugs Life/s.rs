5b71af678adeae41df00008c


fn shortest_distance(a: f64, b: f64, c: f64) -> f64 {
    let largest = a.max(b).max(c);
    let sum_others = a + b + c - largest;
    sum_others.hypot(largest)
}
____________________________
fn shortest_distance(a: f64, b: f64, c: f64) -> f64 {
    match a.max(b).max(c) {
        v if v==a => (a*a + (b+c).powf(2.0)).sqrt(),
        v if v==b => (b*b + (a+c).powf(2.0)).sqrt(),
        v if v==c => (c*c + (a+b).powf(2.0)).sqrt(),
        _ => panic!(),
    }
}
____________________________
fn shortest_distance(a: f64, b: f64, c: f64) -> f64 {
    let mut r = [a,b,c].to_vec();
    r.sort_by(|a,b| a.partial_cmp(b).unwrap());
    (r[0] + r[1]).hypot(r[2])
}
