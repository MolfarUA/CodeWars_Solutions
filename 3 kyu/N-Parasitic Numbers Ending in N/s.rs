55df87b23ed27f40b90001e5


fn calc_special(last_digit: u8, base: u8) -> String {
    let mut digits: Vec<u8> = Vec::new();

    let mut current_digit: u8 = last_digit;
    let mut remains: u16 = 0u16;

    loop {
        digits.push(current_digit);
        let sum: u16 = current_digit as u16 * last_digit as u16 + remains;
        if sum == last_digit as u16 {
            break;
        }
        current_digit = (sum % base as u16) as u8;
        remains = sum / base as u16;
    }
    digits.reverse();
    let mut result: String = String::new();
    for d in digits {
        result.push(to_char(d));
    }
    return result;
}

fn to_char(n: u8) -> char {
    return if n <= 9 {
        char::from_u32(('0' as u32) + n as u32).unwrap()
    } else {
        char::from_u32(('A' as u32) + n as u32 - 10u32).unwrap()
    }
}
____________________________
fn calc_special(last_digit: u8, base: u8) -> String {
    if last_digit == 1 { return "1".to_owned(); }
    let mut nums = Vec::new();
    nums.push(last_digit);
    let mut prev = last_digit;
    let mut carry = 0;
    while prev != 0 || carry != 1 {
        let cur = prev * last_digit + carry;
        prev = cur % base;
        nums.push(prev);
        carry = cur / base;
    }
    nums.push(carry);
    nums.reverse();
    nums.into_iter().map(|n| char::from_digit(n as u32, base as u32).unwrap()).collect::<String>()
}
____________________________
fn calc_special(last_digit: u8, base: u8) -> String {
    let last_digit = last_digit as u32;
    let base = base as u32;
    
    let mut digits = vec![last_digit, 0, 0];
    let mut idx = 0;
    
    while idx == 0 || digits[idx] != last_digit || digits[idx + 1] != 0 {
        let next = digits[idx ] * last_digit + digits[idx + 1];
        idx += 1;
        digits[idx] = next % base;
        digits[idx + 1] = next / base;
        digits.push(0);
    }
    digits.reverse();
    
    digits[3..].into_iter().map(|&d| char::from_digit(d, base).expect("Digit should be valid")).collect()
}
