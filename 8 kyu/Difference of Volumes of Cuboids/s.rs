58cb43f4256836ed95000f97


type Cuboid = [i32; 3];

fn find_difference(a: &Cuboid, b: &Cuboid) -> i32 {
    (volume(a) - volume(b)).abs()
}

fn volume(c: &Cuboid) -> i32 {
    c[0] * c[1] * c[2]
}
________________________
fn find_difference(a: &[i32; 3], b: &[i32; 3]) -> i32 {
    i32::abs(a.iter().product::<i32>() - b.iter().product::<i32>())
}
________________________
fn find_difference(a: &[i32; 3], b: &[i32; 3]) -> i32 {
    (a.iter().product::<i32>() - b.iter().product::<i32>()).abs()
}
