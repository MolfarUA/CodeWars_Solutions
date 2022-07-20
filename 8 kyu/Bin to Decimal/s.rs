57a5c31ce298a7e6b7000334


fn bin_to_decimal(inp: &str) -> i32 {
    i32::from_str_radix(inp, 2).unwrap_or(0)
}
_________________________
fn bin_to_decimal(inp: &str) -> i32 {
    i32::from_str_radix(inp, 2).expect("Parsing error.")
}
_________________________
fn bin_to_decimal(inp: &str) -> i32 {
    inp.chars().map(|c| if c == '1' { 1 } else { 0 }).fold(0, |sum, c| (sum << 1) + c)
}
