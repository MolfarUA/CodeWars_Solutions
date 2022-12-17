58bc16e271b1e4c5d3000151


fn get_min_base(number: u64) -> u64 {
    for i in (2..=(number as f64).log2().ceil() as u64).rev() {
        let b = (number as f64).powf(1.0 / i as f64) as u64;
        let mut a = number;
        
        while a % b == 1 {
            a = (a - 1) /b;
        }
        
        if a == 0 { return b; }
    }
    
    number - 1
}
______________________________________
fn get_min_base(number: u64) -> u64 {
    for i in 2..number.min(60000) {
        let mut t = 0;
        let mut j = 0;
        while t <= number / i {
            t += i.pow(j);
            j += 1;
            if t == number {
                return i;
            }
        }
    }
    let x = f64::floor(f64::sqrt(number as f64)) as u64;
    let y = f64::floor(f64::powf(number as f64, 1.0/3.0)) as u64;
    if x*x + x + 1 == number {
        x
    } else if y*y*y + y*y + y + 1 == number {
        y
    } else {
        number-1
    }
}
______________________________________
fn get_min_base(n: u64) -> u64 {
    for k in (2..=(n as f64).log2().ceil() as u64).rev() {
        let b = (n as f64).powf(1. / k as f64) as u64;
        let mut a = n;
        while a % b == 1 {
            a = (a - 1) / b;
        }
        if a == 0 {
            return b;
        }
    }
    n - 1
}
