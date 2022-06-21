5263c6999e0f40dee200059d


use itertools::Itertools;

fn get_pins(observed: &str) -> Vec<String> {
    const CORRECTIONS: [&str; 10] = [
        "80", "124", "1235", "236", "1457", "24568", "3569", "478", "57890", "689"
    ];
    observed.bytes().map(|c| CORRECTIONS[(c - b'0') as usize].bytes())
        .multi_cartesian_product()
        .map(|cs| String::from_utf8(cs).unwrap())
        .collect()
}
______________________________
fn get_pins(observed: &str) -> Vec<String> {
    // def not best practice :P
    let adj_est = observed.chars().map(|a|
        ["08", "124", "1235", "236", "1457", "24568", "3569", "478", "05789", "689"]
        .iter().map(|b| b.chars().collect()).collect::<Vec<Vec<char>>>()
        [a.to_digit(10).unwrap() as usize].clone());
    let mut perm : Vec<String> = vec!["".to_string()];
    for options in adj_est {
        let mut new_perm : Vec<String> = vec![];
        for dir in perm.iter() {
            for opt in options.iter() {
                new_perm.push(dir.to_string() + &opt.to_string());
            }
        }
        perm = new_perm.clone();
    }
    perm
}
______________________________
fn possible_pins(pin: char) -> &'static [char] {
    match pin {
        '0' => &['0', '8'],
        '1' => &['1', '2', '4'],
        '2' => &['1', '2', '3', '5'],
        '3' => &['2', '3', '6'],
        '4' => &['1', '4', '5', '7'],
        '5' => &['2', '4', '5', '6', '8'],
        '6' => &['3', '5', '6', '9'],
        '7' => &['4', '7', '8'],
        '8' => &['5', '7', '8', '9', '0'],
        '9' => &['6', '8', '9'],
        _ => &[],
    }
}

fn get_pins(observed: &str) -> Vec<String> {
    observed.chars().fold(vec![String::new()], |results, ch| {
        results
            .into_iter()
            .flat_map(|previous| {
                possible_pins(ch)
                    .into_iter()
                    .map(move |pin| format!("{}{}", previous, pin))
            })
            .collect::<Vec<String>>()
    })
}
