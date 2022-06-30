53af2b8861023f1d88000832


fn are_you_playing_banjo(name: &str) -> String {
    match &name[0..1] {
        "R" | "r" => format!("{} plays banjo", name),
        _ => format!("{} does not play banjo", name)
    }
}
________________________________
fn are_you_playing_banjo(name: &str) -> String {
    match name.to_lowercase().starts_with("r") {
        true => format!("{} plays banjo", name),
        false => format!("{} does not play banjo", name)
    }
}
________________________________
fn are_you_playing_banjo(name: &str) -> String {
    format!("{} {} banjo", name, if "Rr".contains(&name[0..1]) {"plays"} else {"does not play"})
}
