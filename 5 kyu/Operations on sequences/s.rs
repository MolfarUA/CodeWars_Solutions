fn solve(arr: Vec<i128>) -> (i128, i128) {
    arr[2..].chunks(2)
            .fold((arr[0],arr[1]), |(a,b),x|(a*x[0]+b*x[1], (a*x[1]-b*x[0]).abs()))
}
_____________________________________
fn solve(arr: Vec<i128>) -> (i128, i128) {
    let a = arr[0]; let b = arr[1]; let c = arr[2]; let d = arr[3];
    let first4 = [i128::abs(a*c - b*d), (a*d + b*c)].to_vec();
    if arr.len() == 4 {
        return (first4[0], first4[1]);
    }
    return solve([&first4[..], &arr[4..]].concat());
}
_____________________________________
use itertools::Itertools;

fn solve(arr: Vec<i128>) -> (i128, i128) {
    arr.iter().tuples::<(_,_)>().fold((1, 0), |(a, b), (c, d)| ((a * c - b * d).abs(), a * d + b * c))
}
_____________________________________
fn h(a: &[i128]) -> [i128; 2] {
    [
        (a[0] * a[2] - a[1] * a[3]).abs(),
        (a[0] * a[3] + a[1] * a[2]),
    ]
}

fn solve(mut a: Vec<i128>) -> (i128, i128) {
    while a.len() >= 4 {
        let i = a.len() - 4;
        a.splice(i.., h(&a[i..]));
    }
    (a[0], a[1])
}
_____________________________________
fn solve(arr: Vec<i128>) -> (i128, i128) {
    arr.chunks(2).fold((1, 0), |(a, b), c| (a * c[0] + b * c[1], (a * c[1] - b * c[0]).abs()))
}
