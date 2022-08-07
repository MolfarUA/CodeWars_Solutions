57cfdf34902f6ba3d300001e


fn two_sort(arr: &[&str]) -> String {
    arr.iter().min().unwrap().chars().map(|c| c.to_string()).collect::<Vec<_>>().join("***")
}
___________________________
fn two_sort(arr: &[&str]) -> String {
    arr.iter()
        .min()
        .unwrap()
        .chars()
        .fold(String::new(), |acc, s| format!("{}***{}", acc, s))[3..]
        .to_string()
}
___________________________
fn two_sort(arr: &[&str]) -> String {
    let mut v = arr.to_vec();
    v.sort();
    v[0].chars().map(|c| c.to_string()).collect::<Vec<String>>().join("***")
}
___________________________
extern crate itertools;
use itertools::Itertools;

fn two_sort(arr: &[&str]) -> String {
  arr.iter().min().unwrap().chars().intersperse('*').intersperse('*').collect()
}
___________________________
fn two_sort(arr: &[&str]) -> String {
    let mut res = arr.iter().min().expect("Array is empty.").to_string();
    for i in (1..res.len()).rev() {
        res.insert_str(i, "***");
    }
    res
}
