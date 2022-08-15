5659c6d896bc135c4c00021e


fn next_smaller_number(n: u64) -> Option<u64> {
    let mut digs = n.to_string().chars()
            .map(|c| c.to_digit(10).unwrap())
            .collect::<Vec<u32>>();
    let bnp = digs.windows(2).rposition(|d| d[0] > d[1])?;
    let bn = digs[bnp];
    let mn = digs[bnp+1..].iter().filter(|&d| d < &bn).max()?;
    let mnp = digs.iter().rposition(|&d| d == *mn)?;
    digs.swap(bnp, mnp);
    let (_, tail) = digs.split_at_mut(bnp+1);
    tail.reverse();
    if digs[0] == 0 { return None; }
    digs.into_iter()
        .map(|d| std::char::from_digit(d, 10).unwrap()).collect::<String>()
        .parse::<u64>().ok()
}
_______________________________
fn next_smaller_number(mut n: u64) -> Option<u64> {
    let mut digits = vec![];
    while n > 0 {
        let d = n % 10;
        n /= 10;
        digits.push(d);
    }

    for i in 1..digits.len() {
        if let Some(pos) = digits[0..i].iter().position(|&j| j < digits[i]) {
            digits.swap(pos, i);
            digits[0..i].sort_unstable();
            digits.reverse();

            if digits[0] == 0 {
                return None;
            }

            let mut res = 0;
            for d in digits {
                res *= 10;
                res += d;
            }

            return Some(res);
        }
    }

    None
}
_______________________________
fn next_smaller_number(n: u64) -> Option<u64> {
    let mut ds = n.to_string().into_bytes();
    let i = ds.windows(2).rposition(|de| matches!(de, [d, e] if d > e))?;
    let j = ds.iter().rposition(|&d| d < ds[i]).unwrap();
    ds.swap(i, j);
    ds[(i + 1)..].reverse();
    (ds[0] != b'0').then(|| String::from_utf8(ds).unwrap().parse().unwrap())
}
