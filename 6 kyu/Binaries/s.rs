fn code(s: &str) -> String {
    s.bytes().map(|b| {
        let bin = format!("{:b}", b - 48);
        format!("{}1{}", "0".repeat(bin.len() - 1), bin)
    }).collect()
}

fn from_bin(s: &str) -> u32 {
    s.bytes().fold(0, |n, b| n * 2 + b as u32 - 48)
}

fn decode(s: &str) -> String {
    if s.is_empty() { "".to_string() } else {
        let idx = s.find('1').unwrap() + 1;
        format!("{}{}", from_bin(&s[idx..idx*2]), decode(&s[idx*2..]))
    }
}
__________________________
fn code(s: &str) -> String {
    let codemap = ["10", "11", "0110", "0111", "001100", "001101", "001110", "001111", "00011000", "00011001"];
    let mut ss: Vec<&str> = Vec::new();
    for c in s.chars() {
        let n = c.to_digit(10).unwrap() as usize;
        ss.push(codemap[n]);
    }
    ss.join("")
}
fn decode(s: &str) -> String {
    let mut r = String::new();
    let mut i = 0;
    let lg = s.len();
    while i < lg {
        let mut zero_i = i;
        while zero_i < lg && s.chars().nth(zero_i) != Some('1') {
            zero_i = zero_i + 1;
        }
        let l = zero_i - i + 2;
        let h = &s[zero_i + 1..zero_i + l];
        let k = isize::from_str_radix(h, 2).unwrap().to_string();
        r = format!("{}{}", r, k);
        i = zero_i + l;
    }
    r
}
__________________________
fn code(s: &str) -> String {
    s.chars()
        .map(|c| c as i8 - '0' as i8)
        .map(|n| format!("{:b}", n))
        .map(|b| format!("{0:01$}{2}", 1, b.len(), b))
        .collect()
}

fn decode(s: &str) -> String {
    let mut cp = s;
    let mut result = String::new();
    while let Some(pos) = cp.find('1') {
        let p = pos + 1;
        result.push(('0' as u8 + u8::from_str_radix(&cp[p..p * 2], 2).unwrap()) as char);
        cp = &cp[(p * 2)..];
    }
    result
}
__________________________
fn code(s: &str) -> String {
    s.chars().map(|c| 
        { let binary = format!("{:b}",c.to_digit(10).unwrap_or(0));
          format!("{1:0>0$}{2:}", binary.len(), 1, binary)
        }).collect()
}

fn decode(s: &str) -> String {  
    let mut count = 0;
    let mut iter = s.chars();
    let mut result: String = String::new();
    loop {
        match iter.next() {
            None => break,
            Some(x)  => {
                if x == '0' {
                    count+=1;
                    continue;
                }

       
                let mut number: String = String::new();

                while count >= 0 {
                    match iter.next() {
                        Some(x) => number.push(x),
                        None => break,
                    }
                    count-=1;
                }
                count = 0;
                match isize::from_str_radix(&number, 2) {
                    Ok(x) => result.push_str(&x.to_string()),
                    Err(_) => break,
                }
            }
        }
    }
    result.to_string()
}
