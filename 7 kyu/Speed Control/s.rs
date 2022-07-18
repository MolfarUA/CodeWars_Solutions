56484848ba95170a8000004d


fn gps(s: i32, xs: Vec<f64>) -> i32 {
    xs.windows(2).map(|xx| 3600. * (xx[1] - xx[0]) / s as f64).fold(0., f64::max) as i32
}
_____________________________
fn gps(d: i32, xs: Vec<f64>) -> i32 {
  xs.iter()
    .zip(xs.iter().skip(1))
    .map(|(a, b)| (b - a) * 3600.0 / (d as f64))
    .fold(0.0, f64::max).floor() as i32
}
_____________________________
fn gps(s: i32, x: Vec<f64>) -> i32 {
    x.windows(2)
        .map(|distance| (3600. * (distance[1] - distance[0]) / s as f64) as i32)
        .max()
        .unwrap_or(0)
}
