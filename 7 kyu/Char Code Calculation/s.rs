57f75cc397d62fc93d000059


fn calc(s: &str) -> u32 {
    s.chars().map(|c| (c as u8).to_string().chars().filter(|&c| c == '7').count() as u32).sum::<u32>() * 6
}
__________________________________
fn calc(s: &str) -> u32 {
    s.bytes()
        .map(|b| 6 * (b % 100 / 10 == 7) as u32 + 6 * (b % 10 == 7) as u32)
        .sum()
}
__________________________________
fn calc(s: &str) -> u32 {
    let mut n:u32 = 0;
    for c in s.chars(){
        if (c as u32 /10) == 7 {n+=1;}
        if (c as u32 %10) == 7 {n+=1;}
    }
    6*n
}
