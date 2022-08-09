57f780909f7e8e3183000078


fn grow(array: Vec<i32>) -> i32 {
    array.iter().product()
}
_______________________
fn grow(array: Vec<i32>) -> i32 {
    array.iter().fold(1, |acc, x| acc * x)
}
_______________________
fn grow(array: Vec<i32>) -> i32 {
    let mut m = 1;
    for i in array {
        m *= i;
    }
    return m;
}
