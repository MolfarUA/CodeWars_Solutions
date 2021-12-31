fn format_duration(seconds: u64) -> String {
    let result = [
        ("year", 31536000, 100000),
        ("day", 86400, 365),
        ("hour", 3600, 24),
        ("minute", 60, 60),
        ("second", 1, 60),
    ].iter()
    .map(|(unit, duration, modulo)| (seconds / duration % modulo, unit))
    .filter_map(|(duration, unit)| match duration {
        _ if duration == 1 => Some(format!("{} {}", duration, unit)),
        _ if duration != 0 => Some(format!("{} {}s", duration, unit)),
        _ => None,
    }).collect::<Vec<String>>();

    match result.len() {
        0 => String::from("now"),
        1 => result.join(""),
        _ => result
            .split_last()
            .map(|(r, l)| l.join(", ") + " and " + r)
            .unwrap(),
    }
}

__________________________________________________
const SECOND: u64 = 1;
const MINUTE: u64 = 60 * SECOND;
const HOUR: u64 = 60 * MINUTE;
const DAY: u64 = 24 * HOUR;
const YEAR: u64 = 365 * DAY;

enum Unit {
    SECONDS,
    MINUTES,
    HOURS,
    DAYS,
    YEARS,
}

struct Time {
    kind: Unit,
    amt: u64,
}

impl Time {
    fn unit_str(&self) -> &str {
        match self.kind {
            Unit::SECONDS => "second",
            Unit::MINUTES => "minute",
            Unit::HOURS => "hour",
            Unit::DAYS => "day",
            Unit::YEARS => "year",
        }
    }
    
    fn as_string(&self) -> String {
        let has_s = |x| if x > 1 { "s" } else { "" };
        
        format!("{} {}{}", self.amt, self.unit_str(), has_s(self.amt))
    }
}

fn format_duration(seconds: u64) -> String {
    let years = seconds / YEAR;
    let days = (seconds % YEAR) / DAY;
    let hours = (seconds % DAY) / HOUR;
    let minutes = (seconds % HOUR) / MINUTE;
    let secs = seconds % MINUTE;
    
    let t = |u, l| Time{ kind: u, amt: l };
    
    let times = 
        [t(Unit::YEARS, years), t(Unit::DAYS, days), t(Unit::HOURS, hours), 
            t(Unit::MINUTES, minutes), t(Unit::SECONDS, secs)]
        .iter()
        .filter(|x| x.amt > 0)
        .map(|t| t.as_string())
        .collect::<Vec<String>>();
    
    match times.len() {
        0 => String::from("now"),
        1 => times.first().unwrap().to_string(),
        _ => format!("{} and {}", times[..times.len() - 1].join(", "), times.last().unwrap()),
    }
}

__________________________________________________
fn format_duration(seconds: u64) -> String {
    let y = seconds / 31536000;
    let d = seconds / 86400 % 365;
    let h = seconds / 3600 % 24;
    let m = seconds / 60 % 60;
    let s = seconds % 60;
    let time: [(u64, &'static str); 5] = [(y, "year"), (d, "day"), (h, "hour"), (m, "minute"), (s, "second")];
    let str_v: Vec<_> = time.into_iter().filter(|t| t.0 != 0)
        .map(|&(i, u)| format!("{} {}{}", i, u, if i == 1 { "" } else { "s" })).collect();
    match str_v.len() {
        0 => "now".into(),
        1 => str_v[0].clone(),
        c => str_v.iter().cloned().take(c - 1).collect::<Vec<_>>().join(", ") + &format!(" and {}", str_v[c - 1]),
    }
}
