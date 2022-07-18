515decfd9dcfc23bb6000006


use std::iter;

fn is_valid_ip(ip: &str) -> bool {
    ip.splitn(4, '.')
        .chain(iter::repeat(""))
        .take(4)
        .all(|token| {
            !(token.len() > 1 && token.starts_with('0')) && token.parse::<u8>().is_ok()
        })
}
_____________________________
fn is_valid_ip(ip: &str) -> bool {
    let segments: Vec<&str> = ip.split(".").collect();
    segments
        .iter()
        .all(|s| (!s.starts_with("0") || s.len() == 1) && s.parse::<u8>().is_ok())
        && segments.len() == 4
}
_____________________________
fn is_valid_ip(ip: &str) -> bool {
    let v = ip.split('.').collect::<Vec<_>>();
    if v.len() != 4 { return false; }
    
    v.iter().all(|x|{
        match x.parse::<u32>() {
            Ok(d) => if d > 255 || d.to_string().len() != x.len() { false } else { true }
            _ => false,
        } 
    })
}
