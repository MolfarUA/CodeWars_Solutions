595bbea8a930ac0b91000130

fn calculate_1_rm(w: i32, r: i32) -> i32 {
    let mut x = vec![
        w as f64 * (1.00 + (r as f64 / 30.00)),
        (100.00 * w as f64) / (101.3 - 2.67123 * r as f64),
        (r as f64).powf(0.1000) as f64 * w as f64,
    ]
    .iter()
    .map(|x| x.round() as i32)
    .collect::<Vec<i32>>();
    x.sort_unstable();
    match r {
        0 => 0,
        1 => w,
        _ => x[2],
    }
}
_______________________________
fn calculate_1_rm(w: i32, r: i32) -> i32 {
    assert!(w >= 0 && r >= 0);
    if r < 2 {
        return w * r;
    }
    let w = w as f64;
    let r = r as f64;
    [
        w * (1.0 + r / 30.0),
        100.0 * w / (101.3 - 2.67123 * r),
        w * r.powf(0.1),
    ]
    .iter()
    .map(|&n| n.round() as i32)
    .max()
    .unwrap()
}
_______________________________
fn calculate_1_rm(wi: i32, ri: i32) -> i32 {
    let (w, r) = (wi as f64, ri as f64);
    let epley      = w*(1. + (r / 30.));
    let mc_glothin = 100.*w / (101.3 - (2.67123 * r));
    let lombardi   = w*r.powf(0.1);

    match ri {
        0 => 0,
        1 => wi,
        _ => epley.max(mc_glothin).max(lombardi).round() as i32
    }
}
_______________________________
fn calculate_1_rm(w: i32, r: i32) -> i32 {
    match r {
        0 => 0,
        1 => w,
        r => {
            let w = w as f64;
            let r = r as f64;
            let epley = w*(1.0 + r / 30.0);
            let mcglothin = (100.0*w)/(101.3 - 2.67123*r);
            let lombardi : f64 = w * r.powf(0.10);
            
            epley.max(mcglothin).max(lombardi).round() as i32
        }
    }
}
