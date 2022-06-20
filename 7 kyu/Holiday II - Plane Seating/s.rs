57e8f757085f7c7d6300009a


fn plane_seat(seat_number: &str) -> String {
    let mut s = seat_number.to_string();
    let code = s.pop().unwrap();
    let num = s.parse::<u32>().unwrap();
        
    let c = match code {
        'A'|'B'|'C' => "Left",
        'D'|'E'|'F' => "Middle",
        'G'|'H'|'K' => "Right",
        _ => "",
    };

    let n = match num {
        n if n >= 1 && n <= 20 => "Front",
        n if n >= 21 && n <= 40 => "Middle",
        n if n >= 41 && n <= 60 => "Back",
        _ => "",
    };

    if c.is_empty() || n.is_empty() { return "No Seat!!".to_string(); }
    format!("{}-{}", n, c)
}
_______________________________
fn plane_seat(seat_number: &str) -> String {    
    let row = match seat_number[..seat_number.len() - 1].parse::<u64>() {
        Ok(1..=20) => "Front",
        Ok(21..=40) => "Middle",
        Ok(0|41..=60) => "Back",
        _ => return "No Seat!!".to_owned()
    };
    let chair = match seat_number.chars().last() {
        Some('A'..='C') => "Left",
        Some('D'..='F') => "Middle",
        Some('G'|'H'|'K') => "Right",
        _ => return "No Seat!!".to_owned()
    };
    format!("{}-{}", row, chair)
}
_______________________________
fn plane_seat(seat_number: &str) -> String {
    let number = seat_number[..seat_number.len() - 1].parse::<usize>().unwrap();
    let letter = seat_number.chars().reduce(|_, chr| chr).unwrap();
    let number = match number {
        1..=20 => "Front",
        21..=40 => "Middle",
        0 | 41..=60 => "Back",
        _ => return "No Seat!!".to_owned(),
    };
    let letter = match letter {
        'A'..='C' => "Left",
        'D'..='F' => "Middle",
        'G' | 'H' | 'K' => "Right",
        _ => return "No Seat!!".to_owned(),
    };
    format!("{}-{}", number, letter)
}
