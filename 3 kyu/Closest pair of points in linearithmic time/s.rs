5376b901424ed4f8c20002b7


use itertools::Itertools;

fn closest_pair(points: &[(f64, f64)]) -> ((f64, f64), (f64, f64)) {
    let mut p = points.to_vec();
    p.sort_by(|(a, _), (b, _)| a.partial_cmp(&b).unwrap());
    closest_pair_impl(&p)
}

fn dist(p1: (f64, f64), p2: (f64, f64)) -> f64 {
    ((p1.0 - p2.0).powf(2.0) + (p1.1 - p2.1).powf(2.0)).sqrt()
}

fn smallest_brute_force(points: &[(f64, f64)], mut min: f64, mut r: ((f64, f64), (f64, f64)), break_early: bool) 
    -> ((f64, f64), (f64, f64)) 
{
    for i in 0..points.len() {
        for j in (i+1)..points.len() {
            if break_early && (points[i].1 - points[j].1).abs() > min { break; }
            if dist(points[i], points[j]) < min {
                min = dist(points[i], points[j]);
                r = (points[i], points[j]);
            }
        }
    }
    r
}

fn closest_pair_impl(points: &[(f64, f64)]) -> ((f64, f64), (f64, f64)) {
    if points.len() <= 3 {
        return smallest_brute_force(points, f64::INFINITY, ((0.0, 0.0), (0.0, 0.0)), false);
    }
    let mid = points.len() / 2;
    let c1 = closest_pair_impl(&points[..mid]);
    let c2 = closest_pair_impl(&points[mid..]);
    
    let min = f64::min(dist(c1.0, c1.1), dist(c2.0, c2.1));
    let r = if dist(c1.0, c1.1) < dist(c2.0, c2.1) { c1 } else { c2 };
    
    let close_to_mid: Vec<(f64, f64)> = points.iter().copied()
        .filter(|p| (p.0 - points[mid].0).abs() <= min)
        .sorted_by(|(_, a), (_, b)| a.partial_cmp(&b).unwrap()).collect();
    
    smallest_brute_force(&close_to_mid, min, r, true)
}
______________________________________
use itertools::Itertools;

fn closest_pair(points: &[(f64, f64)]) -> ((f64, f64), (f64, f64)) {
    let n = points.len();
    let mut l = f64::MAX;
    let mut a = 0;
    let mut b = 0;
    let mut tolerance = l.sqrt();
    let arr: Vec<(f64, f64)> = points.iter()
                                     .cloned()
                                     .sorted_by(|&a,&b| (a.0)
                                     .partial_cmp(&b.0).unwrap())
                                     .collect();
    for i in 0..(n-1) {
        for j in (i+1)..n {
            if arr[j].0 >= arr[i].0 + tolerance {
                break
            } else {
                let ls = (arr[i].0 - arr[j].0).powf(2.0) + (arr[i].1 - arr[j].1).powf(2.0);
                if ls < l {
                    l = ls;
                    tolerance = l.sqrt();
                    a = i;
                    b = j;
                }
            }
        } 
    }
    
    (arr[a], arr[b])
}
______________________________________
fn closest_pair(points: &[(f64, f64)]) -> ((f64, f64), (f64, f64)) {
    if points.len() < 3 {
        return (
            points.first().unwrap().clone(),
            points.last().unwrap().clone(),
        );
    }

    // find min coordinate to use as the basis for the grid
    let min = points
        .iter()
        .fold((std::f64::MAX, std::f64::MAX), |(min_x, min_y), &(x, y)| {
            (min_x.min(x), min_y.min(y))
        });

    let mut distance = std::f64::MAX;
    for i in 0..points.len() - 1 {
        let dx = points[i].0 - points[i + 1].0;
        let dy = points[i].1 - points[i + 1].1;
        distance = distance.min(dx * dx + dy * dy);
        if distance == 0.0 {
            // no need to continue as we found duplicate points
            // this also protects against the divide by zero error
            return (points[i].clone(), points[i + 1].clone());
        }
    }
    distance = distance.sqrt();

    // split points into cells with size `distance` and put them into a hashmap
    // this reduces the number of comparisons needed to find the closest pair
    // from O(n^2) to aproximate O(n log n) assuming that `distance` splits points good enough
    let mut cells = std::collections::HashMap::new();
    for &(x, y) in points {
        let key = (
            ((x - min.0) / distance) as i32,
            ((y - min.1) / distance) as i32,
        );
        cells.entry(key).or_insert(Vec::new()).push((x, y));
    }

    // find closest pair in each cell and it's neighbors
    let mut distance = std::f64::MAX;
    let mut closest_pair = (
        points.first().unwrap().clone(),
        points.last().unwrap().clone(),
    );
    for (&(cell_x, cell_y), points) in cells.iter() {
        // check in the cell itself
        for i in 0..points.len() - 1 {
            for j in i + 1..points.len() {
                let dx = points[i].0 - points[j].0;
                let dy = points[i].1 - points[j].1;
                let d = dx * dx + dy * dy;
                if d < distance {
                    distance = d;
                    closest_pair = (points[i].clone(), points[j].clone());
                }
            }
        }

        // check in the neighbors
        let neighbors = [
            (cell_x - 1, cell_y - 1),
            (cell_x - 1, cell_y),
            (cell_x - 1, cell_y + 1),
            (cell_x, cell_y - 1),
            (cell_x, cell_y + 1),
            (cell_x + 1, cell_y - 1),
            (cell_x + 1, cell_y),
            (cell_x + 1, cell_y + 1),
        ];
        for point in points {
            for key in neighbors {
                if let Some(points) = cells.get(&key) {
                    for other in points {
                        let dx = point.0 - other.0;
                        let dy = point.1 - other.1;
                        let d = dx * dx + dy * dy;
                        if d < distance {
                            distance = d;
                            closest_pair = (point.clone(), other.clone());
                        }
                    }
                }
            }
        }
    }

    closest_pair
}
