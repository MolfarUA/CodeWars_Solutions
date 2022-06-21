58708934a44cfccca60000c4


extern crate regex;
use regex::{Regex, Captures};

pub fn highlight(code: &str) -> String {
    let re = Regex::new(r"F+|L+|R+|\d+").unwrap();
    re.replace_all(code, |c: &Captures| match c[0].chars().next().unwrap() {
        'F' => format!(r#"<span style="color: pink">{}</span>"#, &c[0]),
        'L' => format!(r#"<span style="color: red">{}</span>"#, &c[0]),
        'R' => format!(r#"<span style="color: green">{}</span>"#, &c[0]),
        _ => format!(r#"<span style="color: orange">{}</span>"#, &c[0]),
    }).to_string()
}
__________________________
fn flush(s: &mut String, c: &Option<&str>, a: &str) {
    if !a.is_empty() {
        match c {
            &Some(color) => s.push_str(&format!(r#"<span style="color: {}">{}</span>"#, color, a)),
            &None => s.push_str(a)
        }
    }
}

pub fn highlight(code: &str) -> String {
  let mut res = String::new();
  let mut current_color = None;
  let mut acc = String::new();
  for c in code.chars() {
      let color = match c {
          'F' => Some("pink"),
          'L' => Some("red"),
          'R' => Some("green"),
          _ if c.is_digit(10) => Some("orange"),
          _ => None,
      };
      if color != current_color {
          flush(&mut res, &current_color, &acc);
          acc.clear();
      }
      current_color = color;
      acc.push(c);
  }
  flush(&mut res, &current_color, &acc);
  res
}
__________________________
extern crate itertools;
use itertools::Itertools;

pub fn highligh_sub(code: &str) -> String {
    match code.chars().nth(0) {
        Some('F') => format!("<span style=\"color: pink\">{}</span>", code),
        Some('L') => format!("<span style=\"color: red\">{}</span>", code),
        Some('R') => format!("<span style=\"color: green\">{}</span>", code),
        Some(x) if x.is_numeric() => format!("<span style=\"color: orange\">{}</span>", code),
        _ => format!("{}", code)
    }
}

pub fn highlight(code: &str) -> String {
    code.chars()
        .group_by(|c| if c.is_numeric() {'0'} else {*c})
        .into_iter()
        .map(|(_, group)| highligh_sub(&group.collect::<String>()))
        .collect()
}
