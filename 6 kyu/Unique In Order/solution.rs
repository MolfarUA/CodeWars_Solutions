fn unique_in_order<T>(sequence: T) -> Vec<T::Item>
where
    T: std::iter::IntoIterator,
    T::Item: std::cmp::PartialEq + std::fmt::Debug,
{
    let mut v: Vec<_> = sequence.into_iter().collect();
    v.dedup();
    v
}
_____________________________________________
use std::iter::FromIterator;

fn unique_in_order<T>(iter: T) -> Vec<T::Item>
where
    T: IntoIterator,
    T::Item: PartialEq,
{
    let mut vec = Vec::from_iter(iter);
    vec.dedup();
    vec
}
_____________________________________________
fn unique_in_order<T>(sequence: T) -> Vec<T::Item>
where
    T: std::iter::IntoIterator,
    T::Item: std::cmp::PartialEq + std::fmt::Debug,
{
    sequence.into_iter().fold(Vec::new(), |mut v, i| {
        if let Some(last) = v.last() {
            if last != &i {
                v.push(i);
            }
        } else {
            v.push(i);
        }
        v
    })
}
_____________________________________________
fn unique_in_order<T>(sequence: T) -> Vec<T::Item>
where
    T: std::iter::IntoIterator,
    T::Item: std::cmp::PartialEq + std::fmt::Debug,
{
    let mut v = vec![];    
    let mut sequence = sequence.into_iter();
    if let Some(prev) = sequence.next() {
        v.push(prev);
        let mut prev = &v[0];
        while let Some(next) = sequence.next() {
            if prev != &next {
                v.push(next);
                prev = v.last().unwrap();
            }
        }
    } 
    
    v
}
