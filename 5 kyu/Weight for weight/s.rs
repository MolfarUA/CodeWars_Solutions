55c6126177c9441a570000cc


fn order_weight(s: &str) -> String {
  let mut numbers = s.split_whitespace().collect::<Vec<_>>();
  numbers.sort();
  numbers.sort_by_key(|s| s.chars().flat_map(|c| c.to_digit(10)).sum::<u32>());
  numbers.join(" ")
}
______________________________
fn weight(num: &str) -> i32 {
    num
        .chars()
        .map(|x| x.to_digit(10).unwrap())
        .fold(0, |a, x| a + x as i32)
}
fn comp(l: &str, r: &str) -> std::cmp::Ordering {
    if weight(l) == weight(r) {
        l.cmp(&r)
    } else {
        weight(l).cmp(&weight(r))
    }
}
fn order_weight(s: &str) -> String {
    let mut ss = s.split(' ').collect::<Vec<&str>>();
    ss.sort_by(|l, r| comp(l, r));
    ss.join(" ")
}
______________________________
fn weight(w: &str) -> u32 {
 w.chars()
  .fold(0, |total, c|
    total + c.to_digit(10).unwrap()
  )
}

fn order_weight(s: &str) -> String {
  let mut weigths = s.split_whitespace().collect::<Vec<_>>();

  weigths.sort_by_key(|&w| {
    (weight(w), w)
  });

  weigths.join(" ")
}
