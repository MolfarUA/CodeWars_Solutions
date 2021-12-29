fn alphabet_position(text: &str) -> String {
    text.to_lowercase()
        .chars()
        .filter(|c| c >= &'a' && c <= &'z')
        .map(|c| (c as u32 - 96).to_string())
        .collect::<Vec<String>>()
        .join(" ")
}

________________________________________________
const CHAR_OFFSET: u8 = 96;

fn alphabet_position(text: &str) -> String {
    text
        .chars()
        .filter(|c| c.is_alphabetic())
        .map(|c| (c.to_ascii_lowercase() as u8 - CHAR_OFFSET).to_string())
        .collect::<Vec<String>>()
        .join(" ")
}
          
________________________________________________
fn alphabet_position(text: &str) -> String {
    text.chars()
        .filter(|c| c.is_ascii_alphabetic())
        .map(|c| (c.to_ascii_uppercase() as u8 - 64).to_string())
        .collect::<Vec<_>>()
        .join(" ")
}
          
________________________________________________
const ALPHABET: &str = "abcdefghijklmnopqrstuvwxyz";

fn alphabet_position(text: &str) -> String {
    let lower_txt = text.to_ascii_lowercase();
    let mut numbers = Vec::new();

    for c in lower_txt.chars() {
        if let Some(number) = ALPHABET.find(c) {
            numbers.push((number + 1).to_string());
        }
    }

    numbers.join(" ")
}
