54b72c16cd7f5154e9000457


mod preloaded;
use preloaded::MORSE_CODE;
// MORSE_CODE is `HashMap<String, String>`. e.g. ".-" -> "A".

pub fn decode_bits(encoded: &str) -> String {
    // Trim excess zeros at the start and end
    let encoded = encoded.trim_matches('0');
    
    // Get the length of a time unit by finding the shortest sequence of zeros or ones,
    // this will represent a time unit of one which equals a dot
    let rate = {
        let rate_ones = encoded
            .split("0")
            .filter_map(|ones| (!ones.is_empty()).then(|| ones.len()))
            .min()
            .unwrap_or(usize::MAX);
        let rate_zeros = encoded
            .split("1")
            .filter_map(|zeros| (!zeros.is_empty()).then(|| zeros.len()))
            .min()
            .unwrap_or(usize::MAX);
        rate_zeros.min(rate_ones)
    };

    // Parse the encoded message
    encoded
        .chars() // Iterate through the characters
        .step_by(rate) // Only parse every n-th code
        .collect::<String>() // Collect it into a string
        // Begin converting from 1/0 to dot/dash
        .replace("111", "-") // Dash
        .replace("1", ".") // Dot
        .replace("0000000", "   ") // Word seperator
        .replace("000", " ") // Letter seperator
        .replace("0", "") // Dot/Dash seperator
}

pub fn decode_morse(encoded: &str) -> String {
    encoded
        .trim()
        .split("   ")
        .map(|word| {
            word.split(" ")
                .filter_map(|letter| MORSE_CODE.get(letter).map(|letter| letter.clone()))
                .collect::<String>()
        })
        .collect::<Vec<String>>()
        .join(" ")
}
_____________________________
mod preloaded;
use preloaded::MORSE_CODE;
// MORSE_CODE is `HashMap<String, String>`. e.g. ".-" -> "A".

use itertools::Itertools;
use num::Integer;

pub fn decode_bits(encoded: &str) -> String {
    lazy_static::lazy_static! {
        static ref GROUP: regex::Regex = regex::Regex::new("0+|1+").unwrap();
    };
    let encoded = encoded.trim_matches('0');
    let step = GROUP
        .find_iter(&encoded)
        .map(|_match| _match.as_str().len())
        .fold(0, |div, next| div.gcd(&next));
    return encoded
        .chars()
        .step_by(step)
        .collect::<String>()
        .replace("111", "-")
        .replace("1", ".")
        .replace("0000000", " ")
        .replace("000", "/")
        .replace("0", "");
}

pub fn decode_morse(encoded: &str) -> String {
    return encoded
        .split(' ')
        .map(|w| w.split('/').filter_map(|m| MORSE_CODE.get(m)).join(""))
        .join(" ");
}
_____________________________
use itertools::Itertools;

mod preloaded;
use preloaded::MORSE_CODE;

pub fn decode_bits(encoded: &str) -> String {
    encoded.to_string() // Let's do this in a single function...
}

pub fn decode_morse(encoded: &str) -> String {
    let encoded = encoded.trim_matches('0');

    let len_unit = encoded
        .chars()
        .group_by(|&c| c)
        .into_iter()
        .map(|(_zero_or_one, group)| group.count())
        .min()
        .unwrap();

    let dot = "1".repeat(1 * len_unit);
    let dash = "1".repeat(3 * len_unit);
    let pause_signs = "0".repeat(1 * len_unit);
    let pause_chars = "0".repeat(3 * len_unit);
    let pause_words = "0".repeat(7 * len_unit);

    encoded
        .split(&pause_words)
        .map(|word| {
            word.split(&pause_chars)
                .map(|char| {
                    let sign = char
                        .split(&pause_signs)
                        .map(|sign| {
                            if sign == dot {
                                '.'
                            } else if sign == dash {
                                '-'
                            } else {
                                panic!("Bad data: {}", sign)
                            }
                        })
                        .join("");
                    MORSE_CODE.get(&sign).unwrap()
                })
                .join("")
        })
        .join(" ")
}
