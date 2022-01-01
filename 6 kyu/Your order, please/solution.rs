fn order(sentence: &str) -> String {
    let mut ws: Vec<_> = sentence.split_whitespace().map(String::from).collect();
    ws.sort_by_key(|s| s.chars().find(|c| c.is_digit(10)).unwrap());
    ws.join(" ")
}
      
_____________________________________________
fn order(sentence: &str) -> String {
    let mut ws: Vec<_> = sentence.split_whitespace().collect();
    ws.sort_by_key(|s| s.chars().find(|c| c.is_digit(10)).unwrap());
    ws.join(" ")
}
      
_____________________________________________
fn order(sentence: &str) -> String {
    let mut ws: Vec<_> = sentence.split_whitespace().collect();
    ws.sort_by_cached_key(|s| s.chars().find(|c| c.is_digit(10)).unwrap());
    ws.join(" ")
}
      
_____________________________________________
fn order(sentence: &str) -> String {
    let mut words = sentence.split_whitespace().collect::<Vec<&str>>();
    words.sort_by_key(|word| word.matches(char::is_numeric).next().unwrap());
    words.join(" ")
}
      
_____________________________________________
pub fn words(input_str: &str) -> Vec<&str> {
    input_str.trim().split_whitespace().collect()
}
pub fn get_number(words: Vec<&str>) -> Vec<(&str,i32)> {
    let mut result: Vec<(&str,i32)> = Vec::new();
    for word in words {
        let number = word.chars()
            .filter(|c| c.is_digit(10))
            .collect::<String>()
            .parse::<i32>()
            .unwrap();
        result.push((word,number));
    }
    result 
}

pub fn tuples_to_string(tuples: Vec<(&str,i32)>) -> String {
    let mut result = String::new();
    for (string,_) in &tuples {
        result.push_str(string);
        result.push(' ');
    }
    result.pop();
    result
}
pub fn order(sentence: &str) -> String {
    let mut res = get_number(words(sentence));
    res.sort_by_key(|k| k.1);
    tuples_to_string(res)
}
