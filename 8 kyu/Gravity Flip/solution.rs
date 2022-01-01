fn flip(dir: char, cubes: &[u32]) -> Vec<u32> {
    let mut res = cubes.to_vec();
    res.sort();
    if dir == 'L' { res.reverse(); }
    res
}
  
_____________________________________________
use itertools::Itertools;

fn flip(dir: char, cubes: &[u32]) -> Vec<u32> {
    let cmp: fn(&u32, &u32) -> std::cmp::Ordering = match dir {
        'R' => |a, b| a.cmp(b),
        'L' => |a, b| b.cmp(a),
        _ => unreachable!()
    };
    cubes.iter().cloned().sorted_by(cmp).collect()
}
  
_____________________________________________
fn flip(dir: char, cubes: &[u32]) -> Vec<u32> {
    let mut arr = cubes.to_vec();
    match dir {
        'R' => arr.sort_by(|a, b| a.cmp(b)),
        _ => arr.sort_by(|a, b| b.cmp(a))
        
    };
    arr
}
  
_____________________________________________
use itertools::Itertools;

fn flip(dir: char, cubes: &[u32]) -> Vec<u32> {
    match dir {
        'R' => cubes.iter().map(|&x| x).sorted().collect(),
        _ => cubes.iter().map(|&x| x).sorted().rev().collect()
    }
}
